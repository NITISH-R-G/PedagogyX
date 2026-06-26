import asyncio
import sys
from contextlib import asynccontextmanager
from uuid import UUID

from fastapi import FastAPI, File, HTTPException, UploadFile, status
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel, Field

from app import db, minio_client, queue, storage
from app.config import settings
from app.dat_routes import router as dat_router


class SessionCreateBody(BaseModel):
    school_id: str = Field(..., min_length=1)
    room_id: str | None = None
    teacher_id: str | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await run_in_threadpool(minio_client.ensure_bucket)
    except Exception as exc:
        print(f"WARN: MinIO bucket init skipped: {exc}", file=sys.stderr)
    yield


app = FastAPI(
    title="PedagogyX API",
    version="0.2.1-dat",
    lifespan=lifespan,
)
app.include_router(dat_router)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "api",
        "version": "0.2.1-dat",
        "g2_prod_data": False,
    }


@app.post("/v1/sessions")
def create_session(body: SessionCreateBody):
    row = db.insert_session(body.school_id, body.room_id, body.teacher_id)
    sid = row["id"]
    return {
        "session_id": str(sid),
        "status": row["status"],
        "school_id": row["school_id"],
        "upload_url_template": f"/v1/sessions/{sid}/chunks/{{chunk_index}}",
    }


@app.get("/v1/sessions/{session_id}")
async def get_session(session_id: UUID):
    row = await asyncio.to_thread(db.get_session, session_id)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="session not found")
    payload = _serialize_session(row)

    chunks_task = asyncio.to_thread(db.list_chunks, session_id)
    metrics_task = asyncio.to_thread(db.get_metrics, session_id)
    transcript_task = asyncio.to_thread(db.get_transcript, session_id)

    chunks_data, metrics, transcript = await asyncio.gather(
        chunks_task, metrics_task, transcript_task
    )

    payload["chunks"] = [
        {
            "chunk_index": c["chunk_index"],
            "size_bytes": c["size_bytes"],
            "content_type": c["content_type"],
            "uploaded_at": c["uploaded_at"].isoformat() if c.get("uploaded_at") else None,
        }
        for c in chunks_data
    ]
    if metrics:
        payload["metrics"] = _serialize_metrics(metrics)
    if transcript:
        payload["transcript_preview"] = (transcript["text"] or "")[:200]
    return payload


@app.post("/v1/sessions/{session_id}/chunks/{chunk_index}")
def upload_chunk(
    session_id: UUID,
    chunk_index: int,
    file: UploadFile = File(...),
):
    if chunk_index < 0 or chunk_index > 9999:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="invalid chunk_index")
    row = db.get_session(session_id)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="session not found")
    if row["status"] not in ("active", "created"):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="session not accepting uploads")

    body = file.file.read()
    if len(body) > settings.max_upload_bytes:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="chunk exceeds max size")

    key = storage.put_chunk(session_id, chunk_index, body, file.content_type)
    chunk = db.insert_chunk(session_id, chunk_index, key, len(body), file.content_type)
    return {
        "session_id": str(session_id),
        "chunk_index": chunk["chunk_index"],
        "object_key": chunk["object_key"],
        "size_bytes": chunk["size_bytes"],
    }


@app.post("/v1/sessions/{session_id}/complete")
def complete_session(session_id: UUID):
    row = db.get_session(session_id)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="session not found")
    if row["status"] == "completed":
        return {
            "session_id": str(session_id),
            "status": "completed",
            "job_enqueued": "asr",
            "note": "already completed",
        }
    n_chunks = db.count_chunks(session_id)
    if n_chunks == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="upload at least one chunk before completing",
        )
    row = db.complete_session(session_id)
    queue.enqueue_asr_job(session_id, row["school_id"])
    return {
        "session_id": str(row["id"]),
        "status": row["status"],
        "chunks": n_chunks,
        "job_enqueued": "asr",
    }


@app.get("/v1/sessions/{session_id}/preview")
def session_preview(session_id: UUID):
    row = db.get_session(session_id)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="session not found")
    metrics = db.get_metrics(session_id)
    transcript = db.get_transcript(session_id)
    if not metrics:
        return {
            "session_id": str(session_id),
            "status": row["status"],
            "preview_ready": False,
            "message": "metrics pending",
        }
    return {
        "session_id": str(session_id),
        "status": row["status"],
        "preview_ready": metrics.get("preview_ready_at") is not None,
        "teacher_talk_ratio": metrics.get("teacher_talk_ratio"),
        "student_talk_ratio": metrics.get("student_talk_ratio"),
        "metric_confidence": metrics.get("metric_confidence"),
        "insight_latency_sec": metrics.get("insight_latency_sec"),
        "transcript_excerpt": (transcript["text"][:300] if transcript else None),
    }


@app.get("/v1/schools/{school_id}/overview")
def school_overview(school_id: str):
    return db.school_overview(school_id)


def _serialize_session(row: dict) -> dict:
    return {
        "session_id": str(row["id"]),
        "school_id": row["school_id"],
        "room_id": row["room_id"],
        "teacher_id": row["teacher_id"],
        "status": row["status"],
        "created_at": row["created_at"].isoformat() if row.get("created_at") else None,
        "completed_at": row["completed_at"].isoformat() if row.get("completed_at") else None,
    }


def _serialize_metrics(metrics: dict) -> dict:
    return {
        "teacher_talk_ratio": metrics.get("teacher_talk_ratio"),
        "student_talk_ratio": metrics.get("student_talk_ratio"),
        "metric_confidence": metrics.get("metric_confidence"),
        "preview_ready_at": metrics.get("preview_ready_at").isoformat()
        if metrics.get("preview_ready_at")
        else None,
        "insight_latency_sec": metrics.get("insight_latency_sec"),
    }
