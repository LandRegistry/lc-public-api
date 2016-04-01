import os


class Config(object):
    APPLICATION_NAME = 'lc-public-api'
    DEBUG = os.getenv('DEBUG', True)
    AMQP_URI = os.getenv("AMQP_URI", "amqp://mquser:mqpassword@localhost:5672")
    B2B_PROCESSOR_URL = os.getenv('AUTOMATIC_PROCESS_URL', 'http://localhost:5002')
