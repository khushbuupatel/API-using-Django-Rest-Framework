import json
import pytest
import requests
import pandas as pd
from django.db import connection
from datetime import date
from scripts import django_setup


BASE_URL = "http://127.0.0.1:8000/"
USERNAME = 'tlk'
PASSWORD = 'tlk12345'


def get_correlation_data(correlation):
    """
    This function calculates the correlation of the columns of Product model

    :param correlation: pearson / spearman
    :return: dict
    """
    # connect with the Product sqlite database
    with connection.cursor() as cursor:

        # execute the query to get all the rows from Product db
        cursor.execute("SELECT * FROM 'analysis_product'")

        # create a dictionary with column names as description and cells as it values
        columns = [col[0] for col in cursor.description]
        product_dict = [
            dict(zip(columns, row)) for row in cursor.fetchall()
        ]

        # convert dictionary into df
        product_df = pd.DataFrame(product_dict)

        # calculate correlation based on parameter passed
        if correlation.lower() == 'spearman':
            corr_df = product_df.corr(method="spearman")
        elif correlation.lower() == 'pearson':
            corr_df = product_df.corr()
        else:
            return {'error': correlation + ' is invalid Correlation method'}

        # convert df to dict and return
        return corr_df.to_dict()


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
            else:
                self.token = ""

    return AuthParas()


def test_get_product(auth_paras):
    """
    This test case verifies if the Products are listed when user sends a GET request
    :param auth_paras: object of pytest fixture to access the Authentication Token
    """
    url = BASE_URL + 'products'
    headers = {
        'Authorization': 'Token ' + auth_paras.token
    }

    # send a GET request and convert the response text into dict
    response = requests.get(url=url, headers=headers)
    _dict = json.loads(response.text)

    # verify if the count value in the _dict is greater than 0
    if 'count' in _dict.keys():
        if _dict['count'] > 0:
            assert True
            return

    assert False


def test_add_product(auth_paras):
    """
    This test case verifies if the new Product is added when user sends a POST request
    :param auth_paras: object of pytest fixture to access the Authentication Token
    """
    url = BASE_URL + 'products/'
    headers = {
        'Authorization': 'Token ' + auth_paras.token
    }

    # send a get request and obtain the total count before adding a new product
    before_count = int(json.loads(requests.get(url=url, headers=headers).text)['count'])

    data = {
        "date_w": "2016-12-17", "price": 1.35, "total_vol": 11111, "plu1": 11111, "plu2": 11111,
        "plu3": 11, "bags_t": 111, "bags_s": 1111, "bags_l": 1111, "bags_lx": 0.0, "type": "A",
        "year": 2019, "location": "NewYork"
    }
    # send a POST request to add a new Product
    requests.post(url=url, data=data, headers=headers)

    # send a get request and obtain the total count after adding a new product
    after_count = int(json.loads(requests.get(url=url, headers=headers).text)['count'])

    # assert true if after count is incremented by 1 else false
    if before_count + 1 == after_count:
        assert True
    else:
        assert False


def test_update_product(auth_paras):
    """
    This test case verifies if the Product details are updated when user sends a PATCH request
    :param auth_paras: object of pytest fixture to access the Authentication Token
    """
    url = BASE_URL + 'products/'
    headers = {
        'Authorization': 'Token ' + auth_paras.token
    }

    # send a get request to get the ID of product to be updated and the date_w value before update
    _dict = json.loads(requests.get(url=url, headers=headers).text)

    product_id = str(_dict['results'][0]['id'])
    before_update = _dict['results'][0]['date_w']

    # send a PATCH request to to update the date_w with today's data for the product
    url = BASE_URL + 'products/' + product_id + "/"
    data = {
        "date_w": {date.today()}
    }
    requests.patch(url=url, data=data, headers=headers)

    # send a get request using the product id url and get the date_w
    after_update = json.loads(requests.get(url=url, headers=headers).text)['date_w']

    # assert False if both the date values are same after update
    if before_update == after_update:
        assert False
    else:
        assert True


def test_delete_product(auth_paras):
    """
    This test case verifies if the Product is deleted when user sends a DELETE request
    :param auth_paras: object of pytest fixture to access the Authentication Token
    """
    headers = {
            'Authorization': 'Token ' + auth_paras.token
    }

    url = BASE_URL + 'products/'

    # send a get request to get the ID of product to be deleted and the total count of products
    _dict = json.loads(requests.get(url=url, headers=headers).text)

    before_count = _dict['count']
    product_id = str(_dict['results'][0]['id'])

    # send a DELETE request with id of the product to be deleted
    delete_url = BASE_URL + 'products/' + product_id + "/"
    requests.delete(url=delete_url, headers=headers)

    # send a get request to get  total count of products
    after_count = int(json.loads(requests.get(url=url, headers=headers).text)['count'])

    # assert True if the after count is reduced by 1
    if before_count - 1 == after_count:
        assert True
    else:
        assert False


def test_not_found_product(auth_paras):
    """
    This test case verifies if the http code 404 is returned if an invalid id is present
    :param auth_paras: object of pytest fixture to access the Authentication Token
    """
    headers = {
        'Authorization': 'Token ' + auth_paras.token
    }

    # send a GET request using invalid id
    url = BASE_URL + 'products/abc'
    response = requests.get(url=url, headers=headers)

    # assert True if Http code 404 not found is returned
    if response.status_code == 404:
        assert True
    else:
        assert False


correlation_methods = ['pearson', 'spearman']


@pytest.mark.parametrize("correlation_method", correlation_methods)
def test_correlation_methods(auth_paras, correlation_method):
    """
    This test case verifies if correct correlation matrix is returned for query parameter PEARSON/SPEARMAN
    :param auth_paras: object of pytest fixture to access the Authentication Token
    :param correlation_method: correlation method parameter list
    """
    headers = {
        'Authorization': 'Token ' + auth_paras.token
    }

    # send a GET request with query parameter correlation
    url = BASE_URL + 'analysis/?correlation=' + correlation_method
    response = json.loads(requests.get(url=url, headers=headers).text)

    # calculate the correlation by calculating it on the product
    corr_dict = get_correlation_data(correlation_method)

    # assert True if both the dict are equal
    if response == corr_dict:
        assert True
        return

    assert False


def test_invalid_correlation_method(auth_paras):
    """
    This test case verifies that HTTP 400 code is returned if invalid correlation method is passed
    :param auth_paras: object of pytest fixture to access the Authentication Token
    """
    headers = {
        'Authorization': 'Token ' + auth_paras.token
    }

    # send a GET request with invalid correlation value
    url = BASE_URL + 'analysis/?correlation=abc'
    response = requests.get(url=url, headers=headers)

    # assert True if 400 code is returned
    if response.status_code == 400:
        assert True
        return

    assert False


def test_missing_correlation_param(auth_paras):
    """
    This test case verifies that HTTP 400 code is returned if correlation query param is not passed
    :param auth_paras: object of pytest fixture to access the Authentication Token
    """
    headers = {
        'Authorization': 'Token ' + auth_paras.token
    }

    # send a GET request with missing correlation param
    url = BASE_URL + 'analysis/'
    response = requests.get(url=url, headers=headers)

    # assert True if 400 code is returned
    if response.status_code == 400:
        assert True
        return

    assert False
