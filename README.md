# Weather Dashboard (week6)

Minimal weather dashboard CLI using OpenWeatherMap.

Setup

1. Create a virtual environment and install dependencies:

```bash
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and set `OPENWEATHER_API_KEY`.

Run

```bash
python -m weather_app.main London
```

Tests

```bash
pytest
```


Weather Dashboard Application
Project Description
A comprehensive weather application that fetches real-time weather data from external APIs and displays it in a user-friendly interface. This project demonstrates API integration, external library usage, and professional Python development practices.
What I Learned
1. API Integration: How to work with external web services
2. HTTP Requests: Making GET requests and handling responses
3. JSON Processing: Parsing and working with complex JSON data
4. Error Handling: Managing network errors and API limitations
5. Environment Management: Using environment variables for configuration
6. Package Management: Installing and using external libraries

Features

•	Current weather for any city worldwide
•	5-day weather forecast with daily summaries
•	Temperature in Celsius or Fahrenheit
•	Weather condition icons and descriptions
•	Wind speed, humidity, and pressure information
•	City search with autocomplete
•	Favorite cities management
•	API response caching
•	Comprehensive error handling
•	Export weather data to CSV
Required Libraries

requests: For making HTTP requests
python-dotenv: For environment variable management
colorama: For colored terminal output (optional)


How to Run

1. Get API key from OpenWeatherMap
2. Copy .env.example to .env and add your API key
3. Install dependencies: pip install -r requirements.txt
4. Run: python -m weather_app.main
















Code:

import json
import time

from .config import (
    DEFAULT_UNITS,
    FAVORITES_FILE,
    CACHE_DIR,
    CACHE_DURATION
)

from .weather_api import (
    get_current_weather,
    get_forecast
)

from .weather_parser import (
    parse_current_weather,
    parse_forecast
)

from .weather_display import (
    display_dashboard
)

# --------------------------------------------------
# CACHE FUNCTIONS
# --------------------------------------------------

def get_cache_file(city):
    """
    Return cache file path for a city.
    """

    safe_city = (
        city.lower()
        .replace(" ", "_")
        .replace("/", "_")
    )

    return CACHE_DIR / f"{safe_city}.json"

def save_cache(
    city,
    current,
    forecast
):
    """
    Save weather information to cache.
    """

    cache_file = get_cache_file(city)

    cache_data = {
        "timestamp": time.time(),
        "city": city,
        "current": current,
        "forecast": forecast
    }

    with open(
        cache_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            cache_data,
            file,
            indent=4
        )

def load_cache(city):
    """
    Load cached weather data if it is
    less than 5 minutes old.
    """

    cache_file = get_cache_file(city)

    if not cache_file.exists():

        return None

    try:

        with open(
            cache_file,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        age = time.time() - data["timestamp"]

        if age <= CACHE_DURATION:

            return data, int(age)

    except (
        json.JSONDecodeError,
        KeyError,
        OSError
    ):

        return None

    return None

# --------------------------------------------------
# FAVORITE FUNCTIONS
# --------------------------------------------------

def load_favorites():
    """
    Load favorite cities.
    """

    if not FAVORITES_FILE.exists():

        return []

    try:

        with open(
            FAVORITES_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except (
        json.JSONDecodeError,
        OSError
    ):

        return []

def save_favorites(favorites):
    """
    Save favorite cities.
    """

    FAVORITES_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        FAVORITES_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            favorites,
            file,
            indent=4
        )

def add_favorite(city):
    """
    Add a city to favorites.
    """

    favorites = load_favorites()

    if city not in favorites:

        favorites.append(city)

        save_favorites(favorites)

        print(
            f"⭐ {city} added to favorites."
        )

    else:

        print(
            f"⭐ {city} is already a favorite."
        )

def show_favorites():
    """
    Display favorite cities.
    """

    favorites = load_favorites()

    print()
    print("⭐ Favorite Cities")
    print("------------------")

    if not favorites:

        print("No favorite cities.")

        return

    for index, city in enumerate(
        favorites,
        start=1
    ):

        print(
            f"{index}. {city}"
        )

# --------------------------------------------------
# API / CACHE
# --------------------------------------------------

def fetch_weather(
    city,
    force_refresh=False
):
    """
    Fetch weather from cache or API.
    """

    if not force_refresh:

        cached = load_cache(city)

        if cached:

            data, age = cached

            minutes = age // 60

            status = (
                f"Using cached data "
                f"({minutes} minutes old)"
            )

            return (
                data["current"],
                data["forecast"],
                status
            )

    print(
        "\nFetching latest weather data..."
    )

    current_data = get_current_weather(
        city,
        DEFAULT_UNITS
    )

    forecast_data = get_forecast(
        city,
        DEFAULT_UNITS
    )

    current = parse_current_weather(
        current_data
    )

    forecast = parse_forecast(
        forecast_data
    )

    save_cache(
        city,
        current,
        forecast
    )

    return (
        current,
        forecast,
        "Using fresh API data"
    )

# --------------------------------------------------
# DISPLAY
# --------------------------------------------------

def show_weather(
    city,
    force_refresh=False
):
    """
    Get and display weather.
    """

    try:

        current, forecast, status = fetch_weather(
            city,
            force_refresh
        )

        display_dashboard(
            current,
            forecast,
            status
        )

        return True

    except ValueError as error:

        print()
        print(f"❌ Error: {error}")

        return False

# --------------------------------------------------
# MAIN PROGRAM
# --------------------------------------------------

def main():

    print()
    print("🌤️  WEATHER DASHBOARD")
    print("=======================")

    city = input(
        "Enter city name: "
    ).strip()

    while not city:

        print("City name cannot be empty.")

        city = input(
            "Enter city name: "
        ).strip()

    while True:

        success = show_weather(city)

        if not success:

            city = input(
                "\nEnter another city: "
            ).strip()

            while not city:

                print("City name cannot be empty.")

                city = input(
                    "Enter another city: "
                ).strip()

            continue

        print()

        print(
            "Type 'refresh' to update, "
            "'search' for new city, "
            "'favorite' to save city, "
            "'favorites' to view favorites, "
            "or 'quit' to exit:"
        )

        command = input(
            "\n> "
        ).strip().lower()

        # ------------------------------------------
        # REFRESH
        # ------------------------------------------

        if command == "refresh":

            show_weather(
                city,
                force_refresh=True
            )

        # ------------------------------------------
        # SEARCH
        # ------------------------------------------

        elif command == "search":

            new_city = input(
                "Enter city name: "
            ).strip()

            if new_city:

                city = new_city

                show_weather(city)

        # ------------------------------------------
        # FAVORITE
        # ------------------------------------------

        elif command == "favorite":

            add_favorite(city)

        # ------------------------------------------
        # SHOW FAVORITES
        # ------------------------------------------

        elif command == "favorites":

            show_favorites()

        # ------------------------------------------
        # QUIT
        # ------------------------------------------

        elif command == "quit":

            print()
            print(
                "Thank you for using "
                "Weather Dashboard! 🌤️"
            )

            break

        # ------------------------------------------
        # INVALID COMMAND
        # ------------------------------------------

        else:

            print(
                "\n❌ Unknown command."
            )

            print(
                "Available commands:"
            )

            print(
                "refresh | search | favorite | "
                "favorites | quit"
            )

if __name__ == "__main__":
    main()
















Output:





























































































Testing Evidence





















































































































































