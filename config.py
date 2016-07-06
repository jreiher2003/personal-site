import os 

class BaseConfig(object):
    DEBUG = False 
    SECRET_KEY = os.environ['SECRET_KEY']


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False