# apps/core/tests/test_views.py
from django.test import TestCase
from django.urls import reverse

class HealthCheckTests(TestCase):
    def test_health_endpoint(self):
        response = self.client.get(reverse('health-check'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "status": "ok",
            "services": {
                "database": "connected",
                "cache": "enabled"
            }
        })