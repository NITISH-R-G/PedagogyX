from unittest.mock import patch

from dat_session_cli import main


def test_cli_api_key_from_explicit_arg(monkeypatch):
    monkeypatch.delenv("API_KEY", raising=False)
    test_args = ["dat_session_cli.py", "run", "--api-key", "explicit_key"]
    with (
        patch("sys.argv", test_args),
        patch("dat_session_cli.run_session", return_value=0) as mock_run,
    ):
        main()
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        assert args.api_key == "explicit_key"


def test_cli_api_key_from_env_var(monkeypatch):
    monkeypatch.setenv("API_KEY", "env_provided_key")
    test_args = ["dat_session_cli.py", "run"]
    with (
        patch("sys.argv", test_args),
        patch("dat_session_cli.run_session", return_value=0) as mock_run,
    ):
        main()
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        assert args.api_key == "env_provided_key"


def test_cli_api_key_default_is_none_when_unset(monkeypatch):
    monkeypatch.delenv("API_KEY", raising=False)
    test_args = ["dat_session_cli.py", "run"]
    with (
        patch("sys.argv", test_args),
        patch("dat_session_cli.run_session", return_value=0) as mock_run,
    ):
        main()
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        assert args.api_key is None
