"""This module is use to run Behave scenario in local.

Utilities
* Can run more than one scenario together
* Store scenario test result in JSON and show it into HTML tabular format
    (Test case status, scenario name and error log.)
* Debug the BDD scenario
"""

import os
import shutil
import glob
import sys
from json2html import json2html
from behave import __main__ as runner_with_options

if __name__ == "__main__":
    sys.stdout.flush()

    # set env var
    os.environ["HARDWARE"] = "GATEWAY"
    os.environ["ENVIRONMENT"] = "local"
    os.environ["BROWSERS"] = "Chrome"
    os.environ["SELENIUM_DRIVER_NAME"] = "chrome"
    os.environ["SELENIUM_TARGET_HOST"] = "192.168.59.20"
    os.environ["SELENIUM_TARGET_IP"] = "192.168.59.20"
    os.environ["SELENIUM_TARGET_PORT"] = "8080"
    os.environ["WINDOW_SIZE"] = "1920x1080"
    os.environ["APPLITOOLS_API_KEY"] = "VAZwJRXDArRHGhrOH2XvYdmZfcwtn05vpmt8Fn7IZeE110"

    REPORT_DIR = "reports"
    SCREENSHOTS_DIR = "./screenshots"

    # remove if any reporting folder exists
    shutil.rmtree(REPORT_DIR, ignore_errors=True)

    # remove if any screenshots folder exists
    shutil.rmtree(SCREENSHOTS_DIR, ignore_errors=True)

    # allure reporting related command line arguments
    REPORT_RELATED = (
        " -f allure_behave.formatter:AllureFormatter -o " + REPORT_DIR + "  "
    )

    # run Behave + BDD + Python code
    TAGS_OPTION = "-t {}".format("@GWUAT-4")
    FEATURE_FILE_PATH = "./features/login/login.feature"
    COMMON_RUNNER_OPTIONS = " --no-capture --no-capture-stderr -f plain "
    FULL_RUNNER_OPTIONS = (
        FEATURE_FILE_PATH
        + REPORT_RELATED
        + COMMON_RUNNER_OPTIONS
        + TAGS_OPTION
    )
    runner_with_options.main(FULL_RUNNER_OPTIONS)

    # read resultant json file
    LIST_OF_JSON = glob.glob(REPORT_DIR + "/*.json")
    FINAL_JSON = ""
    for cnt in range(0, len(LIST_OF_JSON)):
        LIST_OF_JSON[cnt] = (
            ' {"'
            + "Scenario_"
            + str(cnt)
            + '"'
            + " : "
            + open(LIST_OF_JSON[cnt], "r").read()
            + "}"
        )
        if cnt < (-1 + len(LIST_OF_JSON)):
            LIST_OF_JSON[cnt] = LIST_OF_JSON[cnt] + ","
        FINAL_JSON = FINAL_JSON + LIST_OF_JSON[cnt]
    FINAL_JSON = "[ " + FINAL_JSON + " ]"

    # convert json to html using simple utility and publish report
    HTML_CONTENT = json2html.convert(json=FINAL_JSON)
    HTML_REPORT_FILE = open(REPORT_DIR + "/" + "HMI_behave_report.html", "w")
    HTML_REPORT_FILE.write(HTML_CONTENT)
    HTML_REPORT_FILE.close()
