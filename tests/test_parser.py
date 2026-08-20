from weather_app.weather_parser import (
    get_wind_direction,
    get_weather_emoji,
    parse_current_weather
)


def test_wind_direction():

    assert get_wind_direction(0) == "N"
    assert get_wind_direction(90) == "E"
    assert get_wind_direction(180) == "S"
    assert get_wind_direction(270) == "W"


def test_weather_emoji():

    assert get_weather_emoji(
        "clear sky"
    ) == "☀️"

    assert get_weather_emoji(
        "light rain"
    ) == "🌧️"

    assert get_weather_emoji(
        "snow"
    ) == "❄️"


def test_parse_current_weather():

    sample_data = {

        "name": "London",

        "sys": {
            "country": "GB",
            "sunrise": 1706165100,
            "sunset": 1706193000
        },

        "dt": 1706174100,

        "main": {
            "temp": 8,
            "feels_like": 5,
            "humidity": 87,
            "pressure": 1009
        },

        "weather": [
            {
                "description": "light rain"
            }
        ],

        "wind": {
            "speed": 6.11,
            "deg": 225
        },

        "visibility": 8000
    }

    result = parse_current_weather(
        sample_data
    )

    assert result["city"] == "London"
    assert result["country"] == "GB"
    assert result["temperature"] == 8
    assert result["humidity"] == 87
    assert result["pressure"] == 1009
    assert result["wind_direction"] == "SW"