import cv2
import numpy as np

from scripts.ocr import ocr
from scripts.preprocessing import (
    gaussian_blur,
    cut_using_canny,
    cut_using_thresholding,
    fine_deskew,
    thresh
)

def new_preprocessing(image_path: str):
    """
    We will apply the following preprocessing steps:
    - Gaussian Blur
    - Canny Edge Detection
    """

    # Apply Canny Edge Detection and cut the image...

    cut_image, cut_image_path = cut_using_thresholding(image_path)

    # Apply deskewing
    deskew_image, deskew_path = fine_deskew(cut_image_path)

    # Apply thresholding
    final_thresh_image, final_thresh_path = thresh(deskew_path)

    # Apply OCR
    extracted_text = ocr(final_thresh_path)

    print("\n--- TEXT EXTRAS FINAL ---")
    print(extracted_text)
    print("---")

    return cut_image, cut_image_path


if __name__ == '__main__':

    result_image, result_image_path = new_preprocessing("./input_images/demo_live.jpeg")


