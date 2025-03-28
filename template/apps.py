from django.apps import AppConfig


class TemplateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'template'
   
    def ready(self):
        import template.signals