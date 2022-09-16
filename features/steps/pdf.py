from behave import given
from util_screenshot.pdf import (
    compare_pdf_with_baseline,
)

file_crop_specifications = {"Top": 10, "Bottom": 10, "Left": 10, "Right": 10}

@given("a pdf report")
def compare_pdf(context):
    """
    :type context: behave.runner.Context
    """
    compare_pdf_with_baseline(context, "redacted.pdf", file_crop_specifications)
