from django.apps import AppConfig


class MainConfig(AppConfig):
    name = 'main'

    def ready(self):
        from .signals import create_profile, save_profile