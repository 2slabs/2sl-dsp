"""Templates filled in by marker (twosl_dsp/generated_scripts.py)."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from twosl_dsp.build_error import BuildError  # noqa: E402
from twosl_dsp.generated_scripts import fill_template, kit_template_text  # noqa: E402


class FillTemplateTests(unittest.TestCase):
    def test_every_marker_is_filled_once_over(self):
        filled = fill_template("var A = /*A*/; var B = /*B*/; // /* not a marker */", {"A": "1", "B": "'/*A*/'"}, "t")
        self.assertEqual(filled, "var A = 1; var B = '/*A*/'; // /* not a marker */",
                         "text filled in is not searched for markers again")

    def test_a_marker_the_template_lacks_fails(self):
        with self.assertRaisesRegex(BuildError, r"t has no marker for /\*C\*/"):
            fill_template("/*A*/", {"A": "1", "C": "3"}, "t")

    def test_a_marker_left_unfilled_fails(self):
        with self.assertRaisesRegex(BuildError, r"markers nothing fills: /\*B\*/"):
            fill_template("/*A*/ /*B*/", {"A": "1"}, "t")

    def test_the_kit_templates_exist(self):
        for name in ("transport-clock.template.js", "chord-block.template.js", "stored-table.template.js"):
            self.assertTrue(kit_template_text(name))
        with self.assertRaisesRegex(BuildError, "no template"):
            kit_template_text("nope.js")


if __name__ == "__main__":
    unittest.main(verbosity=2)
