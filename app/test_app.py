#!/usr/bin/python
import unittest
import app


class TestJaccardSimilarity(unittest.TestCase):
    def test_jaccard_similarity(self):
        test_cases = [
            [
                "OK, and what's your order?",
                "I'm ready for your order.",
                0.25
            ],
            [
                "I'd like a medium supreme pizza.",
                "Can I get a pepperoni pizza, medium?",
                0.3
            ],
            [
                "Hi there, how can I help you?",
                "Hi there, how can I help you?",
                1.0
            ],
            [
                "Is your order for one large pizza?",
                "Thanks, please come again.",
                0.0
            ]
        ]

        for case in test_cases:
            s1, s2, expected_result = case
            self.assertEqual(
                app.jaccard_similarity(s1, s2),
                expected_result,
                f"Correct output is {expected_result}"
            )


class TestAppMethods(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_health(self):
        pass
        # self.assertRaises(ValueError, app.success())

    def test_detect_intent(self):
        """
        TEST CASES

        Input: "OK, your order is a large pizza and garlic bread."
        Output: "ConfirmItem"

        Input: "Ready in 30"
        Output: "DurationBeforePickupAnswer"
        """
        pass

    def tearDown(self) -> None:
        return super().tearDown()


if __name__ == '__main__':
    unittest.main()
