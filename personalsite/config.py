import os 

class BaseConfig(object):
    DEBUG = False 
    SECRET_KEY = os.environ['SECRET_KEY']
    CACHE_TYPE = "memcached"
    OPEN_WEATHER_MAP = os.environ["OPEN_WEATHER_MAP"]
    GOOGLE_MAPS_API = os.environ["GOOGLE_MAPS_API"]


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False