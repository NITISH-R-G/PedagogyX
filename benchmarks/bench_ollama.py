#!/usr/bin/env python3
"""Benchmark Ollama LLM tokens/sec. S01-09."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

RESULTS_DIR = Path(__file__).resolve().parent / "results"
DEFAULT_PROMPT = (
    "Summarize this lesson metrics JSON in 3 bullet points for a school admin: "
    '{"teacher_talk_ratio": 0.68, "student_talk_ratio": 0.32, "activity": "moderate"}'
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Ollama LLM benchmark")
    parser.add_argument("--host", default="http://127.0.0.1:11434")
    parser.add_argument(
        "--model",
        default=os.environ.get("BENCH_OLLAMA_MODEL", "qwen2.5:7b-instruct-q4_K_M"),
    )
    parser.add_argument("--prompt", default=DEFAULT_PROMPT)
    args = parser.parse_args()

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    try:
        r = requests.get(f"{args.host}/api/tags", timeout=5)
        r.raise_for_status()
    except requests.RequestException as exc:
        print(f"Ollama not reachable at {args.host}: {exc}")
        print("Start Ollama and pull model: ollama pull qwen2.5:7b-instruct-q4_K_M")
        return 1

    payload = {
        "model": args.model,
        "prompt": args.prompt,
        "stream": False,
        "options": {"num_predict": 256},
    }

    t0 = time.perf_counter()
    resp = requests.post(f"{args.host}/api/generate", json=payload, timeout=600)
    elapsed = time.perf_counter() - t0
    resp.raise_for_status()
    data = resp.json()

    eval_count = data.get("eval_count", 0)
    tps = eval_count / elapsed if elapsed > 0 else 0.0

    result = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "script": "bench_ollama.py",
        "model": args.model,
        "wall_sec": round(elapsed, 3),
        "eval_count": eval_count,
        "tokens_per_sec": round(tps, 2),
        "response_preview": (data.get("response") or "")[:200],
    }

    out = RESULTS_DIR / f"ollama_{args.model.replace(':', '_')}.json"
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
