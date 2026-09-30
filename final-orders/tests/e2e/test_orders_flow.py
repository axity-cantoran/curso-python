from fastapi.testclient import TestClient


def auth_headers(api_key: str) -> dict[str, str]:
    return {"X-API-Key": api_key}


def test_order_lifecycle(
    client: TestClient,
    api_key: str,
) -> None:
    headers = auth_headers(api_key)

    create_response = client.post(
        "/orders",
        headers=headers,
        json={
            "items": [
                {
                    "product_id": "robot",
                    "quantity": 1,
                }
            ]
        },
    )

    assert create_response.status_code == 201
    order_id = create_response.json()["id"]

    get_response = client.get(
        f"/orders/{order_id}",
        headers=headers,
    )

    assert get_response.status_code == 200
    assert get_response.json()["status"] == "PENDING"

    confirm_response = client.patch(
        f"/orders/{order_id}/status",
        headers=headers,
        json={"status": "CONFIRMED"},
    )

    assert confirm_response.status_code == 200
    assert confirm_response.json()["status"] == "CONFIRMED"

    delete_response = client.delete(
        f"/orders/{order_id}",
        headers=headers,
    )

    assert delete_response.status_code == 400


def test_delete_pending_order(
    client: TestClient,
    api_key: str,
) -> None:
    headers = auth_headers(api_key)

    create_response = client.post(
        "/orders",
        headers=headers,
        json={
            "items": [
                {
                    "product_id": "herramientas",
                    "quantity": 1,
                }
            ]
        },
    )

    assert create_response.status_code == 201
    order_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/orders/{order_id}",
        headers=headers,
    )

    assert delete_response.status_code == 204

    get_response = client.get(
        f"/orders/{order_id}",
        headers=headers,
    )

    assert get_response.status_code == 404
