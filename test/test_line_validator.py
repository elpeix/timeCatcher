import unittest

from src.timecatcher import LineValidator


class LineValidatorTest(unittest.TestCase):

    def test_is_not_valid(self):
        wrong_values = [
            None,
            1,
            1.0,
            True,
            False,
            [],
            {},
            "",
            " ",
            "12:00",
            "12:00 ",
            " 12:00",
            "Start",
            "1200 Start",
            "12:00Start",
            ":00 Start",
            "12:Start",
            "-1:00 Start",
            "12:-1 Start",
            "12:60 Start",
            "24:00 Start",
        ]
        for wrong_value in wrong_values:
            line_validator = LineValidator(wrong_value)
            self.assertFalse(
                line_validator.is_valid(),
                msg=f"Value [{wrong_value}] should not be valid")

    def test_is_valid(self):
        valid_values = [
            "12:00 Start",
            "12:00  Start",
            "12:00 Start ",
            "12:00  Start ",
            "12:00  Start with spaces",
            "12:00 *Start",
        ]
        for valid_value in valid_values:
            line_validator = LineValidator(valid_value)
            self.assertTrue(
                line_validator.is_valid(),
                msg=f"Value [{valid_value}] should be valid")
