from uuid import UUID

from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, Field

from app import dat_db, db
from app.dat_db import append_event, EventData
from app.auth import verify_api_key

router = APIRouter(
    prefix="/v1/dat-sessions",
    tags=["dat"],
    dependencies=[Depends(verify_api_key)]
)


class DatSessionCreate(BaseModel):
    school_id: str = Field(..., min_length=1)
    room_id: str | None = None
    teacher_id: str | None = None
    device_label: str | None = None


class LifecycleEvent(BaseModel):
    event_type: str = Field(..., min_length=1)
    target: str = Field(default="session", pattern="^(session|stream)$")
    to_state: str | None = None
    detail: dict = Field(default_factory=dict)


@router.post("")
def create_dat_session(body: DatSessionCreate):
    row = dat_db.create_dat_session(
        body.school_id, body.room_id, body.teacher_id, body.device_label
    )
    append_event(
        row["id"],
        EventData("SESSION_CREATED", None, "IDLE", {"device_label": body.device_label})
    )
    return _serialize(row)


@router.get("/{dat_session_id}")
def get_dat_session(dat_session_id: UUID):
    row = dat_db.get_dat_session(dat_session_id)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="dat session not found")
    out = _serialize(row)
    out["recent_events"] = [
        {
            "event_type": e["event_type"],
            "from_state": e["from_state"],
            "to_state": e["to_state"],
            "detail": e["detail"],
            "created_at": e["created_at"].isoformat() if e.get("created_at") else None,
        }
        for e in dat_db.list_events(dat_session_id, limit=20)
    ]
    return out


@router.post("/{dat_session_id}/lifecycle")
def post_lifecycle(dat_session_id: UUID, body: LifecycleEvent):
    try:
        if body.target == "session":
            if not body.to_state:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="to_state required for session")
            row = dat_db.transition_session_state(
                dat_session_id, body.to_state, body.event_type, body.detail
            )
        else:
            if not body.to_state:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="to_state required for stream")
            row = dat_db.transition_stream_state(
                dat_session_id, body.to_state, body.event_type, body.detail
            )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    # On STREAMING: ensure linked PedagogyX upload session exists
    if body.target == "stream" and body.to_state == "STREAMING":
        row = _ensure_pedagogy_session(row)

    return _serialize(row)


@router.post("/{dat_session_id}/start")
def start_dat_session(dat_session_id: UUID):
    """Convenience: IDLE → STARTING → STARTED (session.start)."""
    try:
        dat_db.transition_session_state(dat_session_id, "STARTING", "session.start", {})
        row = dat_db.transition_session_state(dat_session_id, "STARTED", "session.started", {})
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return _serialize(row)


@router.post("/{dat_session_id}/stream/start")
def start_stream(dat_session_id: UUID):
    """Convenience: addStream + start — STOPPED → STARTING → STREAMING."""
    row = dat_db.get_dat_session(dat_session_id)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="dat session not found")
    if row["state"] not in ("STARTED", "STREAMING", "PAUSED"):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="session must be STARTED before addStream")
    try:
        dat_db.transition_stream_state(dat_session_id, "STARTING", "stream.add", {})
        row = dat_db.transition_stream_state(dat_session_id, "STREAMING", "stream.streaming", {})
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    row = _ensure_pedagogy_session(row)
    return _serialize(row)


@router.post("/{dat_session_id}/stop")
def stop_dat_session(dat_session_id: UUID):
    """Cascading stop: stream then session (DAT semantics)."""
    row = dat_db.get_dat_session(dat_session_id)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="dat session not found")
    try:
        if row["stream_state"] not in ("STOPPED",):
            dat_db.transition_stream_state(dat_session_id, "STOPPING", "stream.stop", {})
            dat_db.transition_stream_state(dat_session_id, "STOPPED", "stream.stopped", {})
        if row["state"] not in ("STOPPED", "IDLE"):
            dat_db.transition_session_state(dat_session_id, "STOPPING", "session.stop", {})
            row = dat_db.transition_session_state(dat_session_id, "STOPPED", "session.stopped", {})
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return _serialize(row)


def _ensure_pedagogy_session(row: dict) -> dict:
    if row.get("pedagogy_session_id"):
        return row
    ped = db.insert_session(row["school_id"], row.get("room_id"), row.get("teacher_id"))
    dat_db.link_pedagogy_session(row["id"], ped["id"])
    append_event(
        row["id"],
        EventData("PEDAGOGY_SESSION_LINKED", None, None, {"pedagogy_session_id": str(ped["id"])})
    )
    return dat_db.get_dat_session(row["id"]) or row


def _serialize(row: dict) -> dict:
    return {
        "dat_session_id": str(row["id"]),
        "school_id": row["school_id"],
        "room_id": row.get("room_id"),
        "teacher_id": row.get("teacher_id"),
        "device_label": row.get("device_label"),
        "state": row["state"],
        "stream_state": row["stream_state"],
        "pedagogy_session_id": str(row["pedagogy_session_id"])
        if row.get("pedagogy_session_id")
        else None,
        "upload_session_url": f"/v1/sessions/{row['pedagogy_session_id']}/chunks/{{chunk_index}}"
        if row.get("pedagogy_session_id")
        else None,
        "updated_at": row["updated_at"].isoformat() if row.get("updated_at") else None,
    }
