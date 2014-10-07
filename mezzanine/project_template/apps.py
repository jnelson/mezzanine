from django.apps import AppConfig

class StoryMakerConfig(AppConfig):
    name = 'project_template'

    def ready(self):
        import signals
        import pages
