import logging

from features.environment import PROJECT_ROOT
from utils.env import log

LOG_PATH = PROJECT_ROOT / "report" / "behave.log"
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")
log.setLevel(logging.INFO)
logging.getLogger("requests").setLevel(logging.INFO)
logging.getLogger("urllib3").setLevel(logging.INFO)
logging.getLogger("selenium").setLevel(logging.INFO)

fileHandler = logging.FileHandler(LOG_PATH)
fileHandler.setFormatter(logFormatter)
log.addHandler(fileHandler)
