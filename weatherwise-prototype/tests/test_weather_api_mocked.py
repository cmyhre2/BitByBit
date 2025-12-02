import pytest
from backend.app import call_openweather

def test_weather_proxy_mocked(mocker, client):
    mock_json = {
        "weather": [{"description": "clear sky"}],
        "main": {"temp": 20, "feels_like": 18, "humidity": 40},
        "wind": {"speed": 2},
        "name": "Test City",
        "sys": {"country": "US"},
    }

    mock_get = mocker.patch("requests.get")
    mock_resp = mocker.Mock()
    mock_resp.json.return_value = mock_json
    mock_resp.status_code = 200
    mock_resp.raise_for_status.return_value = None
    mock_get.return_value = mock_resp

    res = client.get("/api/weather?q=TestCity")
    assert res.status_code == 200
    data = res.get_json()["data"]

    assert data["main"]["temp"] == 20
    assert data["weather"][0]["description"] == "clear sky"
