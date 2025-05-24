# File: apps/users/tests/test_views.py
from django.test import TestCase

class RateLimitTests(TestCase):
    def test_login_rate_limiting(self):
        for _ in range(4):
            response = self.client.post("/api/auth/login/", {
                "username": "test",
                "password": "wrong"
            })
        self.assertEqual(response.status_code, 429)