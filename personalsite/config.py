import os 

class BaseConfig(object):
    DEBUG = False 
    SECRET_KEY = os.environ['SECRET_KEY']
    OPEN_WEATHER_MAP = os.environ["OPEN_WEATHER_MAP"]


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False