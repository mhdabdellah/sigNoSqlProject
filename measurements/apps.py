from django.apps import AppConfig
# pip install https://github.com/darklow/django-suit/tarball/v2
# from suit.apps import DjangoSuiteConfig


class MeasurementsConfig(AppConfig):
    name = 'measurements'
    verbose_name = 'Measurement between 2 locations'

# class SuiteConfig(DjangoSuiteConfig):
#     layout = "horizontal" 
    # vous pouvez utiliser layout = "vertical"
