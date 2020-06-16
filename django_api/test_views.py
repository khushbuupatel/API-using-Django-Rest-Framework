"""
Purpose: Data types used in DataDisca applications are defined here

Developers:
<Khushbu Patel>

Sponsor: DataDisca Pty Ltd. Australia
https://github.com/DataDisca
"""
import json
import pytest
import requests
from time import sleep

BASE_URL = "http://127.0.0.1:8000/"
USERNAME = 'tlk'
PASSWORD = 'tlk12345'


@pytest.fixture(scope="module", name="auth_paras")
def get_auth_paras():
    class AuthParas:
        def __init__(self):
            self.token = None

    return AuthParas()


def test_login(auth_paras):
    url = BASE_URL + 'login'
    data = {
        'username': USERNAME,
        'password': PASSWORD
    }
    kwargs = {
        "data": data
    }
    response = requests.post(url=url, **kwargs)
    if response.status_code == 200:
        _dict = json.loads(response.text)
        if 'token' in _dict.keys():
            auth_paras.token = _dict['token']
            if len(auth_paras.token) > 0:
                assert True
                return

    assert False


def test_items(auth_paras):
    url = BASE_URL + 'items/'
    headers = {
        'Authorization': 'Token ' + auth_paras.token
    }
    kwargs = {
        "headers": headers
    }
    response = requests.get(url=url, **kwargs)
    _dict = json.loads(response.text)
    if 'count' in _dict.keys():
        if _dict['count'] > 0:
            assert True
            return

    assert False


sleep_times = [0, 2, 15]
# sleep_times = [0]


@pytest.mark.parametrize("sleep_time", sleep_times)
def test_check_auth(auth_paras, sleep_time):
    print(sleep_time)
    sleep(sleep_time)
    url = BASE_URL + 'check_auth'
    headers = {
        'Authorization': 'Token ' + auth_paras.token
    }
    kwargs = {
        "headers": headers
    }
    response = requests.post(url=url, **kwargs)
    if response.status_code == 200:
        print("Authorised")
        assert True
        return
    elif response.status_code == 401:
        print("Unauthorised")
        assert True
        return
    else:
        assert False


def test_logout(auth_paras):
    test_login(auth_paras)
    url = BASE_URL + 'logout'
    headers = {
        'Authorization': 'Token ' + auth_paras.token
    }
    kwargs = {
        "headers": headers
    }
    response = requests.post(url=url, **kwargs)
    if response.status_code == 200:
        print("Logged Out")
        assert True
        return
    assert False
