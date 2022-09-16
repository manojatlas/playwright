import json
import os
from pathlib import Path

import polling
import requests
from allure_commons._allure import attach
from allure_commons.types import AttachmentType
from applitools.common import BatchInfo
from applitools.selenium import Eyes
from behave import fixture
from behave import use_fixture
from behave import use_step_matcher
from behave.model_core import Status
from requests import codes
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

from utils.env import get_from_env, log
from utils.env import get_window_size

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Currently facing issue with cfparse, once the issue is resolved we will revert to cfparse
use_step_matcher("parse")


def wait_for_remote_driver():
    hub_host = os.getenv("SELENIUM_HUB_HOST")
    hub_port = os.getenv("SELENIUM_HUB_PORT")
    log.debug(
        f"Waiting for remote hub (at {hub_host}:{hub_port}) " f"to become ready..."
    )

    def is_ready(host, port):
        log.debug("Querying hub...")
        try:
            response = requests.get(f"http://{host}:{port}/wd/hub/status")
            if response.status_code == codes.ok:
                return response.json()["value"]["ready"]
        except requests.exceptions.ConnectionError as ce:
            msg = (
                f"Network problem: {ce}, failed to establish connection at "
                f"{hub_host}:{hub_port}."
            )
            log.info(msg)
        return False

    try:
        polling.poll(lambda: is_ready(hub_host, hub_port), step=1, timeout=60)
    except polling.TimeoutException as te:
        message = (
            f"Could not get access to driver via the hub at " f"{hub_host}:{hub_port}."
        )
        log.error(message)
        raise TimeoutError(message) from te

    log.debug(f"The hub (at {hub_host}:{hub_port}) is ready.")


def set_window_size(context):
    window_size = get_window_size()
    context.driver.set_window_size(window_size[0], window_size[1])


@fixture
def selenium_browser_docker(context):
    browsers = get_from_env("BROWSERS").split(",")
    supported_browsers = {
        "Chrome": DesiredCapabilities.CHROME,
        "Firefox": DesiredCapabilities.FIREFOX,
        "Opera": DesiredCapabilities.OPERA,
    }

    log.debug("Waiting for hub to become ready.")
    wait_for_remote_driver()
    capabilities = supported_browsers[browsers[0]]
    context.driver = webdriver.Remote(
        command_executor="http://selenium_hub:4444/wd/hub",
        desired_capabilities=capabilities,
    )
    set_window_size(context)

    log.debug("Browser is ready.")
    yield context.driver
    context.driver.quit()


@fixture
def selenium_browser_local(context):
    browsers = get_from_env("BROWSERS").split(",")
    # We don't actually want to start up those webdrivers
    supported_browsers = {
        "Chrome": webdriver.Chrome,
        "Firefox": webdriver.Firefox,
        "Opera": webdriver.Opera,
    }

    log.debug("Starting browser locally.")
    context.driver = supported_browsers[browsers[0]]()
    set_window_size(context)

    log.debug("Browser is ready.")
    yield context.driver
    context.driver.quit()


@fixture
def get_eyes(context):
    context.eyes = Eyes()
    # Initialize the eyes SDK and set your private API key.
    context.eyes.api_key = context.APPLITOOLS_API_KEY
    context.eyes.configure.batch = BatchInfo("Some general Test cases name")
    yield context.eyes
    # If the test was aborted before eyes.close was called, ends the test as aborted.
    context.eyes.abort_if_not_closed()


def before_scenario(context, scenario):
    environment = get_from_env("ENVIRONMENT")
    supported_environments = {
        "docker": selenium_browser_docker,
        "local": selenium_browser_local,
    }
    use_fixture(supported_environments[environment], context)
    # Delete all cookies before scenario
    context.driver.delete_all_cookies()
    # Reset Scenario context data dict
    context.vars = {}
    context.target_ip = get_from_env("SELENIUM_TARGET_IP")
    context.APPLITOOLS_API_KEY = get_from_env("APPLITOOLS_API_KEY")
    use_fixture(get_eyes, context)
    # context.driver.get(f"http://{context.target_ip}")
    # log.debug("Went to homepage")


def after_scenario(context, scenario):
    """Attach a screenshot and browser console logs if scenario is failed.

    :param context: behave.runner.Context
    :param scenario: behave scenario
    """
    # Scenario context variable
    context_variable_dict = {key: str(value) for key, value in context.vars.items()}
    context_logs = json.dumps(context_variable_dict)
    attach(
        context_logs,
        name="Context variable",
        attachment_type=AttachmentType.JSON,
    )

    if scenario.status == Status.failed:
        # Screenshot
        attach(
            context.driver.get_screenshot_as_png(),
            name=scenario.name,
            attachment_type=AttachmentType.PNG,
        )

        # Browser Console Log
        browser_logs = json.dumps(context.driver.get_log("browser"), indent=4)
        attach(
            browser_logs,
            name="Browser Console Log",
            attachment_type=AttachmentType.JSON,
        )

        # Network & Page domain events logs.
        if os.getenv("BROWSER_NETWORK_LOGS") == "true":
            performance_logs = json.dumps(
                context.driver.get_log("performance"), indent=4
            )
            attach(
                performance_logs,
                name="Network & Page domain events logs",
                attachment_type=AttachmentType.JSON,
            )
