import http

import pytest

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

pytestmark = pytest.mark.django_db


def test_anonymous_user_cant_create_comment(client, detail_url):
    form_data = {'text': 'Текст комментария'}
    initial_count = Comment.objects.count()
    client.post(detail_url, data=form_data)
    assert Comment.objects.count() == initial_count


def test_user_can_create_comment(
    clean_comments,
    author_client,
    detail_url,
    news,
    author
):
    form_data = {'text': '+ 1 комментарий'}
    initial_count = Comment.objects.count()
    response = author_client.post(detail_url, data=form_data)
    assert response.url == f'{detail_url}#comments'
    assert Comment.objects.count() == initial_count + 1
    new_comment = Comment.objects.latest('id')
    assert new_comment.text == form_data['text']
    assert new_comment.news == news
    assert new_comment.author == author


def test_user_cant_use_bad_words(
    author_client,
    detail_url,
):
    """Тест проверяет, что нельзя отправить комментарий со стоп-словами."""
    initial_count = Comment.objects.count()
    bad_text = f'Какой-то текст, {BAD_WORDS[0]}, еще текст'
    response = author_client.post(detail_url, data={'text': bad_text})
    form = response.context['form']
    assert Comment.objects.count() == initial_count
    assert form.errors
    assert 'text' in form.errors
    assert WARNING in form.errors['text']


def test_author_can_delete_own_comment(
    author_client,
    delete_url,
    detail_url,
    comment,
):
    """
    Тест проверяет, что авторизованный пользователь
    может удалить свой комментарий.
    """
    initial_count = Comment.objects.count()
    news_url = detail_url + '#comments'
    response = author_client.delete(delete_url)
    assert Comment.objects.count() == initial_count - 1
    assert response.status_code == http.HTTPStatus.FOUND, (
        f"Ожидался статус 302, получен {response.status_code}. "
        f"URL: {delete_url}"
    )
    assert response.url == news_url
    assert not Comment.objects.filter(id=comment.id).exists()


def test_author_can_not_delete_not_own_comment(
    not_author_client,
    delete_url,
    comment,
):
    """
    Тест проверяет, что авторизованный пользователь
    не может удалить чужой комментарий.
    """
    initial_count = Comment.objects.count()
    response = not_author_client.delete(delete_url)
    assert response.status_code == http.HTTPStatus.NOT_FOUND, (
        f"Ожидался статус 404, получен {response.status_code}. "
        f"URL: {delete_url}"
    )
    assert Comment.objects.filter(id=comment.id).exists()
    assert Comment.objects.count() == initial_count
