#!/usr/bin/python
import unittest
from app import create_app, jaccard_similarity


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
                jaccard_similarity(s1, s2),
                expected_result,
                f"Correct output is {expected_result}"
            )


class TestAppEndPoints(unittest.TestCase):
    def setUp(self) -> None:
        app = create_app()
        app.testing = True
        self.client = app.test_client()

    def test_health(self) -> None:
        response = self.client.get('/health')
        assert response.status_code == 200

    def test_detect_intent(self) -> None:
        test_cases = [
            {
                'data': {'message': 'OK, your order is a large pizza and garlic bread.'},
                'expected': 'ConfirmItem'
            },
            {
                'data': {'message': 'Ready in 30'},
                'expected': 'DurationBeforePickupAnswer'
            }
        ]
        for case in test_cases:
            response = self.client.post(
                '/detect_intent',
                data=case['data']
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.text, case['expected'])

        # failing case
        response = self.client.post('/detect_intent', data={'dumb': 'data'})
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.text, "'message' parameter not found, please supply.")


if __name__ == '__main__':
    unittest.main()
