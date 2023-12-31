import json.decoder
from datetime import datetime

from requests import Response
class BaseCase:
    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f"Cannot find cookie with name {cookie_name} in the last response"
        return response.cookies[cookie_name]

    def get_headers(self, response: Response, headers_name):
        assert headers_name in response.headers, f"Cannot find header with name {headers_name} in the last response"
        return response.headers[headers_name]

    def get_json_value(self, response: Response, name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response is not in JSON format. Response text is {response.text}"
        assert name in response_as_dict, f"Response JSON doesn't have key {name}"
        return response_as_dict[name]

    def prepare_registration_data(self, email=None):
        if email is None:
            base_part = 'learnqa'
            domain = 'example.com'
            random_part = datetime.now().strftime("%m%d%Y%H%M%S")
            email = f"{base_part}{random_part}@{domain}"
        return {'password': '123',
                'username': 'learnqa',
                'firstName': 'learnqa',
                'lastName': 'learnqa',
                'email': email}

    def prepare_registration_data_for_all_fields(self, variable):
        base_part = 'learnqa'
        domain = 'example.com'
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        email = f"{base_part}{random_part}@{domain}"
        if variable == 'email':
            return {'password': '123',
                    'username': 'learnqa',
                    'firstName': 'learnqa',
                    'lastName': 'learnqa',
                    'email': None}
        elif variable == 'password':
            return {'password': None,
                    'username': 'learnqa',
                    'firstName': 'learnqa',
                    'lastName': 'learnqa',
                    'email': email}
        elif variable == 'username':
            return {'password': '123',
                    'username': None,
                    'firstName': 'learnqa',
                    'lastName': 'learnqa',
                    'email': email}
        elif variable == 'firstName':
            return {'password': '123',
                    'username': 'learnqa',
                    'firstName': None,
                    'lastName': 'learnqa',
                    'email': email}
        else:
            return {'password': '123',
                    'username': 'learnqa',
                    'firstName': 'learnqa',
                    'lastName': None,
                    'email': email}


    def check_registration_parameters(self, password, username, firstName, lastName):
        base_part = 'learnqa'
        domain = 'example.com'
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        email = f"{base_part}{random_part}@{domain}"
        return {'password': password,
                'username': username,
                'firstName': firstName,
                'lastName': lastName,
                'email': email}