import logging

from src.model_predictor.src.utils import AppConfig

logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")

ml_log = logging.getLogger('ml')
api_log = logging.getLogger('api')

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)

if AppConfig.DEBUG:
    ml_log.setLevel(logging.DEBUG)
    api_log.setLevel(logging.DEBUG)

    ml_log.addHandler(consoleHandler)
    api_log.addHandler(consoleHandler)

else:
    pass
