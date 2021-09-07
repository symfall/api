from django.apps import AppConfig


class MessengerConfig(AppConfig):
    name = "messenger"

    def ready(self):
        import messenger.signals  # pylint: disable=C0415,W0611
