from http import HTTPStatus

from fastapi.testclient import TestClient

from todo.app import app


def test_root_deve_retorna_ok_e_hello_world():
    client = TestClient(app) # Arrange -> Organizar

    response = client.get('/') # Act -> Agir

    # Assert -> Afirmar
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello, World!'}
