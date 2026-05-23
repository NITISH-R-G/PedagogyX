-- Sprint 03 vertical slice: uploads, transcripts, preview metrics

CREATE TABLE IF NOT EXISTS session_chunks (
    session_id UUID NOT NULL REFERENCES sessions (id) ON DELETE CASCADE,
    chunk_index INT NOT NULL,
    object_key TEXT NOT NULL,
    size_bytes BIGINT NOT NULL DEFAULT 0,
    content_type TEXT,
    uploaded_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (session_id, chunk_index)
);

CREATE TABLE IF NOT EXISTS session_transcripts (
    session_id UUID PRIMARY KEY REFERENCES sessions (id) ON DELETE CASCADE,
    language TEXT NOT NULL DEFAULT 'en',
    text TEXT NOT NULL DEFAULT '',
    segments_json JSONB NOT NULL DEFAULT '[]'::jsonb,
    rtf REAL,
    processed_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS session_metrics (
    session_id UUID PRIMARY KEY REFERENCES sessions (id) ON DELETE CASCADE,
    teacher_talk_ratio REAL,
    student_talk_ratio REAL,
    metric_confidence TEXT NOT NULL DEFAULT 'preview_stub',
    preview_ready_at TIMESTAMPTZ,
    insight_latency_sec REAL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_chunks_session ON session_chunks (session_id);
