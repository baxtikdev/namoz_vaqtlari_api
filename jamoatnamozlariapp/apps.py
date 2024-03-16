from django.apps import AppConfig


class JamoatnamozlariappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'jamoatnamozlariapp'

    verbose_name = "Jamoat namozlari"

    def ready(self):
        import jamoatnamozlariapp.signals
