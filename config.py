import os

class Config(object):
    DEBUG = False

class DevelopmentConfig(object):
    DEBUG = True
    B2B_PROCESSOR_URL = "http://localhost:5002"