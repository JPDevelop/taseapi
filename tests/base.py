import time
import unittest
from datetime import datetime
from random import randint
from typing import Any

import requests_mock

from tests.mock_authenticator import MockAuthenticator


class BaseTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.m_requests = requests_mock.Mocker(case_sensitive=True)
        self.m_requests.start()
        self.mock_authenticator = MockAuthenticator()
        self.base_url = "https://openapigw.tase.co.il/tase/prod/api/v1"
        self.mock_response = {"response": "mock"}
        self.lang = "mock-language"

    def _mock_uri(self, path: str, status: int = 200) -> None:
        self.m_requests.register_uri(
            "GET",
            f"{self.base_url}/{path}",
            json=self.mock_response,
            status_code=status,
        )

    def _random_int(self) -> int:
        return randint(1, 9999)

    def _random_date(self) -> datetime:
        d = randint(1, int(time.time()))
        return datetime.fromtimestamp(d)

    def _random_date_string(self) -> str:
        return self._random_date().strftime("%Y-%m-%d")

    def assertApiRequestHeaders(self, request):
        self.assertEqual(
            "Bearer " + self.mock_authenticator.get_access_token(),
            request.headers["Authorization"],
        )
        self.assertEqual(self.lang, request.headers["Accept-Language"])

    def assertQueryParams(self, request, params: dict[str, Any]):
        if not params:
            self.assertEqual(request.query, "")
            return
        params_list = [f"{item}={params[item]}" for item in params]
        self.assertCountEqual(request.query.split("&"), params_list)
