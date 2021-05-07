from api import utils
from django.apps import AppConfig
from . import utils

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
        
