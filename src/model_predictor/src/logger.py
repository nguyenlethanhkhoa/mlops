import logging
import os

from utils import AppConfig


if not os.path.exists(os.environ.get("LOG_PATH")):
    os.mkdir(os.environ.get("LOG_PATH"))

logFormatter = logging.Formatter(
    "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s"
)

featureFormatter = logging.Formatter("%(message)s")

model_1_log = logging.getLogger("ml")
model_2_log = logging.getLogger("ml2")
api_log = logging.getLogger("api")

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(featureFormatter)

fileHandler_1 = logging.FileHandler(
    "{0}/model_1.log".format(os.environ.get("LOG_PATH"), "log")
)

fileHandler_2 = logging.FileHandler(
    "{0}/model_2.log".format(os.environ.get("LOG_PATH"), "log")
)

fileHandler_1.setFormatter(featureFormatter)
fileHandler_2.setFormatter(featureFormatter)

model_1_log.setLevel(logging.INFO)
model_1_log.addHandler(fileHandler_1)

model_2_log.setLevel(logging.INFO)
model_2_log.addHandler(fileHandler_2)


model_1_log.addHandler(consoleHandler)
api_log.addHandler(consoleHandler)
