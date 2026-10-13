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

from scripts.preprocessing import (
    preprocess_using_thresholding,
    preprocess_using_canny,
    grayscale,
    thresh
)
from scripts.ocr import ocr

def create_ocr_model(image_path: str) -> list[dict]:
    """
    This function creates OCR model based on the OCR output.
    The OCR model will help us create the parser.
    """

    # PREPROCESS THE IMAGE  (GRAY -> THRESHOLDING -> CUT -> RESIZE)
    (
        preprocessed_image,
        preprocessed_image_path
    ) = preprocess_using_thresholding(image_path)

    # PREPROCESS THE IMAGE (CANNY -> CUT -> RESIZE)
    # (
    #     preprocessed_image,
    #     preprocessed_image_path
    # ) = preprocess_using_canny(image_path)

    # Apply OCR
    ocr_raw_result = ocr(preprocessed_image_path)

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
