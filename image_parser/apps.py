from django.apps import AppConfig


class ImageParcerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'image_parser'

    def ready(self):
        from . import signals
