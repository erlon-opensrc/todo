from http import HTTPStatus

from fastapi.testclient import TestClient

from todo.models import User
from todo.schemas import UserPublic, UserSchema


def test_create_user(client: TestClient):
    response = client.post(
        url='/users',
        json={
            'username': 'Alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'Alice',
        'email': 'alice@example.com',
    }


def test_create_user_conflict_username(client: TestClient, user: User):
    user_schema = UserSchema.model_validate(user).model_dump()
    response = client.post(url='/users', json=user_schema)

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username already exists'}


def test_create_user_conflict_email(client: TestClient, user: User):
    user_schema = UserSchema.model_validate(user)
    user_schema.username = 'bob'

    response = client.post(url='/users', json=user_schema.model_dump())

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


def test_read_current_user(client: TestClient, user: User, token: str):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema


def test_read_current_user_forbidden(
    client: TestClient, user: User, token: str
):
    response = client.get(
        url=f'/users/{user.id + 1}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


def test_update_user(client: TestClient, user: User, token: str):
    response = client.put(
        url=f'/users/{user.id}',
        json={
            'username': 'Bob',
            'email': 'bob@example.com',
            'password': 'myNewpassword',
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'Bob',
        'email': 'bob@example.com',
    }


def test_update_user_forbidden(client: TestClient, user: User, token: str):
    user_schema = UserSchema.model_validate(user).model_dump()

    response = client.put(
        url=f'/users/{user.id + 1}',
        json=user_schema,
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


def test_update_user_integrity_error(
    client: TestClient, user: User, token: str
):
    new_user = UserSchema(
        username='Bob', email='bob@example.com', password='secret'
    ).model_dump()

    client.post(url='/users', json=new_user)

    response = client.put(
        url=f'/users/{user.id}',
        json=new_user,  # tenta atualizar user com os dados de new_user.
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username or Email already exists'}


def test_delete_user(client: TestClient, user: User, token: str):
    response = client.delete(
        url=f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_forbidden(client: TestClient, user: User, token: str):
    response = client.delete(
        url=f'/users/{user.id + 1}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}
