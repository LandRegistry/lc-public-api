import os


class Config(object):
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    B2B_PROCESSOR_URL = "http://localhost:5002"


class PreviewConfig(Config):
    B2B_PROCESSOR_URL = "http://localhost:5002"
