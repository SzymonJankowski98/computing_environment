from django.apps import AppConfig


class ComputingEnvironmentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'computing_environment'

    def ready(self):
        from computing_environment import updater
        updater.start()
