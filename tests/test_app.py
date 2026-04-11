from http import HTTPStatus

from fastapi.testclient import TestClient


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

    response = client.post('/users/', json=request_body)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == expected_response


def test_read_users(client: TestClient):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [{'id': 1, 'email': 'alice@example.com', 'username': 'Alice'}]
    }


def test_read_user(client: TestClient):
    expected_response: dict[str, str | int] = {
        'username': 'Alice',
        'email': 'alice@example.com',
        'id': 1,
    }

    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_response


def test_read_user_not_found(client: TestClient):
    response = client.get('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_user(client: TestClient):
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

    response = client.put('/users/1', json=request_body)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_response


def test_updated_user_not_found(client: TestClient):
    request_body = {
        'username': 'Alice',
        'email': 'alice@example.com',
        'password': 'secret',
    }

    response = client.put('/users/2', json=request_body)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client: TestClient):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_not_found(client: TestClient):
    response = client.delete('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
