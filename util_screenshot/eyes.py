import os

from applitools.common import BatchInfo
from applitools.selenium import Eyes, Target
from behave import fixture
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

screen_width = 2560
screen_height = 1440
options = Options()
options.add_argument("--headless")

driver = webdriver.Chrome(options=options)
driver.set_window_size(screen_width, screen_height)
output_directory  = "screenshot_test"
filename = "times_home_page"
os.makedirs(output_directory, exist_ok=True)
# Start the test and set the browser's viewport size to 800x600.
eyes = Eyes()
# Initialize the eyes SDK and set your private API key.
eyes.api_key = "VAZwJRXDArRHGhrOH2XvYdmZfcwtn05vpmt8Fn7IZeE110"
eyes.configure.batch = BatchInfo("Some general Test cases name")

eyes.open(driver, "Test app", "First test", {"width": 800, "height": 600})
# Navigate the browser to the "hello world!" web-site.
driver.get("https://demo.applitools.com")

# Visual checkpoint #1.
eyes.check("Login Window test", Target.window())

# End the test.
eyes.close(False)

