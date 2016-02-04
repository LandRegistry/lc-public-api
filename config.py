import os


class Config(object):
    DEBUG = False
    APPLICATION_NAME = 'lc-public-api'


class DevelopmentConfig(Config):
    DEBUG = True
    B2B_PROCESSOR_URL = "http://localhost:5002"
    MQ_USERNAME = "mquser"
    MQ_PASSWORD = "mqpassword"
    MQ_HOSTNAME = "localhost"
    MQ_PORT = "5672"


class PreviewConfig(Config):
    B2B_PROCESSOR_URL = "http://localhost:5002"
    MQ_USERNAME = "mquser"
    MQ_PASSWORD = "mqpassword"
    MQ_HOSTNAME = "localhost"
    MQ_PORT = "5672"
