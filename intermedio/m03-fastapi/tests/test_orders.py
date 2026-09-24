from fastapi.testclient import TestClient


def test_crear_order_sin_token(client: TestClient) -> None:
    respuesta = client.post(
        "/orders/",
        json={
            "product": "Teclado",
            "quantity": 2,
            "unit_price": 50.0,
        },
    )

    assert respuesta.status_code == 401
