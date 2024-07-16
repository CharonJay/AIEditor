from django.apps import AppConfig


class DialogueConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "dialogue"

    def ready(self):
        import dialogue.signals