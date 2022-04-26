from django.apps import AppConfig
# for install django-suit
# https://django-suit.readthedocs.io/en/v2/install.html
from suit.apps import DjangoSuitConfig


class MeasurementsConfig(AppConfig):
    name = 'measurements'
    verbose_name = 'Measurement between 2 locations'

class SuiteConfig(DjangoSuitConfig):
    # layout = "horizontal" 
    # vous pouvez utiliser 
    layout = "vertical"
