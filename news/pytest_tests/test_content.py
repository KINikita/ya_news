import pytest
from django.conf import settings

from news.forms import CommentForm

pytestmark = pytest.mark.django_db


def test_news_count(client, home_url, list_of_news):
    """
    Проверяем, что количество новостей на главной странице
    не больше значения заданного в настройках:
    settings.NEWS_COUNT_ON_HOME_PAGE.
    """
    response = client.get(home_url)
    assert response.context['object_list'].count(
    ) == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(client, home_url, list_of_news):
    """Проверяем, что новости отсортированы от новых к старым."""
    response = client.get(home_url)
    dates = [news.date for news in response.context['object_list']]
    assert dates == sorted(dates, reverse=True)


def test_comments_order(client, detail_url, list_of_comments):
    """Проверяем, что комментарии отсортированы от старых к новым."""
    response = client.get(detail_url)
    news = response.context['news']
    comments = news.comment_set.all()
    dates = [comment.created for comment in comments]
    assert len(comments) == settings.NEWS_COUNT_ON_HOME_PAGE
    assert dates == sorted(dates, reverse=False)


def test_anonymous_client_has_no_form(client, detail_url):
    """Проверяем, что анонимному пользователю не доступна форма."""
    response = client.get(detail_url)
    assert 'form' not in response.context


def test_authorized_client_has_form(author_client, detail_url):
    """Проверяем, что авторизованному пользователю доступна форма."""
    response = author_client.get(detail_url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
