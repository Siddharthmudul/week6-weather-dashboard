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
