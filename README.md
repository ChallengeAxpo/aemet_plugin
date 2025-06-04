# aemet_plugin

Async Python client for the AEMET Antarctica API

## Features
- Async API calls with configurable rate limiting (defaults)
- Handles time range splitting
- Fetches and aggregates meteorological data from AEMET Antarctica stations
- Returns results as a pandas DataFrame
- Handles time range splitting, error handling, and flexible configuration

## Installation
```bash
pip install git+https://github.com/ChallengeAxpo/aemet_plugin.git
```

## Usage Example
```python
from aemet_plugin import Aemet
import asyncio

async def main():
    result = await Aemet().get_anctartica(
        api_key="YOUR_API_KEY",
        dateTime_start="2024-01-01T00:00:00UTC",
        dateTime_end="2024-01-31T23:59:59UTC",
        meteo_station_name="Meteo Station Juan Carlos I",
        time_aggregation="Daily"
    )
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

## API
- `Aemet.get_anctartica(api_key, dateTime_start, dateTime_end, meteo_station_name, time_aggregation=None)`
    - `api_key`: Your AEMET API key
    - `dateTime_start`, `dateTime_end`: ISO format strings
    - `meteo_station_name`: Station name (see utils.py for valid names)
    - `time_aggregation`: None, 'Hourly', 'Daily', or 'Monthly'

## License
MIT
