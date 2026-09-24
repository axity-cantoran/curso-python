from fastapi.testclient import TestClient


def test_login_invalido(client: TestClient) -> None:
    respuesta = client.post(
        "/auth/login",
        data={
            "username": "ana@example.com",
            "password": "incorrecta",
        },
    )

    assert respuesta.status_code == 401
