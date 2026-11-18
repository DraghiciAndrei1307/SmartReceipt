# ===================== LOGIC ============================

# preprocessing -> ocr -> models

# Sample output after this operation

# [
#   {
#     "text": "LAPTE",
#     "confidence": 0.97,
#     "bbox": [120, 340, 250, 375]
#   },
#   {
#     "text": "7.49",
#     "confidence": 0.95,
#     "bbox": [500, 340, 570, 375]
#   }
# ]

# ========================================================

# =================================================
#           IMPORTS...
# =================================================

from scripts.receipt_preprocessor import ReceiptPreprocessor
from scripts.ocr import tesseract_ocr
#from scripts.ocr import ocr

# =================================================
#           CREATE OCR MODEL FUNCTION...
# =================================================

def create_ocr_model(image_path: str) -> list[dict]:
    """
    This function creates OCR model based on the OCR output.
    The OCR model will help us create the parser.
    """

    # Create an instance of the ReceiptPreprocessor class...
    receipt_preprocessor_instance = ReceiptPreprocessor()

    # APPLY WARPING (on the original gray image)
    warped_image, warped_image_path = receipt_preprocessor_instance.factory.operation(
        operation_applied=receipt_preprocessor_instance.factory.WARP,
        image_path="./input_images/image_1_lidl.jpeg"
    )

    # DESKEW IMAGE...
    _, deskew_path = receipt_preprocessor_instance.factory.operation(
        operation_applied=receipt_preprocessor_instance.factory.DESKEW,
        image_path=warped_image_path
    )

    # RESIZE IMAGE...
    _, resized_image_path = receipt_preprocessor_instance.factory.operation(
        operation_applied=receipt_preprocessor_instance.factory.RESIZE,
        image_path=deskew_path
    )

    # APPLY ADAPTIVE THRESHOLDING...

    _, thresholded_image_path = receipt_preprocessor_instance.factory.operation(
        operation_applied=receipt_preprocessor_instance.factory.ADAPTIVE_THRESHOLDING,
        image_path=resized_image_path
    )

    # Apply Tesseract
    ocr_raw_result = tesseract_ocr(thresholded_image_path)

    print("OCR_RAW_RESULT: " + str(ocr_raw_result))

    ocr_model_list = []

    for bbox, text, confidence in ocr_raw_result:
        ocr_model_list.append(
            {
                "bbox": [
                    [int(point[0]), int(point[1])]
                    for point in bbox
                ],
                "text": text,
                "confidence": round(float(confidence),2),
            }
        )

    return ocr_model_list


if __name__ == "__main__":

    print(create_ocr_model("./input_images/image_1_jumbo.jpeg"))
