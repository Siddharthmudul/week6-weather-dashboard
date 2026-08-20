from unittest.mock import patch, Mock

from weather_app.weather_api import (
    get_current_weather
)


@patch("weather_app.weather_api.API_KEY", "valid-test-key")
@patch("weather_app.weather_api.requests.get")
def test_get_current_weather(mock_get):

    mock_response = Mock()

    mock_response.status_code = 200

    mock_response.json.return_value = {
        "name": "London",
        "main": {
            "temp": 8
        }
    }

    mock_response.raise_for_status.return_value = None

    mock_get.return_value = mock_response

    result = get_current_weather(
        "London"
    )

    assert result["name"] == "London"

    mock_get.assert_called_once()