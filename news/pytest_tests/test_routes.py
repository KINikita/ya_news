from django.test import Client

import pytest
from pytest_django.asserts import assertRedirects
from pytest_lazyfixture import lazy_fixture as lf

from news.pytest_tests.pytest_parts.constants import STATUSES

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'url_name, client, expected_status',
    [
        (lf('home_url'), Client(), '200'),
        (lf('login_url'), Client(), '200'),
        (lf('logout_url'), Client(), '200'),
        (lf('signup_url'), Client(), '200'),
        (lf('detail_url'), Client(), '200'),

        (lf('edit_url'), lf('not_author_client'), '404'),
        (lf('edit_url'), lf('author_client'), '200'),
        (lf('delete_url'), lf('not_author_client'), '404'),
        (lf('delete_url'), lf('author_client'), '200'),
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
    test_client = client
    response = test_client.get(url_name)
    assert response.status_code == STATUSES[expected_status]


@pytest.mark.parametrize(
    'url_name',
    [
        lf('edit_url'),
        lf('delete_url'),
    ],
)
def test_redirects_for_anonymous_client(login_url, client, url_name):
    """Тест перенаправления на страницу логина для анонимного пользователя."""
    expected_url = f'{login_url}?next={url_name}'
    response = client.get(url_name)
    assertRedirects(response, expected_url)
