import pandas as pd
from dateutil import parser

def get_station_code(meteo_station_name):
    """
    Returns the station code for the given meteorological station name.
    
    Parameters:
    - meteo_station: Meteorological station name (e.g., 'Meteo Station Gabriel de Castilla' and 'Meteo Station Juan Carlos I'.).
    
    Returns:
    - Station code as a string.
    """
    match meteo_station_name:
        case "Meteo Station Gabriel de Castilla": 
            return "89070"
        case "Meteo Station Juan Carlos I":
            return "89064"
        case _: 
            raise ValueError("Invalid meteorological station name. Use 'Meteo Station Gabriel de Castilla' or 'Meteo Station Juan Carlos I'.")

def split_timeFrame(dateTime_start, dateTime_end):
    """
    Splits the dateTime_start and dateTime_end into 1-month long intervals allowed by the AEMET API.
    
    Parameters:
    - dateTime_start: Start date and time in YYYY-MM-DDTHH:MM:SSUTC format (e.g., '2024-01-01T00:00:00UTC').
    - dateTime_end: End date and time in YYYY-MM-DDTHH:MM:SSUTC format (e.g., '2024-01-18T23:59:59UTC').
    
    Returns:
    - List of Tuples containing 1-month intervals starting in dateTime_start and ending in dateTime_end.
    """
    # Calculate the start timestamps for all months in the range, excluding the start and end months. Add dateTime_start to the begining of the list.
    intervals_start = pd.date_range(start = pd.to_datetime(dateTime_start), end = pd.to_datetime(dateTime_end), freq = '1MS', inclusive = "neither", normalize = True).to_list()
    intervals_start.insert(0, pd.to_datetime(dateTime_start))
    
    # Calculate the end timestamps for all months in the range, excluding the start and end months. Add dateTime_end to the end of the list.
    intervals_end = pd.date_range(start = pd.to_datetime(dateTime_start), end = pd.to_datetime(dateTime_end), freq = '1ME', inclusive = "neither", normalize = True).to_list()
    intervals_end = [dt.replace(hour=23, minute=59, second=59, microsecond=0) for dt in intervals_end]
    intervals_end.append(pd.to_datetime(dateTime_end))

    
    intervals = []
    for dateTime_start, dateTime_end in zip(intervals_start, intervals_end):
        intervals.append((
            dateTime_start.strftime('%Y-%m-%dT%H:%M:%SUTC'),
            dateTime_end.strftime('%Y-%m-%dT%H:%M:%SUTC')
        ))
    return intervals