import pytest
import requests
import json

class TestUserAgent:
    @pytest.mark.parametrize(("user_agent, expected_values"), [("Mozilla/5.0  Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F   AppleWebKit/534.30  KHTML, like Gecko   Version/4.0 Mobile Safari/534.30", "'platform': 'Mobile', 'browser': 'No', 'device': 'Android'"),
        ("Mozilla/5.0  iPad; CPU OS 13_2 like Mac OS X   AppleWebKit/605.1.15  KHTML, like Gecko   CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1", "'platform': 'Mobile', 'browser': 'Chrome', 'device': 'iOS'"),
        ("Mozilla/5.0  compatible; Googlebot/2.1; +http://www.google.com/bot.html", "'platform': 'Googlebot', 'browser': 'Unknown', 'device': 'Unknown'"),
        ("Mozilla/5.0  Windows NT 10.0; Win64; x64   AppleWebKit/537.36  KHTML, like Gecko   Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0", "'platform': 'Web', 'browser': 'Chrome', 'device': 'No'"),
        ("Mozilla/5.0  iPad; CPU iPhone OS 13_2_3 like Mac OS X   AppleWebKit/605.1.15  KHTML, like Gecko   Version/13.0.3 Mobile/15E148 Safari/604.1", "'platform': 'Mobile', 'browser': 'No', 'device': 'iPhone'")])
    def test_user_agent(self, user_agent, expected_values):
        url = "https://playground.learnqa.ru/ajax/api/user_agent_check"
        data = {"User-Agent": user_agent, "expected_values": expected_values}
        response = requests.get(url, headers={"User-Agent": data["User-Agent"]})
        assert response.status_code == 200, 'Wrong status code'
        response_dict = response.json()
        device = response_dict["device"]
        platform = response_dict["platform"]
        browser = response_dict["browser"]
        actual_response_text = f"'platform': '{platform}', 'browser': '{browser}', 'device': '{device}'"
        expected_response_text = data["expected_values"]
        assert actual_response_text == expected_response_text, f"{actual_response_text} is not equal to {expected_response_text}"
