import os


class Config(object):
    APPLICATION_NAME = 'lc-public-api'
    DEBUG = os.getenv('DEBUG', True)
    MQ_USERNAME = os.getenv("MQ_USERNAME", "mquser")
    MQ_PASSWORD = os.getenv("MQ_PASSWORD", "mqpassword")
    MQ_HOSTNAME = os.getenv("MQ_HOST", "localhost")
    MQ_PORT = os.getenv("MQ_PORT", "5672")
    B2B_PROCESSOR_URL = os.getenv('AUTOMATIC_PROCESS_URL', 'http://localhost:5002')
