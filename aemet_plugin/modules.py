from .async_api_client import *
from .utils import *
from .config import *
import pandas as pd
import json

class Aemet:
    def __init__(self):
        pass
        
    async def get_anctartica(self, api_key, dateTime_start, dateTime_end, meteo_station_name, time_aggregation=None):
        """
        Fetches Antarctica weather data from AEMET API. Limits of the API are:
        - Maximum of 40 requests per minute: managed by default in async_api_client.py
        - Maximum of 1 month of data per request: managed by the split_timeFrame function in utils.py
        
        Parameters:
        - api_key: AEMET API key as a string.
        - dateTime_start: Start date and time in ISO format (e.g., '2024-01-01T00:00:00UTC').
        - dateTime_end: End date and time in ISO format (e.g., '2024-01-18T23:59:59UTC').
        - meteo_station: Meteorological station name (e.g., 'Meteo Station Gabriel de Castilla' and 'Meteo Station Juan Carlos I'.).
        - time_aggregation: Time aggregation method (e.g., None, 'Hourly', 'Daily', 'Monthly').
        
        Returns:
        - Pandas dataframe with the AEMET data for anctartica aggregated by the specified time_aggregation method. The aggregation
        will chose the initial timestamp of each interval and the mean of the values for each interval.
        """
        # Get Station code and time intervals that will be passed to the AEMET API in each request
        meteo_station_code = get_station_code(meteo_station_name)
        intervals = split_timeFrame(dateTime_start, dateTime_end)

        # Create the API URLs for each 1-month time interval
        urls = [f"{BASE_URL_ANCTARTICA}/fechaini/{start_date}/fechafin/{end_date}/estacion/{meteo_station_code}?api_key={api_key}" 
                for start_date, end_date in intervals]
        
        # Use AsyncClient to fetch data urls from the API via asynchronous requests
        client = AsyncClient()
        api_responses = await client.fetch_multiple(urls)
        data_urls = [json.loads(response.decode('utf-8'))['datos'] for response in api_responses]
        
        # Fetch the json data from the data URLs 
        data_responses = await client.fetch_multiple(data_urls)
        data = [json.loads(response.decode('utf-8')) for response in data_responses]
        
        # Flatten the list of lists into a single list of dictionaries
        data_flat = [dict for sublist in data for dict in sublist]
        
        # Filter the data to keep only the relevant keys
        keys = ['nombre', 'fhora', 'temp', 'pres', 'vel']
        data_filtered = [{k : dict[k] for k in keys} for dict in data_flat]
        
        #Create and format pandas DataFrame
        data_pd = pd.DataFrame(data_filtered)
        data_format_pd = data_pd.rename(columns={
            'nombre' : 'Station',
            'fhora' : 'Datetime',
            'temp' : 'Temperature (ºC)',
            'pres' : 'Pressure (hpa)',
            'vel' : 'Speed (m/s)'
        })
        data_format_pd = data_format_pd.sort_values('Datetime')
        data_format_pd['Temperature (ºC)'] = pd.to_numeric(data_format_pd['Temperature (ºC)'], errors='coerce')
        data_format_pd['Pressure (hpa)'] = pd.to_numeric(data_format_pd['Pressure (hpa)'], errors='coerce')
        data_format_pd['Speed (m/s)'] = pd.to_numeric(data_format_pd['Speed (m/s)'], errors='coerce')
        data_format_pd['Datetime'] = pd.to_datetime(
            data_format_pd['Datetime'], errors='coerce', utc=True
        ).dt.tz_convert('Europe/Madrid')
        
        # Select aggregation frequency based on the time_aggregation parameter
        match time_aggregation:
            case None:
                output = data_format_pd
                return output
            case 'Hourly':
                groupby_freq = 'h'
            case 'Daily':
                groupby_freq = 'D'
            case 'Monthly':
                groupby_freq = 'MS'
            case _:
                raise ValueError("Invalid time aggregation method. Use None, 'Hourly', 'Daily', or 'Monthly'.")
            
        # apply selected aggregation frequency and aggregate datas specified.
        data_format_pd.set_index('Datetime', inplace=True)
        output = data_format_pd.groupby(pd.Grouper(freq = groupby_freq)).agg({
            'Station': 'first',
            'Temperature (ºC)': 'mean',
            'Pressure (hpa)': 'mean',
            'Speed (m/s)': 'mean'
            }).reset_index().sort_values('Datetime')
        return output