"""Skill tests: skills shape the SkillResult correctly with the model mocked out."""

from __future__ import annotations

import unittest
from unittest.mock import patch

from app.skills import campus, translation


class CampusSkillTests(unittest.TestCase):
    def test_campus_skill_returns_success(self) -> None:
        with patch("app.skills.campus.call_llm", return_value="1983"):
            result = campus.handle("When was SZU founded?")
        self.assertEqual(result.status, "success")
        self.assertEqual(result.response, "1983")

    def test_skill_returns_error_on_llm_failure(self) -> None:
        with patch("app.skills.campus.call_llm", side_effect=Exception("LLM down")):
            result = campus.handle("anything")
        self.assertEqual(result.status, "error")


class TranslationSkillTests(unittest.TestCase):
    def test_translation_skill_does_not_use_knowledge(self) -> None:
        with patch("app.skills.translation.call_llm", return_value="你好") as mocked:
            result = translation.handle("Translate hello")
        self.assertEqual(result.skill_name, "translation")
        self.assertEqual(result.response, "你好")
        # The raw message is forwarded: no knowledge context is prepended.
        mocked.assert_called_once()
        self.assertEqual(mocked.call_args.args[1], "Translate hello")


if __name__ == "__main__":
    unittest.main()
