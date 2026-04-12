from http import HTTPStatus

from fastapi.testclient import TestClient

from todo.models import User


def test_get_token(client: TestClient, user: User):
    response = client.post(
        url='/auth/token',
        data={'username': user.email, 'password': 'test_secret'},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token


def test_get_token_unauthorized_not_user(client: TestClient):
    response = client.post(
        url='/auth/token', data={'username': 'Alice', 'password': 'secret'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_get_token_unauthorized_password(client: TestClient, user: User):
    response = client.post(
        '/auth/token',
        data={'username': user.username, 'password': 'invalidPassword'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password'}
