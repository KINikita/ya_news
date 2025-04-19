from http import HTTPStatus

from django.test import Client

import pytest
from pytest_django.asserts import assertRedirects

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'url_name, client, expected_status',
    [
        (pytest.lazy_fixture('home_url'), None, HTTPStatus.OK),
        (pytest.lazy_fixture('login_url'), None, HTTPStatus.OK),
        (pytest.lazy_fixture('logout_url'), None, HTTPStatus.OK),
        (pytest.lazy_fixture('signup_url'), None, HTTPStatus.OK),
        (pytest.lazy_fixture('detail_url'), None, HTTPStatus.OK),

        (pytest.lazy_fixture('edit_url'), pytest.lazy_fixture(
            'not_author_client'), HTTPStatus.NOT_FOUND),
        (pytest.lazy_fixture('edit_url'), pytest.lazy_fixture(
            'author_client'), HTTPStatus.OK),
        (pytest.lazy_fixture('delete_url'), pytest.lazy_fixture(
            'not_author_client'), HTTPStatus.NOT_FOUND),
        (pytest.lazy_fixture('delete_url'),
         pytest.lazy_fixture('author_client'), HTTPStatus.OK),
    ],
    ids=[
        'home page - anonymous',
        'login page - anonymous',
        'logout page - anonymous',
        'signup page - anonymous',
        'news detail - anonymous',
        'edit comment - not author',
        'edit comment - author',
        'delete comment - not author',
        'delete comment - author',
    ]
)
def test_pages_availability(client, url_name, expected_status, comment):
    """
    Тест доступности страниц для разных типов пользователей.
    Если client=None, используется анонимный клиент из параметра.
    """
    test_client = client if client is not None else Client()
    response = test_client.get(url_name)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'url_name',
    [
        pytest.lazy_fixture('edit_url'),
        pytest.lazy_fixture('delete_url'),
    ],
)
def test_redirects_for_anonymous_client(login_url, client, url_name):
    """Тест перенаправления на страницу логина для анонимного пользователя."""
    expected_url = f'{login_url}?next={url_name}'
    response = client.get(url_name)
    assertRedirects(response, expected_url)
