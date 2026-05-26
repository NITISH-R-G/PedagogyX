import os
import sys
import wave
from pathlib import Path

# Add parent directory to sys.path so we can import bench_whisper
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bench_whisper import _make_silent_wav  # noqa: E402


def test_make_silent_wav(tmp_path: Path):
    out_path = tmp_path / "test.wav"
    duration = 2.0
    sample_rate = 8000
    _make_silent_wav(out_path, duration_sec=duration, sample_rate=sample_rate)

    assert out_path.exists()

    with wave.open(str(out_path), "r") as wf:
        assert wf.getnchannels() == 1
        assert wf.getsampwidth() == 2
        assert wf.getframerate() == sample_rate
        assert wf.getnframes() == int(duration * sample_rate)

        frames = wf.readframes(wf.getnframes())
        assert len(frames) == int(duration * sample_rate) * 2
        assert frames == b"\x00\x00" * int(duration * sample_rate)


def test_make_silent_wav_zero_duration(tmp_path: Path):
    out_path = tmp_path / "test_zero.wav"
    _make_silent_wav(out_path, duration_sec=0.0)

    assert out_path.exists()

    with wave.open(str(out_path), "r") as wf:
        assert wf.getnframes() == 0
        frames = wf.readframes(10)
        assert len(frames) == 0


def test_make_silent_wav_fractional_duration(tmp_path: Path):
    out_path = tmp_path / "test_frac.wav"
    duration = 0.5
    sample_rate = 16000
    _make_silent_wav(out_path, duration_sec=duration, sample_rate=sample_rate)

    assert out_path.exists()

    with wave.open(str(out_path), "r") as wf:
        assert wf.getnframes() == int(duration * sample_rate)
