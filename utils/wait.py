import time

import requests
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException

from utils.env import log


def wait(host: str, port: int, max_attempts: int = 20, sleep_interval: int = 1):
    current_attempts = 0
    status_fetched = False
    status_json = None

    while not status_fetched:
        if current_attempts > max_attempts:
            log.warning(f"Tried maximum number of requetst {max_attempts}.")
            raise TimeoutException
        current_attempts = current_attempts + 1
        try:
            response = requests.get(f"http://{host}:{port}/wd/hub/status")
            status_json = response.json()
            if not status_json["value"]["ready"]:
                log.warning(f"Container is not ready on port {port}; sleeping...")
                time.sleep(sleep_interval)
            else:
                status_fetched = True
        except WebDriverException as e:
            log.warning(e)

    if not status_fetched:
        log.warning(f"Container status was not fetched on port {port}")
        raise TimeoutException
    if status_json and not status_json["status"] == 0:
        log.warning(f"Wrong status value for container on port {port}")
        raise TimeoutException
    if status_json and not status_json["value"]["ready"]:
        log.warning(f"Container is not ready on port {port}")
        raise TimeoutException
