# aemet_plugin

Async Python client for the AEMET Antarctica API

## Features
- Async API calls with configurable rate limiting (defaults)
- Handles time range splitting
- Fetches and aggregates meteorological data from AEMET Antarctica stations
- Returns results as a pandas DataFrame
- Handles time range splitting, error handling, and flexible configuration

## Installation
1- Open a terminal window (in Windows it can be PowerSheell)

2- Type the install command:
```bash
pip install git+https://github.com/ChallengeAxpo/aemet_plugin.git
```
3- After installation, the package should be available in the site-packages directory of your active Python environment. You can verify its location by running `pip show aemet_plugin` and checking the "Location" field.

4- Now, you can import and use the the aemet_plugin package as any other python library.

## Usage Example
A simple program example that can be used to test the library:

```python
from aemet_plugin import Aemet
import asyncio

async def main():
    result = await Aemet().get_antarctica(
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

## Parameters

- **api_key** (`str`): Your AEMET API key.
- **dateTime_start** (`str`): Start date and time in ISO format (e.g., "2024-01-01T00:00:00UTC").
- **dateTime_end** (`str`): End date and time in ISO format (e.g., "2024-01-31T23:59:59UTC").
- **meteo_station_name** (`str`): Name of the meteorological station. Must be "Meteo Station Juan Carlos I" or "Meteo Station Gabriel de Castilla".
- **time_aggregation** (`str`, optional): Aggregation method. One of `None`, `"Hourly"`, `"Daily"`, or `"Monthly"`.

## License
MIT
