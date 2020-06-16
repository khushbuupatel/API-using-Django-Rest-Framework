import json
import pytest
import requests

BASE_URL = "http://127.0.0.1:8000/"

# user credentials
USERNAME = 'tlk'
PASSWORD = 'tlk12345'
NEW_PASSWORD = '12345tlk'


@pytest.fixture(scope="module", name="auth_paras")
def get_auth_paras():
    """
    This is a pytest fixture which will be executed once per module and
    perform the steps to login the user and returns the Authentication token
    :return: Authentication token
    """
    class AuthParas:
        def __init__(self):
            url = BASE_URL + 'login'
            data = {
                'username': USERNAME,
                'password': PASSWORD
            }
            kwargs = {
                "url": url,
                "data": data
            }
            # send post request with above keywords arguments
            response = requests.post(**kwargs)

            # return the authentication token
            if response.status_code == 200:
                _dict = json.loads(response.text)
                if 'token' in _dict.keys():
                    self.token = _dict['token']

    return AuthParas()


def test_wrong_password(auth_paras):
    """
    Test case to test that the password is not changed if the user enters incorrect current password
    :param auth_paras: object of pytest fixture to access the Authentication Token
    :return:
    """
    url = BASE_URL + 'password/'
    headers = {
        'Authorization': 'Token ' + auth_paras.token
    }
    data = {
        'username': USERNAME,
        'password': NEW_PASSWORD,
        'new_password': PASSWORD
    }
    kwargs = {
        "url": url,
        "data": data,
        "headers": headers
    }

    # send put request using above keyword arguments and assert true if http code 400 is returned
    response = requests.put(**kwargs)
    if response.status_code == 400:
        print("Successfully verified that password cannot be changed if current password is incorrect!")
        assert True
        return

    assert False


def test_empty_credentials(auth_paras):
    """
    Test case to test that the password is not changed if the user fails to enter value for any of the three fields
    :param auth_paras: object of pytest fixture to access the Authentication Token
    :return:
    """
    url = BASE_URL + 'password/'
    headers = {
        'Authorization': 'Token ' + auth_paras.token
    }
    data = {
        'username': USERNAME,
        'password': PASSWORD,
        'new_password': ''
    }
    kwargs = {
        "url": url,
        "data": data,
        "headers": headers
    }

    # send put request using above keyword arguments and assert true if http code 400 is returned
    response = requests.put(**kwargs)
    if response.status_code == 400:
        print("Successfully verified that password cannot be changed if any of the field is empty!")
        assert True
        return

    assert False


def test_same_passwords(auth_paras):
    """
    Test case to test that the old and new password cannot be same
    :param auth_paras: object of pytest fixture to access the Authentication Token
    :return:
    """
    url = BASE_URL + 'password/'
    headers = {
        'Authorization': 'Token ' + auth_paras.token
    }
    data = {
        'username': USERNAME,
        'password': PASSWORD,
        'new_password': PASSWORD
    }
    kwargs = {
        "url": url,
        "data": data,
        "headers": headers
    }

    # send put request using above keyword arguments and assert true if http code 400 is returned
    response = requests.put(**kwargs)
    if response.status_code == 400:
        print("Successfully verified that password cannot be changed if both old and new password are same!")
        assert True
        return

    assert False


def test_change_password(auth_paras):
    """
    Test case to test that the password is changed if valid details are entered by user
    :param auth_paras: object of pytest fixture to access the Authentication Token
    :return:
    """
    url = BASE_URL + 'password/'
    headers = {
        'Authorization': 'Token ' + auth_paras.token
    }
    data = {
        'username': USERNAME,
        'password': PASSWORD,
        'new_password': NEW_PASSWORD
    }

    # send a put request to change the password
    requests.put(url=url, data=data, headers=headers)

    # send a post request to logout
    url = BASE_URL + 'logout'
    requests.post(url=url, headers=headers)

    data = {
        'username': USERNAME,
        'password': NEW_PASSWORD
    }
    url = BASE_URL + 'login'

    # send a post request to login again with the new password
    response = requests.post(url=url, data=data)

    # assert True if login is successful
    if response.status_code == 200:
        print("Successfully changed the password!")
        assert True
        return

    assert False
