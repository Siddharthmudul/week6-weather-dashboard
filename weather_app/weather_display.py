def display_dashboard(
    current,
    forecast,
    cache_status
):
    """
    Display the complete weather dashboard.
    """

    print()
    print("🌤️  WEATHER DASHBOARD")
    print("=======================")
    print()

    print(
        f"📍 Current Location: "
        f"{current['city']}, "
        f"{current['country']}"
    )

    print(
        f"🕐 Last Updated: "
        f"{current['updated']}"
    )

    print()

    print("Current Weather:")
    print("────────────────")

    print(
        f"Temperature:   "
        f"{current['temperature']:.0f}°C "
        f"(Feels like: "
        f"{current['feels_like']:.0f}°C)"
    )

    print(
        f"Conditions:    "
        f"{current['condition']} "
        f"{current['emoji']}"
    )

    print(
        f"Humidity:      "
        f"{current['humidity']}%"
    )

    wind_kmh = current["wind_speed"] * 3.6

    print(
        f"Wind:          "
        f"{wind_kmh:.0f} km/h "
        f"from {current['wind_direction']}"
    )

    print(
        f"Pressure:      "
        f"{current['pressure']} hPa"
    )

    print(
        f"Visibility:    "
        f"{current['visibility']:.0f} km"
    )

    print(
        f"Sunrise:       "
        f"{current['sunrise']}"
    )

    print(
        f"Sunset:        "
        f"{current['sunset']}"
    )

    print()

    print("5-Day Forecast:")
    print("───────────────")

    for day in forecast:

        print(
            f"{day['day']}:  "
            f"{day['emoji']}   "
            f"{day['max']:.0f}°C / "
            f"{day['min']:.0f}°C  "
            f"(Humidity: "
            f"{day['humidity']}%)"
        )

    print()

    print(
        f"API Status: {cache_status}"
    )