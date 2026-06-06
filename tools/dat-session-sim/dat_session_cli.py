#!/usr/bin/env python3
"""
DAT session simulator — mirrors Meta Wearables DAT lifecycle against PedagogyX API.

Lifecycle (session): IDLE → STARTING → STARTED → (optional PAUSED) → STOPPING → STOPPED
Stream: STOPPED → STARTING → STREAMING → STOPPING → STOPPED

Usage:
  python dat_session_cli.py run --api-url http://localhost:8080 --frames 30
  python dat_session_cli.py run --no-camera   # synthetic frames only
"""

from __future__ import annotations

import argparse
import io
import sys
import time

import httpx

DEFAULT_API = "http://localhost:8080"


def post(client: httpx.Client, path: str, json: dict | None = None) -> dict:
    r = client.post(path, json=json or {})
    r.raise_for_status()
    return r.json()


def upload_frame_jpeg(
    client: httpx.Client, pedagogy_session_id: str, chunk_index: int, jpeg_bytes: bytes
) -> None:
    client.post(
        f"/v1/sessions/{pedagogy_session_id}/chunks/{chunk_index}",
        files={"file": (f"frame_{chunk_index:04d}.jpg", jpeg_bytes, "image/jpeg")},
    ).raise_for_status()


def synthetic_jpeg() -> bytes:
    try:
        from PIL import Image

        img = Image.new("RGB", (640, 480), color=(40, 80, 120))
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=70)
        return buf.getvalue()
    except ImportError:
        return b"\xff\xd8\xff\xd9"


def capture_jpeg() -> bytes | None:
    try:
        import cv2

        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return None
        ok, frame = cap.read()
        cap.release()
        if not ok:
            return None
        ok, enc = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 70])
        return enc.tobytes() if ok else None
    except ImportError:
        return None


def _create_dat_session(client: httpx.Client, args: argparse.Namespace) -> str:
    created = post(
        client,
        "/v1/dat-sessions",
        {
            "school_id": args.school_id,
            "room_id": args.room_id,
            "teacher_id": args.teacher_id,
            "device_label": args.device_label,
        },
    )
    dat_id = created["dat_session_id"]
    print(f"DAT session {dat_id} state={created['state']}")
    return dat_id


def _start_dat_session(client: httpx.Client, dat_id: str) -> None:
    started = post(client, f"/v1/dat-sessions/{dat_id}/start")
    print(f"session.start → state={started['state']}")


def _start_dat_stream(client: httpx.Client, dat_id: str) -> str | None:
    streaming = post(client, f"/v1/dat-sessions/{dat_id}/stream/start")
    ped_id = streaming.get("pedagogy_session_id")
    print(
        f"stream.start → session={streaming['state']} stream={streaming['stream_state']} "
        f"pedagogy_session={ped_id}"
    )
    return ped_id


def _upload_stream_frames(
    client: httpx.Client, dat_id: str, ped_id: str, args: argparse.Namespace
) -> None:
    for i in range(args.frames):
        if args.no_camera:
            jpeg = synthetic_jpeg()
        else:
            jpeg = capture_jpeg() or synthetic_jpeg()
        upload_frame_jpeg(client, ped_id, i, jpeg)
        post(
            client,
            f"/v1/dat-sessions/{dat_id}/lifecycle",
            {
                "event_type": "stream.frame",
                "target": "stream",
                "to_state": "STREAMING",
                "detail": {"frame_index": i, "bytes": len(jpeg)},
            },
        )
        print(f"  frame {i} uploaded ({len(jpeg)} bytes)")
        time.sleep(args.frame_interval)


def _complete_pedagogy_session(client: httpx.Client, ped_id: str) -> None:
    post(client, f"/v1/sessions/{ped_id}/complete")
    print(f"pedagogy session {ped_id} completed → ASR pipeline")


def _stop_dat_session(client: httpx.Client, dat_id: str) -> None:
    stopped = post(client, f"/v1/dat-sessions/{dat_id}/stop")
    print(f"session.stop → state={stopped['state']} stream={stopped['stream_state']}")


def _print_recent_events(client: httpx.Client, dat_id: str) -> None:
    detail = client.get(f"/v1/dat-sessions/{dat_id}").json()
    print(f"events: {len(detail.get('recent_events', []))} logged")
    for ev in reversed(detail.get("recent_events", [])[:8]):
        print(f"  - {ev['event_type']}: {ev.get('from_state')} → {ev.get('to_state')}")


def run_session(args: argparse.Namespace) -> int:
    base = args.api_url.rstrip("/")
    headers = {}
    if args.api_key:
        headers["Authorization"] = f"Bearer {args.api_key}"

    with httpx.Client(base_url=base, headers=headers, timeout=60.0) as client:
        dat_id = _create_dat_session(client, args)
        _start_dat_session(client, dat_id)

        ped_id = _start_dat_stream(client, dat_id)
        if not ped_id:
            print("ERROR: no pedagogy_session_id linked", file=sys.stderr)
            return 1

        _upload_stream_frames(client, dat_id, ped_id, args)
        _complete_pedagogy_session(client, ped_id)
        _stop_dat_session(client, dat_id)
        _print_recent_events(client, dat_id)

    print("DAT session run OK")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="PedagogyX DAT session simulator")
    sub = parser.add_subparsers(dest="cmd", required=True)

    run_p = sub.add_parser("run", help="Full DAT lifecycle with camera frames")
    run_p.add_argument("--api-url", default=DEFAULT_API)
    run_p.add_argument("--school-id", default="pilot-school-dev")
    run_p.add_argument("--room-id", default="room-dat-1")
    run_p.add_argument("--teacher-id", default="teacher-dat")
    run_p.add_argument("--device-label", default="dev-webcam")
    run_p.add_argument("--frames", type=int, default=10)
    run_p.add_argument("--frame-interval", type=float, default=0.5)
    run_p.add_argument("--no-camera", action="store_true")
    run_p.add_argument("--api-key", default="dev_api_key_placeholder", help="API key for authentication")
    run_p.set_defaults(func=run_session)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
