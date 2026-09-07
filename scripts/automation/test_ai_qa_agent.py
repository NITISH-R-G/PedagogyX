import unittest
from unittest.mock import MagicMock, patch

import scripts.automation.ai_qa_agent as ai_qa_agent


class TestAIQAAgent(unittest.TestCase):
    def test_generate_qa_summary_api_error_fallback(self):
        reports = {"ruff": "Some ruff issue", "vulture": "", "gitleaks": "no leak"}
        api_key = "fake-api-key"

        mock_openai_cls = MagicMock()
        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client
        mock_client.chat.completions.create.side_effect = Exception("API connection failed")

        with patch.object(ai_qa_agent, "OpenAI", mock_openai_cls):
            summary = ai_qa_agent.generate_qa_summary(reports, api_key=api_key)

        self.assertIn("# AI-Powered QA & Security Insights (Fallback Generator)", summary)
        self.assertIn("Code Quality:** Ruff detected potential issues.", summary)
        self.assertIn("*(Note: LLM API error: API connection failed)*", summary)

    def test_generate_qa_summary_success(self):
        reports = {"ruff": ""}
        api_key = "fake-api-key"

        mock_openai_cls = MagicMock()
        mock_client = MagicMock()
        mock_openai_cls.return_value = mock_client

        mock_response = MagicMock()
        mock_choice = MagicMock()
        mock_choice.message.content = "AI Generated Summary Content"
        mock_response.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_response

        with patch.object(ai_qa_agent, "OpenAI", mock_openai_cls):
            summary = ai_qa_agent.generate_qa_summary(reports, api_key=api_key)

        self.assertEqual(summary, "AI Generated Summary Content")

    def test_generate_qa_summary_no_api_key(self):
        reports = {"ruff": "issue"}
        summary = ai_qa_agent.generate_qa_summary(reports, api_key=None)
        self.assertIn("# AI-Powered QA & Security Insights (Fallback Generator)", summary)
        self.assertNotIn("Note: LLM API error", summary)

    def test_generate_fallback_summary_findings(self):
        reports = {
            "ruff": "Found ruff errors",
            "vulture": "Found dead code",
            "gitleaks": "CRITICAL leak found",
        }
        summary = ai_qa_agent.generate_fallback_summary(reports)
        self.assertIn("Ruff detected potential issues", summary)
        self.assertIn("Vulture identified potential dead code", summary)
        self.assertIn("Critical secret leak detected", summary)

    def test_get_report_content(self):
        with (
            patch("os.path.exists", return_value=True),
            patch("builtins.open", unittest.mock.mock_open(read_data=" report data \n")),
        ):
            content = ai_qa_agent.get_report_content("dummy_path")
            self.assertEqual(content, "report data")

        with patch("os.path.exists", return_value=False):
            content = ai_qa_agent.get_report_content("nonexistent_path")
            self.assertEqual(content, "")


if __name__ == "__main__":
    unittest.main()
