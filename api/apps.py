from api import utils
from django.apps import AppConfig
from . import utils

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
    def ready(self):
        global en_classifier, th_classifier
        en_classifier = utils.DepressClassifier("en")
        th_classifier = utils.DepressClassifier("th")
