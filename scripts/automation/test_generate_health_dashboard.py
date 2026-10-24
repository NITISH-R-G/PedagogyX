from unittest.mock import patch, MagicMock
from generate_health_dashboard import run_command, gather_real_metrics

def test_run_command_list_args():
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(stdout="  hello world  \n", returncode=0)
        output, code = run_command(["echo", "hello world"])

        mock_run.assert_called_once_with(["echo", "hello world"], capture_output=True, text=True, cwd=None)
        assert output == "hello world"
        assert code == 0

def test_run_command_str_arg_tokenized():
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(stdout="test output", returncode=0)
        output, code = run_command("git rev-list --count HEAD")

        mock_run.assert_called_once_with(["git", "rev-list", "--count", "HEAD"], capture_output=True, text=True, cwd=None)
        assert output == "test output"
        assert code == 0

def test_run_command_exception():
    with patch("subprocess.run", side_effect=Exception("Failed execution")):
        output, code = run_command(["invalid_cmd"])
        assert code == 1
        assert "Failed execution" in output

def test_gather_real_metrics_executes_safely():
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(stdout="0", returncode=0)
        data = gather_real_metrics()
        assert "executive_overview" in data
        assert "overall_health_score" in data["executive_overview"]
