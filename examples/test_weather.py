from orbit.core.scheduler import Scheduler
from orbit.plugins.weather.plugin import WeatherPlugin

scheduler = Scheduler()

scheduler.register(
    WeatherPlugin(
        name="Weather",
        update_interval=5,
    )
)

scheduler.start()
