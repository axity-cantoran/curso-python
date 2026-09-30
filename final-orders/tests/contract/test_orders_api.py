from fastapi.testclient import TestClient


def auth_headers(api_key: str) -> dict[str, str]:
    return {"X-API-Key": api_key}


def test_create_order_requires_api_key(client: TestClient) -> None:
    response = client.post(
        "/orders",
        json={
            "items": [
                {
                    "product_id": "caballero",
                    "quantity": 1,
                }
            ]
        },
    )

    assert response.status_code == 401


def test_create_order_returns_expected_contract(
    client: TestClient,
    api_key: str,
) -> None:
    response = client.post(
        "/orders",
        headers=auth_headers(api_key),
        json={
            "items": [
                {
                    "product_id": "caballero",
                    "quantity": 1,
                },
                {
                    "product_id": "accesorios",
                    "quantity": 2,
                },
            ]
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert "id" in body
    assert body["status"] == "PENDING"
    assert len(body["items"]) == 2
    assert body["items"][0]["product_id"] == "caballero"


def test_unknown_product_returns_bad_request(
    client: TestClient,
    api_key: str,
) -> None:
    response = client.post(
        "/orders",
        headers=auth_headers(api_key),
        json={
            "items": [
                {
                    "product_id": "producto-inexistente",
                    "quantity": 1,
                }
            ]
        },
    )

    assert response.status_code == 400


def test_get_missing_order_returns_not_found(
    client: TestClient,
    api_key: str,
) -> None:
    response = client.get(
        "/orders/00000000-0000-0000-0000-000000000000",
        headers=auth_headers(api_key),
    )

    assert response.status_code == 404


def test_invalid_quantity_returns_unprocessable_entity(
    client: TestClient,
    api_key: str,
) -> None:
    response = client.post(
        "/orders",
        headers=auth_headers(api_key),
        json={
            "items": [
                {
                    "product_id": "robot",
                    "quantity": 0,
                }
            ]
        },
    )

    assert response.status_code == 422
