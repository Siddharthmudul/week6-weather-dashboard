import requests

from .config import API_KEY, BASE_URL


def _check_api_key():
    """
    Make sure an API key exists.
    """

    normalized_key = API_KEY.lower() if API_KEY else ""
    placeholder_markers = (
        "your_",
        "replace",
        "example",
        "placeholder",
        "<",
        ">",
    )

    if not API_KEY or any(
        marker in normalized_key
        for marker in placeholder_markers
    ):
        raise ValueError(
            "API key is missing or still a placeholder. "
            "Set OPENWEATHER_API_KEY to a valid OpenWeatherMap key in .env."
        )


def get_current_weather(city, units="metric"):
    """
    Fetch current weather for a city.
    """

    _check_api_key()

    url = f"{BASE_URL}/weather"

    params = {
        "q": city,
        "appid": API_KEY,
        "units": units
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        if response.status_code == 401:
            raise ValueError(
                "Invalid API key. "
                "Please check your .env file."
            )

        if response.status_code == 404:
            raise ValueError(
                f"City '{city}' was not found."
            )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.Timeout:

        raise ValueError(
            "Weather API request timed out."
        )

    except requests.exceptions.ConnectionError:

        raise ValueError(
            "Could not connect to the weather service."
        )

    except requests.exceptions.RequestException as error:

        raise ValueError(
            f"Weather API request failed: {error}"
        )


def get_forecast(city, units="metric"):
    """
    Fetch 5-day / 3-hour forecast.
    """

    _check_api_key()

    url = f"{BASE_URL}/forecast"

    params = {
        "q": city,
        "appid": API_KEY,
        "units": units
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        if response.status_code == 401:
            raise ValueError(
                "Invalid API key."
            )

        if response.status_code == 404:
            raise ValueError(
                f"City '{city}' was not found."
            )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.Timeout:

        raise ValueError(
            "Forecast request timed out."
        )

    except requests.exceptions.ConnectionError:

        raise ValueError(
            "Could not connect to the weather service."
        )

    except requests.exceptions.RequestException as error:

        raise ValueError(
            f"Forecast request failed: {error}"
        )