import unittest

from theme import THEMES


class ThemeTests(unittest.TestCase):
    def test_all_palettes_define_the_required_tokens(self):
        required = {"background", "surface", "surface_alt", "border", "text", "muted", "accent"}
        for name, palette in THEMES.items():
            with self.subTest(theme=name):
                self.assertTrue(required <= palette.keys())
                self.assertTrue(all(value.startswith("#") for value in palette.values()))

    def test_graphite_is_the_default_visual_direction(self):
        self.assertEqual(THEMES["graphite"]["background"], "#10151d")
        self.assertEqual(THEMES["graphite"]["accent"], "#68a9ff")


if __name__ == "__main__":
    unittest.main()
