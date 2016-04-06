from flask import Flask
import os
from log.logger import setup_logging
import logging

app = Flask(__name__)
app.config.from_object('config.Config')

setup_logging(app.config)


logging.info('================================')
logging.info(os.getenv('AUTOMATIC_PROCESS_URL', 'AUTOMATIC_PROCESS_URL NOT SET'))
logging.info('================================')