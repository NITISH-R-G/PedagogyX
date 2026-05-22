from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class SessionCreate(BaseModel):
    school_id: str = Field(..., min_length=1, max_length=128)
    room_id: str | None = Field(default=None, max_length=64)
    teacher_id: str | None = Field(default=None, max_length=128)


class SessionComplete(BaseModel):
    session_id: UUID


class JobEnvelope(BaseModel):
    job_type: Literal["asr", "talk_ratio"] = "asr"
    session_id: UUID
    school_id: str
    enqueued_at: datetime = Field(default_factory=datetime.utcnow)
