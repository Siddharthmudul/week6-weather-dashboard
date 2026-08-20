from weather_app.weather_display import (
    display_dashboard
)


def test_display_dashboard(capsys):

    current = {

        "city": "London",

        "country": "GB",

        "updated": "2026-08-19 10:15:00",

        "temperature": 8,

        "feels_like": 5,

        "condition": "Light Rain",

        "emoji": "🌧️",

        "humidity": 87,

        "wind_speed": 6.11,

        "wind_direction": "SW",

        "pressure": 1009,

        "visibility": 8,

        "sunrise": "07:45",

        "sunset": "16:30"
    }

    forecast = [

        {
            "day": "Thu 25 Aug",
            "emoji": "🌧️",
            "max": 9,
            "min": 6,
            "humidity": 85
        }
    ]

    display_dashboard(
        current,
        forecast,
        "Using cached data (5 minutes old)"
    )

    captured = capsys.readouterr()

    assert "WEATHER DASHBOARD" in captured.out
    assert "London, GB" in captured.out
    assert "Light Rain" in captured.out
    assert "5-Day Forecast:" in captured.out
    assert "Using cached data" in captured.out