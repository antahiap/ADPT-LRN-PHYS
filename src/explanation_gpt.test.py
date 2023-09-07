import unittest
from unittest.mock import patch, Mock
from explanation_gpt import ExplanationGPT


class TestExplanationGPT(unittest.TestCase):
    def setUp(self):
        self.topic = "test topic"
        self.context = "test context"
        self.explanation = "test explanation"
        self.explanation_gpt = ExplanationGPT(self.topic, self.explanation, self.context)

    def test_fill_from_db(self):
        explanation = "Random explanation"
        with patch("explanation_gpt.keyword_db.select", return_value=[(1, self.topic, explanation, ["test1", "test2"])]) as mock_select:
            self.explanation_gpt.fill_from_db()
            mock_select.assert_called_once_with(self.topic)
            self.assertEqual(self.explanation_gpt.keywords, {"test1", "test2"})
            self.assertEqual(self.explanation_gpt.explanation, explanation)

    def test_generate_info(self):
        with patch.object(self.explanation_gpt, "generate_explanation") as mock_generate_explanation, \
             patch.object(self.explanation_gpt, "find_keywords") as mock_find_keywords, \
             patch.object(self.explanation_gpt, "fill_explanation_from_db") as mock_fill_explanation_from_db, \
             patch.object(self.explanation_gpt, "explain_keywords") as mock_explain_keywords:
            self.explanation_gpt.explanation = None
            self.explanation_gpt.generate_info()
            mock_generate_explanation.assert_called_once()
            mock_find_keywords.assert_called_once()
            mock_fill_explanation_from_db.assert_called_once()
            mock_explain_keywords.assert_called_once()

    def test_generate_explanation(self):
        with patch.object(self.explanation_gpt.api, "call_api", return_value=(self.explanation, None, None)) as mock_call_api, \
            patch("explanation_gpt.keyword_db.insert_explanation") as mock_insert:
            self.explanation_gpt.generate_explanation()
            mock_call_api.assert_called_once_with(self.explanation_gpt.explanation_prompt("", self.context))
            mock_insert.assert_called_once_with(self.topic, self.explanation)

    def test_parse_keywords(self):
        raw_keywords = "[\"keyword1\", \"keyword2\"]"
        expected_keywords = ["keyword1", "keyword2"]
        keywords = self.explanation_gpt._parse_keywords(raw_keywords)
        self.assertEqual(keywords, expected_keywords)

    def test_find_keywords(self):
        with patch.object(self.explanation_gpt.api, "call_api", return_value=("[\"keyword1\", \"keyword2\"]", None, None)) as mock_call_api, \
             patch.object(self.explanation_gpt, "_parse_keywords", return_value=["keyword1", "keyword2"]) as mock_parse_keywords, \
             patch("explanation_gpt.keyword_db.update_keywords") as mock_update:
            self.explanation_gpt.find_keywords()
            mock_call_api.assert_called_once_with(f"What are the 5 most important keywords of the text. Answer in a python array: \n{self.explanation}\n", model="gpt-3.5-turbo")
            mock_parse_keywords.assert_called_once_with("[\"keyword1\", \"keyword2\"]")
            mock_update.assert_called_once_with(self.topic, {"keyword1", "keyword2"})
            self.assertEqual(self.explanation_gpt.keywords, {"keyword1", "keyword2"})

    def test_setup_explanation(self):
        keyword = "test keyword"
        explanation = "test explanation"
        self.explanation_gpt.keywords = {keyword}
        self.explanation_gpt.setup_explanation(keyword, explanation)
        self.assertIsInstance(self.explanation_gpt.keywords_explanations[keyword], ExplanationGPT)

    def test_fill_explanation_from_db(self):
        keyword = "test Keyword"
        explanation = "test explanation"
        self.explanation_gpt.keywords = {keyword}
        with patch("explanation_gpt.keyword_db.select_multi", return_value=[(1, keyword.upper(), explanation)]) as mock_select, \
             patch.object(self.explanation_gpt, "setup_explanation") as mock_setup_explanation:
            self.explanation_gpt.fill_explanation_from_db()
            mock_select.assert_called_once_with(self.explanation_gpt.keywords)
            mock_setup_explanation.assert_called_once_with(keyword.upper(), explanation)
            self.assertEqual(self.explanation_gpt.keywords, set())

    def test_add_explanation(self):
        keyword = "test keyword"
        explanation = "test explanation"
        result = Mock(metadata={"keyword": keyword}, response={'choices': [{'message': {'content': explanation}}]})
        with patch("explanation_gpt.keyword_db.insert_explanation") as mock_insert, \
             patch.object(self.explanation_gpt, "setup_explanation") as mock_setup_explanation:
            self.explanation_gpt.add_explanation(result)
            mock_insert.assert_called_once_with(keyword, explanation)
            mock_setup_explanation.assert_called_once_with(keyword, explanation)

    def test_explain_keywords(self):
        self.explanation_gpt.keywords = {"test keyword"}
        with patch.object(self.explanation_gpt, "explanation_prompt", return_value="test prompt") as mock_explanation_prompt, \
             patch("explanation_gpt.OpenAIMultiClient.request") as mock_request, \
             patch("explanation_gpt.OpenAIMultiClient.__init__", return_value=None), \
             patch("explanation_gpt.OpenAIMultiClient.__next__", side_effect=["test"]), \
             patch.object(self.explanation_gpt, "add_explanation") as mock_add_explanation:
            self.explanation_gpt.explain_keywords()
            mock_explanation_prompt.assert_called_once_with("test keyword", self.explanation)
            mock_request.assert_called_once_with(
                data={"messages": [{"role": "user", "content": "test prompt"}]},
                metadata={'id': 0, 'keyword': "test keyword"})
            mock_add_explanation.assert_called_once_with("test")

    def test_format_explanation_short(self):
        explanation = "This is a short explanation."
        formatted_explanation = self.explanation_gpt._format_explanation(explanation)
        self.assertEqual(formatted_explanation, explanation)

    def test_format_explanation_new_line(self):
        explanation = "This is a short explanation\nwith a new line."
        formatted_explanation = self.explanation_gpt._format_explanation(explanation)
        self.assertEqual(formatted_explanation,  "This is a short explanation<br>with a new line.")

    def test_format_explanation_long(self):
        explanation = "This is a long explanation that is over 100 characters long. It should be truncated to 100 characters and have an ellipsis added to the end."
        explanation_gpt = ExplanationGPT("test")
        formatted_explanation = explanation_gpt._format_explanation(explanation)
        self.assertEqual(len(formatted_explanation), 103)
        self.assertEqual(formatted_explanation[-3:], "...")

    def test_to_html(self):
        tooltip_class = "test-tooltip"
        tooltip_text_class = "test-tooltip-text"
        self.explanation_gpt.explanation = "test explanation"
        self.explanation_gpt.keywords_explanations = {"keyword1": Mock(explanation="test explanation 1"), "keyword2": Mock(explanation="test explanation 2")}
        expected_html = "test explanation"
        expected_html = expected_html.replace("keyword1", f'<span class="{tooltip_class}">keyword1<span class="{tooltip_text_class}">test explanation 1</span></span>')
        expected_html = expected_html.replace("keyword2", f'<span class="{tooltip_class}">keyword2<span class="{tooltip_text_class}">test explanation 2</span></span>')
        self.explanation_gpt.to_html(tooltip_class, tooltip_text_class)
        self.assertEqual(self.explanation_gpt.html, expected_html)


if __name__ == "__main__":
    unittest.main()