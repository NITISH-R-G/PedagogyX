#!/usr/bin/env python3
"""Benchmark faster-whisper RTF on sample audio. S01-09."""

from __future__ import annotations

import argparse
import json
import sys
import time
import wave
from datetime import datetime, timezone
from pathlib import Path

RESULTS_DIR = Path(__file__).resolve().parent / "results"


def _has_cuda() -> bool:
    try:
        import torch

        return torch.cuda.is_available()
    except ImportError:
        return False


def _make_silent_wav(path: Path, duration_sec: float = 60.0, sample_rate: int = 16000) -> None:
    n_frames = int(duration_sec * sample_rate)
    with wave.open(str(path), "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(b"\x00\x00" * n_frames)


def main() -> int:
    parser = argparse.ArgumentParser(description="Whisper ASR benchmark")
    parser.add_argument("--model", default="medium", choices=["tiny", "small", "medium", "large-v3"])
    parser.add_argument("--device", default="auto", choices=["auto", "cuda", "cpu"])
    parser.add_argument("--duration-sec", type=float, default=300.0, help="Synthetic audio length")
    parser.add_argument("--compute-type", default="int8", help="CTranslate2 compute type")
    args = parser.parse_args()

    device = args.device
    if device == "auto":
        device = "cuda" if _has_cuda() else "cpu"

    if device == "cuda" and not _has_cuda():
        print("CUDA requested but unavailable; use --device cpu or run on RTX 5070 host.")
        return 1

    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print("Install: pip install -r benchmarks/requirements-bench.txt")
        return 1

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    sample = RESULTS_DIR / "_sample_silence.wav"
    if not sample.exists():
        print(f"Creating {args.duration_sec}s silent sample at {sample}")
        _make_silent_wav(sample, args.duration_sec)

    print(f"Loading faster-whisper {args.model} ({args.compute_type}) on {device}...")
    model = WhisperModel(args.model, device=device, compute_type=args.compute_type)

    t0 = time.perf_counter()
    segments, info = model.transcribe(str(sample), beam_size=1, vad_filter=True)
    text_parts = [s.text for s in segments]
    elapsed = time.perf_counter() - t0

    audio_duration = args.duration_sec
    rtf = elapsed / audio_duration if audio_duration else 0.0

    result = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "script": "bench_whisper.py",
        "model": args.model,
        "device": device,
        "compute_type": args.compute_type,
        "audio_duration_sec": audio_duration,
        "wall_sec": round(elapsed, 3),
        "rtf": round(rtf, 4),
        "language": info.language,
        "segments": len(text_parts),
    }

    if device == "cuda":
        try:
            import torch

            result["vram_allocated_gb"] = round(torch.cuda.max_memory_allocated() / 1e9, 3)
        except Exception:
            pass

    out = RESULTS_DIR / f"whisper_{args.model}_{device}.json"
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
