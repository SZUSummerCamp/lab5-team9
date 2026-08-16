"""Router tests: the right message reaches the right skill."""

from __future__ import annotations

import unittest

from app.runtime.router import route


class RoutingTests(unittest.TestCase):
    def test_campus_keyword_routes_to_campus(self) -> None:
        result = route("What is the university motto?")
        self.assertEqual(result.skill_name, "campus")

    def test_library_keyword_routes_to_library(self) -> None:
        result = route("Where is the library?")
        self.assertEqual(result.skill_name, "library")

    def test_translation_keyword_routes_to_translation(self) -> None:
        result = route("Translate this to Chinese")
        self.assertEqual(result.skill_name, "translation")

    def test_unmatched_routes_to_unknown(self) -> None:
        result = route("What is the weather today?")
        self.assertEqual(result.skill_name, "unknown")
        self.assertEqual(result.status, "unmatched")

    def test_chinese_keyword_routes_to_translation(self) -> None:
        result = route("翻译一下")
        self.assertEqual(result.skill_name, "translation")


if __name__ == "__main__":
    unittest.main()
