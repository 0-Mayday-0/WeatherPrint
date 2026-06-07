import requests
from dotenv import load_dotenv
from os import getenv
from os import system
from datetime import datetime


class WeatherData:
    def __init__(self) -> None:
        load_dotenv('api.env')
        self._protocol: str = 'http://'
        self._subdomain: str = 'api.'
        self._root_domain: str = 'openweathermap.'
        self._top_domain: str = 'org/'
        self._path: str = 'data/2.5/weather'
        #self._lat: str = f'?lat={getenv("LOCALE_LAT")}' DEPRECATED
        #self._lon: str = f'&lon={getenv("LOCALE_LON")}' DEPRECATED
        self._locale: str = f'?q={getenv("LOCALE")}'
        self._metric: str = '&units=metric'
        self._api_key: str = f'&appid={getenv("API_KEY")}'

    def __str__(self) -> str:
        return (f'{self._protocol}{self._subdomain}{self._root_domain}'
                f'{self._top_domain}{self._path}{self._locale}{self._metric}'
                f'{self._api_key}')

    def fetch_weather(self) -> dict:
        weather_data: requests.Response = requests.get(str(self))
        return weather_data.json()

    def print_weather(self, filename: str, center_width: int) -> None:
        open(filename, 'w').close()
        timestamp: datetime = datetime.now()
        weather_data: dict = self.fetch_weather()
        header: str = f'WEATHER REPORT - {timestamp.strftime("%d/%m/%Y - %H:%M:%S")}'

        main_data: dict = weather_data['main']
        clouds: int = weather_data['clouds']['all']

        sunrise: str = datetime.fromtimestamp(weather_data['sys']['sunrise']).strftime('%H:%M')
        sunset: str = datetime.fromtimestamp(weather_data['sys']['sunset']).strftime('%H:%M')

        with open(filename, 'a') as file_handle:
            print(f'{header.center(center_width)}\n\20\n{'-'*45}\n\20\n{"TEMPERATURE".center(center_width)}\n\20\n'
                  f'{"Current: ".center(center_width)}{main_data['temp']} degC\n\20\n{"Min: ".center(center_width)}'
                  f'{main_data['temp_min']} degC\n{"Max: ".center(center_width)}{main_data['temp_max']} degC\n\20\n'
                  f'{"Feels like: ".center(center_width)}{main_data['feels_like']} degC\n\20\n{'-'*45}\n\20\n'
                  f'{"EXTRA INFORMATION".center(center_width)}\n\20\n{"Humidity: ".center(center_width)}'
                  f'{main_data['humidity']}%\n{"Overcast: ".center(center_width)}{clouds}%\n\20\n'
                  f'{"Wind: ".rjust(center_width-14)}{weather_data['wind']['speed']} knots\n\20\n'
                  f'{"Sunrise: ".center(center_width)}{sunrise}\n{"Sunset: ".center(center_width)}{sunset}\n\20\n'
                  f'{weather_data['weather'][0]['description'].title().center(center_width)}', file=file_handle)

        system(f'python ./cat-printer/printer.py ./weather.txt -d -D --assume-text -A {getenv("PRINTER_MAC")}')



def main() -> None:
    handle: WeatherData = WeatherData()

    handle.print_weather('weather.txt', 30)

if __name__ == "__main__":
    main()