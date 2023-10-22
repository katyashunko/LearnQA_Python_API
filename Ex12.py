import requests

class TestCookie:
    def test_cookie(self):
        url = "https://playground.learnqa.ru/api/homework_header"
        response = requests.get(url)
        assert response.status_code == 200, 'Wrong response status code'
        expected_headers = str(response.headers)
        word = 'homework'
        assert word in expected_headers.lower(), 'Incorrect header'
