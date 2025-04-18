from datetime import timedelta
from django.urls import reverse
from django.utils import timezone
import pytest

from django.test.client import Client
from django.conf import settings

from news.models import Comment, News


@pytest.fixture(autouse=True)
def clean_news():
    """Автоматически очищает все новости перед каждым тестом."""
    News.objects.all().delete()
    yield


@pytest.fixture(autouse=True)
def clean_comments():
    """Автоматически очищает все комментарии перед каждым тестом."""
    Comment.objects.all().delete()
    yield


@pytest.fixture
def home_url():
    return reverse('news:home')


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news(author):
    news = News.objects.create(
        title='Заголовок новости',
        text='Текст новости',
    )
    return news


@pytest.fixture
def comment(author, news):
    return Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария'
    )


@pytest.fixture
def list_of_news(author):
    all_news = [
        News(title=f'Новость {index}', text='Просто текст.')
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    News.objects.bulk_create(all_news)
    return all_news


@pytest.fixture
def list_of_comments(news, author):
    """Фикстура создаёт 10 комментариев с разными датами создания."""
    comments = []
    now = timezone.now()
    # Создаём комментарии в цикле.
    for index in range(settings.NEWS_COUNT_ON_HOME_PAGE):
        comment = Comment.objects.create(
            news=news, author=author, text=f'Tекст {index}',
        )
        comment.created = now + timedelta(days=index)
        comments.append(comment)
    return comments


@pytest.fixture
def detail_url(news):
    """Фикстура возвращает URL страницы новости."""
    return reverse('news:detail', args=(news.id,))
