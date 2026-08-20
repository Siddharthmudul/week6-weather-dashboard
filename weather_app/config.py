import os
from pathlib import Path

from dotenv import load_dotenv


# --------------------------------------------------
# PROJECT PATH
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent


# --------------------------------------------------
# ENVIRONMENT FILE
# --------------------------------------------------

ENV_FILE = BASE_DIR / ".env"

load_dotenv(
    dotenv_path=ENV_FILE,
    override=True
)


# --------------------------------------------------
# API SETTINGS
# --------------------------------------------------

API_KEY = os.getenv(
    "OPENWEATHER_API_KEY"
)

BASE_URL = (
    "https://api.openweathermap.org/data/2.5"
)


# --------------------------------------------------
# DATA SETTINGS
# --------------------------------------------------

DATA_DIR = BASE_DIR / "data"

CACHE_DIR = DATA_DIR / "cache"

FAVORITES_FILE = DATA_DIR / "favorites.json"


# --------------------------------------------------
# CACHE SETTINGS
# --------------------------------------------------

CACHE_DURATION = 300


# --------------------------------------------------
# DEFAULT SETTINGS
# --------------------------------------------------

DEFAULT_CITY = "London"

DEFAULT_UNITS = "metric"


# --------------------------------------------------
# CREATE DIRECTORIES
# --------------------------------------------------

CACHE_DIR.mkdir(
    parents=True,
    exist_ok=True
)


DATA_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# --------------------------------------------------
# API KEY CHECK
# --------------------------------------------------

if not API_KEY:

    print()
    print(
        "⚠️  WARNING: OpenWeatherMap API key "
        "was not found."
    )

    print(
        f"Expected .env file at:"
    )

    print(
        ENV_FILE
    )

    print()