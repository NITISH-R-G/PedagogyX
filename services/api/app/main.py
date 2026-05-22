from contextlib import asynccontextmanager
from uuid import UUID

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app import db, minio_client, queue
from app.config import settings


class SessionCreateBody(BaseModel):
    school_id: str = Field(..., min_length=1)
    room_id: str | None = None
    teacher_id: str | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        minio_client.ensure_bucket()
    except Exception as exc:
        # MinIO may start slightly after API in compose; bucket created on retry via upload path later.
        print(f"WARN: MinIO bucket init skipped: {exc}")
    yield


app = FastAPI(
    title="PedagogyX API",
    version="0.1.0-boilerplate",
    lifespan=lifespan,
)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "api",
        "boilerplate": True,
        "g2_prod_data": False,
    }


@app.post("/v1/sessions")
def create_session(body: SessionCreateBody):
    row = db.insert_session(body.school_id, body.room_id, body.teacher_id)
    return {
        "session_id": str(row["id"]),
        "status": row["status"],
        "school_id": row["school_id"],
        "upload_hint": f"s3://{settings.minio_bucket}/sessions/{row['id']}/chunks/",
    }


@app.get("/v1/sessions/{session_id}")
def get_session(session_id: UUID):
    row = db.get_session(session_id)
    if not row:
        raise HTTPException(status_code=404, detail="session not found")
    return _serialize_session(row)


@app.post("/v1/sessions/{session_id}/complete")
def complete_session(session_id: UUID):
    row = db.complete_session(session_id)
    if not row:
        raise HTTPException(status_code=404, detail="session not found")
    queue.enqueue_asr_job(session_id, row["school_id"])
    return {
        "session_id": str(row["id"]),
        "status": row["status"],
        "job_enqueued": "asr",
    }


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
