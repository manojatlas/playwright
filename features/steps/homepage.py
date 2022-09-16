import time

from behave import then
from selenium.webdriver.common.by import By
from util_screenshot.files import set_output_file
from util_screenshot.imgCompare import compare_screenshots_with_opencv


@then("they validate header on the landing page")
def validate_home_page_header(context):
    """
    :type context: behave.runner.Context
    """
    filename = "home_header_page"
    output_directory, baseline_directory, outfile = set_output_file(context, filename)
    time.sleep(2)
    context.driver.find_element(By.XPATH, "//header[@class = 'ant-layout-header header']").screenshot(outfile)
    assert compare_screenshots_with_opencv(
        baseline_directory, output_directory, filename
    ), "Screenshot does not match with baseline."
