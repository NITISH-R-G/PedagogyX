from unittest.mock import patch, MagicMock
from uuid import uuid4
from datetime import datetime, timezone
from psycopg2.extras import Json
from app.db import (
    get_transcript,
    insert_session,
    complete_session,
    get_session,
    insert_chunk,
    list_chunks,
    count_chunks,
    save_transcript,
    save_metrics,
    get_metrics,
    school_overview,
)


def test_get_transcript_found():
    session_id = uuid4()
    mock_row = {"session_id": str(session_id), "text": "Hello world", "language": "en"}

    with patch("app.db.get_conn") as mock_get_conn:
        mock_conn = MagicMock()
        mock_get_conn.return_value.__enter__.return_value = mock_conn

        mock_cur = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cur

        mock_cur.fetchone.return_value = mock_row

        result = get_transcript(session_id)

        assert result == mock_row
        mock_cur.execute.assert_called_once_with(
            "SELECT * FROM session_transcripts WHERE session_id = %s",
            (str(session_id),),
        )


def test_get_transcript_not_found():
    session_id = uuid4()

    with patch("app.db.get_conn") as mock_get_conn:
        mock_conn = MagicMock()
        mock_get_conn.return_value.__enter__.return_value = mock_conn

        mock_cur = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cur

        mock_cur.fetchone.return_value = None

        result = get_transcript(session_id)

        assert result is None
        mock_cur.execute.assert_called_once_with(
            "SELECT * FROM session_transcripts WHERE session_id = %s",
            (str(session_id),),
        )


def test_insert_session():
    mock_row = {
        "id": str(uuid4()),
        "school_id": "school_1",
        "room_id": "room_1",
        "teacher_id": "teacher_1",
    }

    with patch("app.db.get_conn") as mock_get_conn:
        mock_conn = MagicMock()
        mock_get_conn.return_value.__enter__.return_value = mock_conn

        mock_cur = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cur
        mock_cur.fetchone.return_value = mock_row

        result = insert_session("school_1", "room_1", "teacher_1")
        assert result == mock_row
        mock_cur.execute.assert_called_once()


def test_complete_session():
    session_id = uuid4()
    mock_row = {"id": str(session_id), "status": "completed"}

    with patch("app.db.get_conn") as mock_get_conn:
        mock_conn = MagicMock()
        mock_get_conn.return_value.__enter__.return_value = mock_conn

        mock_cur = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cur
        mock_cur.fetchone.return_value = mock_row

        result = complete_session(session_id)
        assert result == mock_row
        mock_cur.execute.assert_called_once()


def test_complete_session_not_found():
    session_id = uuid4()

    with patch("app.db.get_conn") as mock_get_conn:
        mock_conn = MagicMock()
        mock_get_conn.return_value.__enter__.return_value = mock_conn

        mock_cur = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cur
        mock_cur.fetchone.return_value = None

        result = complete_session(session_id)
        assert result is None
        mock_cur.execute.assert_called_once()


def test_get_session():
    session_id = uuid4()
    mock_row = {"id": str(session_id), "status": "active"}

    with patch("app.db.get_conn") as mock_get_conn:
        mock_conn = MagicMock()
        mock_get_conn.return_value.__enter__.return_value = mock_conn

        mock_cur = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cur
        mock_cur.fetchone.return_value = mock_row

        result = get_session(session_id)
        assert result == mock_row
        mock_cur.execute.assert_called_once()


def test_get_session_not_found():
    session_id = uuid4()

    with patch("app.db.get_conn") as mock_get_conn:
        mock_conn = MagicMock()
        mock_get_conn.return_value.__enter__.return_value = mock_conn

        mock_cur = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cur
        mock_cur.fetchone.return_value = None

        result = get_session(session_id)
        assert result is None
        mock_cur.execute.assert_called_once()


def test_insert_chunk():
    session_id = uuid4()
    mock_row = {"session_id": str(session_id), "chunk_index": 1}

    with patch("app.db.get_conn") as mock_get_conn:
        mock_conn = MagicMock()
        mock_get_conn.return_value.__enter__.return_value = mock_conn

        mock_cur = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cur
        mock_cur.fetchone.return_value = mock_row

        result = insert_chunk(session_id, 1, "key", 100, "audio/wav")
        assert result == mock_row
        mock_cur.execute.assert_called_once()


def test_list_chunks():
    session_id = uuid4()
    mock_rows = [{"chunk_index": 1}, {"chunk_index": 2}]

    with patch("app.db.get_conn") as mock_get_conn:
        mock_conn = MagicMock()
        mock_get_conn.return_value.__enter__.return_value = mock_conn

        mock_cur = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cur
        mock_cur.fetchall.return_value = mock_rows

        result = list_chunks(session_id)
        assert result == mock_rows
        mock_cur.execute.assert_called_once()


def test_count_chunks():
    session_id = uuid4()

    with patch("app.db.get_conn") as mock_get_conn:
        mock_conn = MagicMock()
        mock_get_conn.return_value.__enter__.return_value = mock_conn

        mock_cur = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cur
        mock_cur.fetchone.return_value = [5]

        result = count_chunks(session_id)
        assert result == 5
        mock_cur.execute.assert_called_once()


