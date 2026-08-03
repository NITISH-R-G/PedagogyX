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


def create_silent_wav(path: Path, duration_sec: float = 60.0, sample_rate: int = 16000) -> None:
    """Create a silent WAV file for testing.
    
    Args:
        path: Output file path
        duration_sec: Duration in seconds
        sample_rate: Audio sample rate in Hz
    """
    n_frames = int(duration_sec * sample_rate)
    with wave.open(str(path), "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(b"\x00\x00" * n_frames)


def run_benchmark(model: str, device: str, compute_type: str, duration_sec: float) -> dict:
    """Run Whisper benchmark and return results.
    
    Args:
        model: Model name to benchmark
        device: Target device ('cuda' or 'cpu')
        compute_type: CTranslate2 compute type
        duration_sec: Audio duration in seconds
        
    Returns:
        Dictionary containing benchmark results
    """
    from faster_whisper import WhisperModel

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    sample = RESULTS_DIR / "_sample_silence.wav"
    if not sample.exists():
        print(f"Creating {duration_sec}s silent sample at {sample}")
        create_silent_wav(sample, duration_sec)

    print(f"Loading faster-whisper {model} ({compute_type}) on {device}...")
    model_instance = WhisperModel(model, device=device, compute_type=compute_type)

    t0 = time.perf_counter()
    segments, info = model_instance.transcribe(str(sample), beam_size=1, vad_filter=True)
    text_parts = [s.text for s in segments]
    elapsed = time.perf_counter() - t0

    audio_duration = duration_sec
    rtf = elapsed / audio_duration if audio_duration else 0.0

    result = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "script": "bench_whisper.py",
        "model": model,
        "device": device,
        "compute_type": compute_type,
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

    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Whisper ASR benchmark")
    parser.add_argument("--model", default="medium", choices=["tiny", "small", "medium", "large-v3"])
    parser.add_argument("--device", default="auto", choices=["auto", "cuda", "cpu"])
    parser.add_argument("--duration-sec", type=float, default=300.0, help="Synthetic audio length")
    parser.add_argument("--compute-type", default="int8", help="CTranslate2 compute type")
    args = parser.parse_args()

    device = get_device(args.device)

    if device == "cuda" and not has_cuda():
        print("CUDA requested but unavailable; use --device cpu or run on RTX 5070 host.")
        return 1

    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print("Install: pip install -r benchmarks/requirements-bench.txt")
        return 1

    result = run_benchmark(args.model, device, args.compute_type, args.duration_sec)

    out = RESULTS_DIR / f"whisper_{args.model}_{device}.json"
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
