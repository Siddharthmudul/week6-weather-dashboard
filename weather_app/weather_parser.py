from datetime import datetime


def format_time(timestamp):
    """
    Convert Unix timestamp to HH:MM.
    """

    if not timestamp:
        return "N/A"

    return datetime.fromtimestamp(
        timestamp
    ).strftime("%H:%M")


def format_datetime(timestamp):
    """
    Convert Unix timestamp to YYYY-MM-DD HH:MM:SS.
    """

    if not timestamp:
        return "N/A"

    return datetime.fromtimestamp(
        timestamp
    ).strftime("%Y-%m-%d %H:%M:%S")


def get_wind_direction(degrees):
    """
    Convert wind direction in degrees
    into compass direction.
    """

    if degrees is None:
        return "N/A"

    directions = [
        "N",
        "NE",
        "E",
        "SE",
        "S",
        "SW",
        "W",
        "NW"
    ]

    index = round(degrees / 45) % 8

    return directions[index]


def get_weather_emoji(condition):
    """
    Return an emoji for a weather condition.
    """

    condition = condition.lower()

    if "thunderstorm" in condition:
        return "⛈️"

    if "drizzle" in condition:
        return "🌦️"

    if "rain" in condition:
        return "🌧️"

    if "snow" in condition:
        return "❄️"

    if "mist" in condition:
        return "🌫️"

    if "fog" in condition:
        return "🌫️"

    if "haze" in condition:
        return "🌫️"

    if "clear" in condition:
        return "☀️"

    if "cloud" in condition:
        return "☁️"

    return "🌤️"


def parse_current_weather(data):
    """
    Parse current weather API response.
    """

    weather = data.get(
        "weather",
        [{}]
    )[0]

    main = data.get(
        "main",
        {}
    )

    wind = data.get(
        "wind",
        {}
    )

    system = data.get(
        "sys",
        {}
    )

    condition = weather.get(
        "description",
        "Unknown"
    ).title()

    visibility_meters = data.get(
        "visibility",
        0
    )

    visibility_km = visibility_meters / 1000

    return {
        "city": data.get(
            "name",
            "Unknown"
        ),

        "country": system.get(
            "country",
            ""
        ),

        "updated": format_datetime(
            data.get("dt")
        ),

        "temperature": main.get(
            "temp",
            0
        ),

        "feels_like": main.get(
            "feels_like",
            0
        ),

        "condition": condition,

        "emoji": get_weather_emoji(
            condition
        ),

        "humidity": main.get(
            "humidity",
            0
        ),

        "wind_speed": wind.get(
            "speed",
            0
        ),

        "wind_direction": get_wind_direction(
            wind.get("deg")
        ),

        "pressure": main.get(
            "pressure",
            0
        ),

        "visibility": visibility_km,

        "sunrise": format_time(
            system.get("sunrise")
        ),

        "sunset": format_time(
            system.get("sunset")
        )
    }


def parse_forecast(data):
    """
    Parse OpenWeatherMap 5-day forecast.

    The API returns data every 3 hours.
    This function creates one summary per day.
    """

    forecast_list = data.get(
        "list",
        []
    )

    daily = {}

    for item in forecast_list:

        timestamp = item.get("dt")

        if not timestamp:
            continue

        date = datetime.fromtimestamp(
            timestamp
        ).strftime("%Y-%m-%d")

        weather = item.get(
            "weather",
            [{}]
        )[0]

        main = item.get(
            "main",
            {}
        )

        condition = weather.get(
            "description",
            "Unknown"
        )

        temperature = main.get(
            "temp"
        )

        temp_min = main.get(
            "temp_min"
        )

        temp_max = main.get(
            "temp_max"
        )

        humidity = main.get(
            "humidity"
        )

        # Create day if it doesn't exist
        if date not in daily:

            daily[date] = {
                "date": date,

                "day": datetime.fromtimestamp(
                    timestamp
                ).strftime("%a %d %b"),

                "temperature": temperature,

                "min": temp_min,

                "max": temp_max,

                "humidity": humidity,

                "condition": condition.title(),

                "emoji": get_weather_emoji(
                    condition
                )
            }

        else:

            # Update minimum temperature
            if temp_min is not None:

                if (
                    daily[date]["min"] is None
                    or temp_min < daily[date]["min"]
                ):
                    daily[date]["min"] = temp_min

            # Update maximum temperature
            if temp_max is not None:

                if (
                    daily[date]["max"] is None
                    or temp_max > daily[date]["max"]
                ):
                    daily[date]["max"] = temp_max

    return list(daily.values())[:5]