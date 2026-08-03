#!/usr/bin/env python3
"""Benchmark YOLO11 inference FPS at 480p/720p. S01-09."""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

RESULTS_DIR = Path(__file__).resolve().parent / "results"


def has_cuda() -> bool:
    """Check if CUDA is available."""
    try:
        import torch

        return torch.cuda.is_available()
    except ImportError:
        return False


def get_device(requested: str) -> str:
    """Resolve device selection.
    
    Args:
        requested: Device string ('auto', 'cuda', or 'cpu')
        
    Returns:
        Resolved device string ('cuda' or 'cpu')
    """
    if requested != "auto":
        return requested
    return "cuda" if has_cuda() else "cpu"


def run_benchmark(model_name: str, device: str, height: int, width: int, frames: int) -> dict:
    """Run YOLO benchmark and return results.
    
    Args:
        model_name: Model name to benchmark
        device: Target device ('cuda' or 'cpu')
        height: Frame height in pixels
        width: Frame width in pixels
        frames: Number of frames to process
        
    Returns:
        Dictionary containing benchmark results
    """
    from ultralytics import YOLO

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    model = YOLO(model_name)
    frame = np.zeros((height, width, 3), dtype=np.uint8)

    # Warmup
    model.predict(frame, device=device, verbose=False)

    t0 = time.perf_counter()
    for _ in range(frames):
        model.predict(frame, device=device, verbose=False)
    elapsed = time.perf_counter() - t0

    fps = frames / elapsed if elapsed > 0 else 0.0

    result = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "script": "bench_yolo_trt.py",
        "model": model_name,
        "device": device,
        "resolution": f"{width}x{height}",
        "frames": frames,
        "wall_sec": round(elapsed, 3),
        "fps": round(fps, 2),
        "note": "TensorRT export not run in CI; use export=engine locally for TRT numbers",
    }

    if device == "cuda":
        try:
            import torch

            result["vram_allocated_gb"] = round(torch.cuda.max_memory_allocated() / 1e9, 3)
        except Exception:
            pass

    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="YOLO11 inference benchmark")
    parser.add_argument("--model", default="yolo11n.pt")
    parser.add_argument("--device", default="auto", choices=["auto", "cuda", "cpu"])
    parser.add_argument("--height", type=int, default=480)
    parser.add_argument("--width", type=int, default=854)
    parser.add_argument("--frames", type=int, default=300)
    args = parser.parse_args()

    device = get_device(args.device)

    try:
        from ultralytics import YOLO
    except ImportError:
        print("Install: pip install -r benchmarks/requirements-bench.txt")
        return 1

    result = run_benchmark(args.model, device, args.height, args.width, args.frames)

    out = RESULTS_DIR / f"yolo_{args.height}p_{device}.json"
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
