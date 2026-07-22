from orbit.core.plugin import Plugin
from orbit.plugins.weather.service import WeatherService


class WeatherPlugin(Plugin):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = WeatherService()

    def initialize(self):
        print("Weather initialized")

    def update(self):
        weather = self.service.get_weather()

        print(weather)

    def shutdown(self):
        print("Weather stopped")
