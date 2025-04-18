from http import HTTPStatus
import pytest
from pytest_django.asserts import assertRedirects
from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.parametrize(
    'url_name, news_object',
    [
        ('news:home', None),
        ('users:login', None),
        ('users:logout', None),
        ('users:signup', None),
        ('news:detail', pytest.lazy_fixture('news')),
    ],
    ids=[
        'home page',
        'login page',
        'logout page',
        'signup page',
        'news detail page',
    ]
)
def test_pages_availability_for_anonymous_user(client, url_name, news_object):
    """Тест доступности страниц для анонимного пользователя."""
    if news_object is not None:
        url = reverse(url_name, args=(news_object.id,))
    else:
        url = reverse(url_name)

    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'client, expected_status',
    [
        (pytest.lazy_fixture('not_author_client'), HTTPStatus.NOT_FOUND),
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK)
    ]
)
@pytest.mark.parametrize(
    'name',
    ('news:edit', 'news:delete')
)
def test_comment_edit_delete_access(client, name, comment, expected_status):
    """Тест доступа для редактирования комментария."""
    url = reverse(name, args=(comment.id,))
    response = client.get(url)
    assert response.status_code == expected_status


@pytest.mark.django_db
@pytest.mark.parametrize(
    'url_name, news_object',
    [
        ('news:edit', pytest.lazy_fixture('news')),
        ('news:delete', pytest.lazy_fixture('news')),
    ],
)
def test_redirects_for_anonymous_client(client, url_name, news_object):
    """Тест перенаправления на страницу логина для анонимного пользователя."""
    login_url = reverse('users:login')

    if news_object is not None:
        url = reverse(url_name, args=(news_object.id,))
    else:
        url = reverse(url_name)

    expected_url = f'{login_url}?next={url}'
    response = client.get(url)

    assertRedirects(response, expected_url)
