from orbit.core.plugin import Plugin
from orbit.core.scheduler import Scheduler


class TestPlugin(Plugin):
    def initialize(self):
        print(f"{self.name}: initialized")

    def update(self):
        print(f"{self.name}: update")

    def shutdown(self):
        print(f"{self.name}: stopped")


scheduler = Scheduler()

scheduler.register(TestPlugin("Music", update_interval=1))
scheduler.register(TestPlugin("System", update_interval=2))
scheduler.register(TestPlugin("Weather", update_interval=5))

scheduler.start()
