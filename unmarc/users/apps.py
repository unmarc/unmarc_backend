from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'
    verbose_name = 'unmarc Users'

    def ready(self):
        from . import signals
