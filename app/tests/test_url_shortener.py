from fastapi import status


def test_create_short_url(client, example_url, mock_redis):
    response = client.post("/urls/", json=example_url)
    assert response.status_code == status.HTTP_200_OK
    assert "short_url" in response.json()
    assert response.json()["original_url"] == example_url["original_url"]


def test_get_original_url(client, example_url, mock_redis):
    response = client.post("/urls/", json=example_url)
    short_url = response.json()["short_url"]
    response = client.get(f"/{short_url}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["original_url"] == example_url["original_url"]


def test_redirect(client, example_url, mock_redis):
    response = client.post("/urls/", json=example_url)
    short_url = response.json()["short_url"]
    response = client.get(f"/{short_url}/redirect", follow_redirects=False)
    assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
    assert response.headers["location"] == example_url["original_url"]


def test_invalid_short_url(client, mock_redis):
    invalid_short_url = "invalidURL"
    response = client.get(f"/{invalid_short_url}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_invalid_redirect(client, mock_redis):
    invalid_short_url = "invalidURL"
    response = client.get(f"/{invalid_short_url}/redirect", follow_redirects=False)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_cache_mechanism(client, example_url, mock_redis):
    response = client.post("/urls/", json=example_url)
    short_url = response.json()["short_url"]
    response = client.get(f"/{short_url}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["original_url"] == example_url["original_url"]
    response = client.get(f"/{short_url}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["original_url"] == example_url["original_url"]
