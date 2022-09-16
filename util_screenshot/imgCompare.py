import os
from datetime import datetime
import cv2
import imutils


def compare_screenshots_with_opencv(
    baseline_folder, test_folder, image_to_compare, file_crop_specifications=None
):
    """Compare an image file with it's baseline image.

    :param baseline_folder: Baseline folder name
    :type baseline_folder: str
    :param test_folder: Test folder name
    :type test_folder: str
    :param image_to_compare: image name
    :type image_to_compare: str
    :param file_crop_specifications: Portion of page to be cropped. eg.  {"Top": 10, "Bottom": 10, "Left": 10, "Right": 10}
    :type file_crop_specifications: dict
    """
    dir1 = baseline_folder
    dir2 = test_folder
    if len(image_to_compare.split(".")) > 1 and not image_to_compare.split(".")[1] in [
        "png",
        None,
    ]:
        raise RuntimeError("Cannot process non PNG image as of now.")
    image_to_compare = f"{image_to_compare.split('.')[0]}.png"

    outputdir = "screenshot_diff/compresult_" + datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs(outputdir, exist_ok=True)

    # for filename in os.listdir(dir1):
    if image_to_compare in os.listdir(dir1) and os.listdir(dir2):
        file1 = os.path.join(dir1, image_to_compare)
        file2 = os.path.join(dir2, image_to_compare)

        # get the images you want to compare.
        original = cv2.imread(file1)
        new = cv2.imread(file2)
        # resize the images to make them small in size. A bigger size image may take a significant time
        # more computing power and time
        original = imutils.resize(original, height=600)
        new = imutils.resize(new, height=600)

        original = cropped_image_shape(original, file_crop_specifications)
        new = cropped_image_shape(new, file_crop_specifications)
        cv2.imwrite("Cropped Image1.jpg", original)

        # create a copy of original image so that we can store the
        # difference of 2 images in the same on
        diff = original.copy()
        cv2.absdiff(original, new, diff)

        # converting the difference into grayscale images
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

        # increasing the size of differences after that we can capture them all
        for i in range(0, 3):
            dilated = cv2.dilate(gray.copy(), None, iterations=i + 1)

        # threshold the gray image to binary it. Anything pixel that has
        # value higher than 3 we are converting to white
        # (remember 0 is black and 255 is exact white)
        # the image is called binarised as any value lower than 3 will be 0 and
        # all of the values equal to and higher than 3 will be 255
        (T, thresh) = cv2.threshold(dilated, 3, 255, cv2.THRESH_BINARY)

        # now we have to find contours in the binarized image
        cnts = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        print(f"Number of countours : {len(cnts)}")

        for c in cnts:
            # nicely fiting a bounding box to the contour
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(new, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # remove comments from below 2 lines if you want to
        # for viewing the image press any key to continue
        # simply write the identified changes to the disk

        if len(cnts):
            outpath = outputdir + "/" + image_to_compare + "-s.png"
            print(
                " [\033[91m\u2717\033[0m] Images ("
                + image_to_compare
                + ") are different, store difference in "
                + outpath
            )
            cv2.imwrite(f"{outputdir}/{image_to_compare.split('.')[0]}_diff.png", new)
            return False
        else:
            print(
                " [\033[92m\N{check mark}\033[0m] Images ("
                + image_to_compare
                + ") are equal"
            )
            return True
    else:
        print(f"File {image_to_compare} does not exist in both folder.")
        return FileNotFoundError


def cropped_image_shape(image, file_crop_specifications):
    """Crop the images to provided specification

    :param image: image name
    :type image: numpy.ndarray
    :param file_crop_specifications: Portion of page to be cropped. eg.  {"Top": 10, "Bottom": 10, "Left": 10, "Right": 10}
    :type file_crop_specifications: dict
    :return:image
    :rtype: numpy.ndarray
    """
    shape = image.shape
    if not file_crop_specifications:
        return image
    resize_dim_top, resize_dim_bottom, resize_dim_left, resize_dim_right = (
        0,
        shape[0],
        0,
        shape[1],
    )
    for key, value in file_crop_specifications.items():
        if key == "Top":
            resize_dim_top = int(shape[0] * get_percentage(value))
        if key == "Bottom":
            resize_dim_bottom = int(shape[0] - shape[0] * get_percentage(value))
        if key == "Left":
            resize_dim_left = int(shape[1] * get_percentage(value))
        if key == "Right":
            resize_dim_right = int(shape[1] - shape[1] * get_percentage(value))

    return image[resize_dim_top:resize_dim_bottom, resize_dim_left:resize_dim_right]


def get_percentage(num):
    """Get percentage value"""
    return num / 100
