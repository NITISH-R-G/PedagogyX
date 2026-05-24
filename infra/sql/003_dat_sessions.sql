-- DAT-style capture sessions (Device Access Toolkit lifecycle mirror)

CREATE TABLE IF NOT EXISTS dat_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    school_id TEXT NOT NULL,
    room_id TEXT,
    teacher_id TEXT,
    device_label TEXT,
    state TEXT NOT NULL DEFAULT 'IDLE',
    stream_state TEXT NOT NULL DEFAULT 'STOPPED',
    pedagogy_session_id UUID REFERENCES sessions (id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS dat_session_events (
    id BIGSERIAL PRIMARY KEY,
    dat_session_id UUID NOT NULL REFERENCES dat_sessions (id) ON DELETE CASCADE,
    event_type TEXT NOT NULL,
    from_state TEXT,
    to_state TEXT,
    detail JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_dat_sessions_school ON dat_sessions (school_id, updated_at DESC);
CREATE INDEX IF NOT EXISTS idx_dat_events_session ON dat_session_events (dat_session_id, created_at);
