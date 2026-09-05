from datetime import timezone
from uuid import uuid4

from pedagogyx_core.models import JobEnvelope


def test_job_envelope_enqueued_at_default():
    session_id = uuid4()
    job = JobEnvelope(session_id=session_id, school_id="school-123")
    assert job.session_id == session_id
    assert job.school_id == "school-123"
    assert job.job_type == "asr"
    assert job.enqueued_at is not None
    assert job.enqueued_at.tzinfo == timezone.utc
