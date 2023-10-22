import pytest
import requests
import json

class TestCookie:
    def test_cookie(self):
        url = "https://playground.learnqa.ru/api/homework_cookie"
        response = requests.get(url)
        assert response.status_code == 200, 'Wrong response status code'
        expected_cookie = str(response.cookies)
        word = 'homework'
        assert word in expected_cookie.lower(), 'Incorrect cookie'
