#!/usr/bin/env python3
"""Benchmark YOLO11 inference FPS at 480p/720p. S01-09."""

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

RESULTS_DIR = Path(__file__).resolve().parent / "results"


def _has_cuda() -> bool:
    try:
        import torch

        return torch.cuda.is_available()
    except ImportError:
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description="YOLO11 inference benchmark")
    parser.add_argument("--model", default="yolo11n.pt")
    parser.add_argument("--device", default="auto", choices=["auto", "cuda", "cpu"])
    parser.add_argument("--height", type=int, default=480)
    parser.add_argument("--width", type=int, default=854)
    parser.add_argument("--frames", type=int, default=300)
    args = parser.parse_args()

    device = args.device
    if device == "auto":
        device = "cuda" if _has_cuda() else "cpu"

    try:
        from ultralytics import YOLO
    except ImportError:
        print("Install: pip install -r benchmarks/requirements-bench.txt")
        return 1

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    model = YOLO(args.model)
    frame = np.zeros((args.height, args.width, 3), dtype=np.uint8)

    # Warmup
    model.predict(frame, device=device, verbose=False)

    frames = [frame] * args.frames

    t0 = time.perf_counter()
    # stream=True is required for batching without memory explosion in some environments
    for _ in model.predict(frames, device=device, verbose=False, stream=True):
        pass
    elapsed = time.perf_counter() - t0

    fps = args.frames / elapsed if elapsed > 0 else 0.0

    result = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "script": "bench_yolo_trt.py",
        "model": args.model,
        "device": device,
        "resolution": f"{args.width}x{args.height}",
        "frames": args.frames,
        "wall_sec": round(elapsed, 3),
        "fps": round(fps, 2),
        "note": "TensorRT export not run in CI; use export=engine locally for TRT numbers",
    }

    if device == "cuda":
        try:
            import torch

            result["vram_allocated_gb"] = round(torch.cuda.max_memory_allocated() / 1e9, 3)
        except Exception as e:
            print(f"Warning: Could not read VRAM allocated: {e}", file=sys.stderr)

    out = RESULTS_DIR / f"yolo_{args.height}p_{device}.json"
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
