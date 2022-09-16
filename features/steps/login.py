import time


from applitools.selenium import Target
from behave import given, then, when
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By


from util_screenshot.files import set_output_file
from util_screenshot.imgCompare import compare_screenshots_with_opencv

from seleniumbase import get_driver
from seleniumbase.fixtures import base_case
from seleniumbase import js_utils
from seleniumbase import page_actions
from seleniumbase import BaseCase



@given("a user wants to access the application")
def dummy_step(context):
    pass


@then("they are able to access the application")
def check_login_page(context):
    """
    :type context: behave.runner.Context
    """
    context.eyes.open(
        context.driver,
        "Gateway Webui app",
        "Login Page test",
        {"width": 800, "height": 600},
    )
    # Visual checkpoint #1.
    context.eyes.check("Login Window test", Target.window())
    # End the test.
    context.eyes.close(False)


@then("they check application layout and compare with baseline")
def compare_login_page_with_baseline(context):
    """
    :type context: behave.runner.Context
    """
    filename = "gateway_home_page"
    output_directory, baseline_directory, outfile = set_output_file(context, filename)
    context.driver.find_element(By.ID, "input-login-username").send_keys(
        Keys.CONTROL + "a"
    )
    context.driver.find_element(By.ID, "input-login-username").send_keys(Keys.DELETE)
    time.sleep(2)
    context.driver.get_screenshot_as_file(outfile)
    assert compare_screenshots_with_opencv(
        baseline_directory, output_directory, filename
    ), "Screenshot does not match with baseline "


@when("they enter a {correct_username} and {correct_password}")
def enter_login(context, correct_username: str, correct_password: str):
    supported_usernames = {
        "correct username": "admin",
        "incorrect username": "DUMMY",
    }
    name = supported_usernames[correct_username]
    supported_passwords = {
        "correct password": "admin",
        "incorrect password": "DUMMYPASS",
    }
    password = supported_passwords[correct_password]
    context.driver.find_element(By.ID, "input-login-username").send_keys(
        Keys.CONTROL + "a"
    )
    context.driver.find_element(By.ID, "input-login-username").send_keys(Keys.DELETE)
    context.driver.find_element(By.ID, "input-login-username").send_keys(name)
    context.driver.find_element(By.ID, "input-login-password").send_keys(password)
    context.driver.find_element(By.ID, "button-login-login").click()


@then("they are able to validate the login page")
def visual_test_login_page(context):
    """
    :type context: behave.runner.Context
    """
    # context.sb_driver = get_driver("chrome", headless=False)
    # context.sb_driver.get("https://seleniumbase.io/apps/calculator")
    # context.sb_driver.check_window(name="helloworld", baseline=True)
    # context.sb_driver.check_window(name="helloworld", level=3)
    context.bs = BaseCase().go_to("https://seleniumbase.io/apps/calculator")
    get_driver("chrome", headless=False)




