from django.apps import AppConfig


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
    verbose_name = 'Задание к уроку 30.1'

    def ready(self):
        pass
        # import app.signals  # noqa: F401
