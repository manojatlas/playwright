import logging
import os
import shutil

from pdf2image import convert_from_path

from features.environment import PROJECT_ROOT
from util_screenshot.imgCompare import compare_screenshots_with_opencv


def convert_pdf_to_image(context, input_pdf_file, output_format="PNG"):
    file_name = input_pdf_file.split(".")[0]
    pdf_convert_output_directory = PROJECT_ROOT / f"pdf_files/out/{file_name}"
    os.makedirs(pdf_convert_output_directory, exist_ok=True)
    pages = convert_from_path(
        PROJECT_ROOT / f"pdf_files/in/{input_pdf_file}",
    )
    for id, page in enumerate(pages):
        page.save(
            f"{pdf_convert_output_directory}/{file_name}_{id}.png",
            output_format,
        )
    # if pdf file is baseline, move converted files to baseline directory
    if ("baseline" in context.feature.tags) or ("baseline" in context.scenario.tags):
        shutil.rmtree(PROJECT_ROOT / f"pdf_files/baseline/{file_name}", ignore_errors=True)
        shutil.copytree(
            pdf_convert_output_directory,
            PROJECT_ROOT / f"pdf_files/baseline/{file_name}",
        )
        shutil.rmtree(pdf_convert_output_directory, ignore_errors=True)


def compare_pdf_file(baseline_folder, test_folder, file_crop_specifications=None):
    """Compare a PDF file with it's baseline document.

    :param baseline_folder: Baseline folder name
    :type baseline_folder: str
    :param test_folder: Test folder name
    :type test_folder: str
    :param file_crop_specifications: Portion of page to be cropped. eg.  {"Top": 10, "Bottom": 10, "Left": 10, "Right": 10}
    :type file_crop_specifications: dict
    """
    baseline_directory = PROJECT_ROOT / f"pdf_files/baseline/{baseline_folder}"
    test_directory = PROJECT_ROOT / f"pdf_files/out/{test_folder}"
    dir_list = os.listdir(baseline_directory)
    logging.info(f"No of images to compare:{len(dir_list)}")
    logging.info(f"files to compare:{dir_list}")
    for image in dir_list:
        compare_screenshots_with_opencv(baseline_directory, test_directory, image, file_crop_specifications)


def compare_pdf_with_baseline(context, filename, file_crop_specifications=None):
    """Compare a PDF file with it's baseline document.

    :param context: context object
    :type context: behave.runner.Context
    :param filename: PDF file name to compare
    :type filename: str
    :param file_crop_specifications: Portion of page to be cropped. eg.  {"Top": 10, "Bottom": 10, "Left": 10, "Right": 10}
    :type file_crop_specifications: dict
    """
    file_name = filename.split(".")[0]
    convert_pdf_to_image(context, filename, output_format="PNG")
    if ("baseline" in context.feature.tags) or ("baseline" in context.scenario.tags):
        logging.info("Baseline created, No comparison is performed.")
        return
    compare_pdf_file(file_name, file_name, file_crop_specifications)