@patch("app.db.datetime")
def test_save_transcript(mock_datetime):
    session_id = uuid4()
    mock_now = datetime(2023, 1, 1, tzinfo=timezone.utc)
    mock_datetime.now.return_value = mock_now

    with patch("app.db.get_conn") as mock_get_conn:
        mock_conn = MagicMock()
        mock_get_conn.return_value.__enter__.return_value = mock_conn

        mock_cur = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cur

        save_transcript(session_id, "text", [], 1.0)
        mock_cur.execute.assert_called_once()

        # Check that Json was used
        args, kwargs = mock_cur.execute.call_args
        assert isinstance(args[1][3], type(Json([])))


@patch("app.db.datetime")
def test_save_metrics(mock_datetime):
    session_id = uuid4()
    mock_now = datetime(2023, 1, 1, tzinfo=timezone.utc)
    mock_datetime.now.return_value = mock_now

    with patch("app.db.get_conn") as mock_get_conn:
        mock_conn = MagicMock()
        mock_get_conn.return_value.__enter__.return_value = mock_conn

        mock_cur = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cur

        save_metrics(session_id, 0.6, 0.4, "high", 5.0)
        mock_cur.execute.assert_called_once()


def test_get_metrics():
    session_id = uuid4()
    mock_row = {"session_id": str(session_id), "teacher_talk_ratio": 0.6}

    with patch("app.db.get_conn") as mock_get_conn:
        mock_conn = MagicMock()
        mock_get_conn.return_value.__enter__.return_value = mock_conn

        mock_cur = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cur
        mock_cur.fetchone.return_value = mock_row

        result = get_metrics(session_id)
        assert result == mock_row
        mock_cur.execute.assert_called_once()


def test_get_metrics_not_found():
    session_id = uuid4()

    with patch("app.db.get_conn") as mock_get_conn:
        mock_conn = MagicMock()
        mock_get_conn.return_value.__enter__.return_value = mock_conn

        mock_cur = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cur
        mock_cur.fetchone.return_value = None

        result = get_metrics(session_id)
        assert result is None
        mock_cur.execute.assert_called_once()


@patch("app.db.settings")
def test_school_overview(mock_settings):
    mock_settings.overview_rooms_target = "10"

    mock_counts = {
        "rooms_observed": 5,
        "sessions_total": 20,
        "sessions_completed": 15,
        "sessions_week": 5,
    }
    mock_recent = [
        {
            "id": "test_id",
            "room_id": "room_1",
            "teacher_id": "teacher_1",
            "status": "completed",
            "created_at": datetime(2023, 1, 1, tzinfo=timezone.utc),
            "completed_at": datetime(2023, 1, 1, tzinfo=timezone.utc),
            "teacher_talk_ratio": 0.6,
            "student_talk_ratio": 0.4,
            "preview_ready_at": datetime(2023, 1, 1, tzinfo=timezone.utc),
            "insight_latency_sec": 5.0,
            "metric_confidence": "high",
        }
    ]
    mock_median = {"percentile_cont": 5.0}

    with patch("app.db.get_conn") as mock_get_conn:
        mock_conn = MagicMock()
        mock_get_conn.return_value.__enter__.return_value = mock_conn

        mock_cur = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cur

        # Since school_overview calls them sequentially on the same cursor
        mock_cur.fetchone.side_effect = [mock_counts, mock_median]
        mock_cur.fetchall.side_effect = [mock_recent]

        result = school_overview("school_1")

        assert result["school_id"] == "school_1"
        assert result["m_a_coverage"]["rooms_observed"] == 5
        assert result["m_a_coverage"]["rooms_target"] == 10
        assert result["m_a_coverage"]["coverage_pct"] == 50.0
        assert result["m_b_median_insight_sec"] == 5.0
        assert result["sessions_total"] == 20
        assert result["sessions_completed"] == 15
        assert result["sessions_week"] == 5
        assert len(result["recent_sessions"]) == 1


def test_school_overview_no_rooms_observed():
    with patch("app.db.settings") as mock_settings:
        mock_settings.overview_rooms_target = "10"

        mock_counts = {
            "rooms_observed": None,
            "sessions_total": 0,
            "sessions_completed": 0,
            "sessions_week": 0,
        }
        mock_recent = []
        mock_median = {"percentile_cont": None}

        with patch("app.db.get_conn") as mock_get_conn:
            mock_conn = MagicMock()
            mock_get_conn.return_value.__enter__.return_value = mock_conn

            mock_cur = MagicMock()
            mock_conn.cursor.return_value.__enter__.return_value = mock_cur

            mock_cur.fetchone.side_effect = [mock_counts, mock_median]
            mock_cur.fetchall.side_effect = [mock_recent]

            result = school_overview("school_1")

            assert result["school_id"] == "school_1"
            assert result["m_a_coverage"]["rooms_observed"] == 0
            assert result["m_a_coverage"]["coverage_pct"] == 0.0
            assert result["m_b_median_insight_sec"] is None
