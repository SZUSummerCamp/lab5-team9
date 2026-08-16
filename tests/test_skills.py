"""Skill tests: skills expose the expected shape without calling the model."""

from __future__ import annotations

import unittest

from app.shared import SkillResult
from app.skills import campus, translation


class SkillStructureTests(unittest.TestCase):
    def test_campus_skill_handle_exists(self) -> None:
        self.assertTrue(callable(campus.handle))

    def test_translation_skill_handle_exists(self) -> None:
        self.assertTrue(callable(translation.handle))

    def test_skill_result_has_correct_fields(self) -> None:
        result = SkillResult(
            skill_name="campus",
            response="test",
            status="success",
            duration=0.1,
        )
        self.assertEqual(result.skill_name, "campus")
        self.assertEqual(result.response, "test")
        self.assertEqual(result.status, "success")
        self.assertEqual(result.duration, 0.1)


if __name__ == "__main__":
    unittest.main()
