import pytest
from django.conf import settings

from news.forms import CommentForm


@pytest.mark.django_db
def test_news_count(client, home_url, list_of_news):
    """Проверяем, что количество новостей на главной странице не более 10."""
    response = client.get(home_url)
    object_list = response.context['object_list']
    assert object_list.count() == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(client, home_url, list_of_news):
    """Проверяем, что новости отсортированы от новых к старым."""
    response = client.get(home_url)
    news_list = response.context['object_list']
    dates = [news.date for news in news_list]
    assert dates == sorted(dates, reverse=True)


@pytest.mark.django_db
def test_comments_order(client, news_with_comments):
    """Проверяем, что комментарии отсортированы от старых к новым."""
    response = client.get(news_with_comments['detail_url'])
    news = response.context['news']
    comments = news.comment_set.all()
    dates = [comment.created for comment in comments]
    assert dates == sorted(dates, reverse=False)


def test_anonymous_client_has_no_form(client, news_with_comments):
    """Проверяем, что анонимному пользователю не доступна форма."""
    response = client.get(news_with_comments['detail_url'])
    assert 'form' not in response.context


def test_authorized_client_has_form(author_client, news_with_comments):
    """Проверяем, что авторизованному пользователю доступна форма."""
    response = author_client.get(news_with_comments['detail_url'])
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
