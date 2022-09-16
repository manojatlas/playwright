import os
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from util_screenshot.imgCompare import compare_screenshots_with_opencv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
screen_width = 2560
screen_height = 1440
options = Options()
options.add_argument("--headless")

driver = webdriver.Chrome(options=options)
driver.set_window_size(screen_width, screen_height)
output_directory  = "screenshot_test"
filename = "times_home_page"
os.makedirs(output_directory, exist_ok=True)
driver.get("https://timesofindia.indiatimes.com/")
driver.find_element(By.XPATH, "//a[@href='/']").click()
outfile = os.path.join(output_directory, f"{filename}.png")
driver.get_screenshot_as_file(outfile)
compare_screenshots_with_opencv("screenshot_baseline", "screenshot_test", "times_home_page")
driver.quit()