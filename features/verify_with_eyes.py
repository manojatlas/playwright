import os

from applitools.selenium import Target
from behave import use_fixture
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from util_screenshot.eyes import get_eyes, eyes

screen_width = 2560
screen_height = 1440
options = Options()
options.add_argument("--headless")

context.driver = webdriver.Chrome(options=options)
driver.set_window_size(screen_width, screen_height)
output_directory  = "screenshot_test"
filename = "times_home_page"
os.makedirs(output_directory, exist_ok=True)
use_fixture(get_eyes)
eyes.open(driver, "Test app", "First test", {"width": 800, "height": 600})
driver.get("https://timesofindia.indiatimes.com/")
# Visual checkpoint #1.
eyes.check("Login Window test", Target.window())

# End the test.
eyes.close(False)
driver.quit()