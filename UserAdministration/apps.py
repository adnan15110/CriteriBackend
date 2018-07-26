from django.apps import AppConfig


class UseradministrationConfig(AppConfig):
    name = 'UserAdministration'

    def ready(self):
            import UserAdministration.signals
