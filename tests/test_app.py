from http import HTTPStatus

from fastapi.testclient import TestClient

from todo.models import User
from todo.schemas import UserPublic, UserSchema
from todo.security import create_access_token


def test_create_user(client: TestClient):
    request_body = {
        'username': 'Alice',
        'email': 'alice@example.com',
        'password': 'secret',
    }

    expected_response: dict[str, int | str] = {
        'id': 1,
        'email': 'alice@example.com',
        'username': 'Alice',
    }

    response = client.post('/users', json=request_body)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == expected_response


def test_create_user_conflict_username(client: TestClient, user: User):
    user_schema = UserSchema.model_validate(user)
    response = client.post('/users', json=user_schema.model_dump())

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username already exists'}


def test_create_user_conflict_email(client: TestClient, user: User):
    new_user = UserSchema(
        username='Alice', email='test@test.com', password='secret'
    )
    response = client.post('/users', json=new_user.model_dump())

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email already exists'}


def test_read_users(client: TestClient):
    response = client.get('/users')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_users(client: TestClient, user: User):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users')
    assert response.json() == {'users': [user_schema]}


def test_read_user(client: TestClient, user: User):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == UserPublic.model_validate(user).model_dump()


def test_read_user_not_found(client: TestClient):
    response = client.get('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_user(client: TestClient, user: User, token: str):
    request_body = {
        'username': 'Bob',
        'email': 'bob@example.com',
        'password': 'myNewPassword',
    }

    expected_response: dict[str, int | str] = {
        'id': 1,
        'email': 'bob@example.com',
        'username': 'Bob',
    }

    response = client.put(
        '/users/1',
        json=request_body,
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_response


def test_update_user_integrity_erro(
    client: TestClient, user: User, token: str
):
    created_user = {
        'username': 'Fausto',
        'email': 'fausto@example.com',
        'password': 'secret',
    }

    updated_user = {
        'username': 'Fausto',
        'email': 'bob@example.com',
        'password': 'myNewPassword',
    }

    client.post('/users', json=created_user)

    response_update = client.put(
        f'/users/{user.id}',
        json=updated_user,
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {
        'detail': 'Username or Email already exists'
    }


def test_delete_user(client: TestClient, user: User, token: str):
    response = client.delete(
        '/users/1', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_get_token(client: TestClient, user: User):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': 'test_secret'},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token


def test_jwt_invalid_token(client: TestClient):
    response = client.delete(
        '/users/1', headers={'Authorization': 'Bearer invalid-token'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_get_current_user_not_found(client: TestClient):
    data = {'no-email': 'test'}
    token = create_access_token(data)

    response = client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_get_current_does_not_exists(client: TestClient):
    data = {'sub': 'test@test'}
    token = create_access_token(data)

    response = client.delete(
        '/users/1', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
