from orbit.core.plugin import Plugin


class TestPlugin(Plugin):
    def initialize(self) -> None:
        print("Initializing")

    def update(self) -> None:
        print("Updating")

    def shutdown(self) -> None:
        print("Stopping")


plugin = TestPlugin(
    name="Test",
    version="0.1.0",
    update_interval=5,
)

plugin.initialize()
plugin.update()
plugin.shutdown()
