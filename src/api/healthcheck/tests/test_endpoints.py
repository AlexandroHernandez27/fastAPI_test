import unittest

from fastapi import status
from fastapi.testclient import TestClient

from core.settings import settings
from main import app


class TestHelathcheckEndpoints(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app)

    def test_healthcheck(self):
        url = "/health-check"
        response = self.client.get(url)

        body = response.json().get("body")
        expected_keys = ["links", "count", "results"]

        results = body.get("results")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(list(body.keys()), expected_keys)
        self.assertEqual(results.get("detail"), settings.PROJECT_NAME)
        self.assertEqual(results.get("version"), settings.VERSION)
