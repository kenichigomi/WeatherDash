"""
API file for a weather dashboard
- Kenichi Gomi
"""
import requests
import json
import pandas as pd


class WeatherAPI:

    @staticmethod
    def get_forecast(lat, lon, key, units='imperial'):
        """
        Gets weather data for a specified location
        Args:
            lat (float): Latitude
            lon (float): Longitude
            key (str): API key
            units (str): units of measurement
        Output:
            dataframe (df): dataframe containing weather data
        """
        url = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units={units}&appid={key}'

        # get url as a string
        url_text = requests.get(url).text

        # convert json to a nested dict
        weather_dict = json.loads(url_text)

        # clean it up
        row_list = list()
        for d in weather_dict['list']:
            # process dictionary into a row
            for feat in ['main', 'sys', 'wind', 'clouds']:
                d.update(d[feat])
                del d[feat]

            for i in d['weather']:
                d.update(d['weather'][0])
            del d['weather']

            # store
            row_list.append(d)

        # convert list of dictionaries to dataframe
        return pd.DataFrame(row_list)

    @staticmethod
    def get_cities():
        """
        Returns a dictionary of cities and their coordinates
        Args: none
        Output:
            cities_dict (dict): A dictionary of cities and their coordinates
        """
        cities_dict = {'Boston': (42.3601, 71.0589),
                       'New York City': (40.7128, 74.0060),
                       'San Francisco': (37.7749, 122.4194),
                       'Tokyo': (35.6764, 139.6500),
                       'Dubai': (25.2048, 55.2708)}

        # In reality I want this function to be able to pull lat/long from another api
        return cities_dict

    @staticmethod
    def get_hours(df, colname, day):
        """
        Gets all unique hours in a dataframe column
        Args:
            df (DataFrame): a dataframe to check for hours
            colname (str): the column storing the hours
            date_picker (str): the date of interest
        Output:
            hour_list (list): a list of all unique hours
        """
        df[colname] = pd.to_datetime(df[colname])
        target_df = df[df[colname].dt.date == pd.to_datetime(day).date()]
        hour_list = target_df[colname].dt.hour.unique()

        return hour_list












