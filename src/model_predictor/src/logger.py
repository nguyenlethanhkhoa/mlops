import logging
import os

from utils import AppConfig


if not os.path.exists(os.environ.get('LOG_PATH')):
    os.mkdir(os.environ.get('LOG_PATH'))

logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")

featureFormatter = logging.Formatter("%(message)s")

ml_log = logging.getLogger('ml')
api_log = logging.getLogger('api')

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(featureFormatter)

fileHandler = logging.FileHandler("{0}/{1}.log".format(
    os.environ.get('LOG_PATH'),
    'log')
)
fileHandler.setFormatter(featureFormatter)

if AppConfig.DEBUG:
    ml_log.setLevel(logging.DEBUG)
    api_log.setLevel(logging.DEBUG)

    ml_log.addHandler(consoleHandler)
    api_log.addHandler(consoleHandler)

else:
    ml_log.setLevel(logging.INFO)
    ml_log.addHandler(fileHandler)
