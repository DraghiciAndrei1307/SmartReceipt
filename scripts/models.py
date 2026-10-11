# ===================== LOGIC ============================

# preprocessing -> ocr -> models

# Sample output after this operation

# [
#   {
#     "text": "LAPTE",
#     "confidence": 0.97,
#     "box": [120, 340, 250, 375]
#   },
#   {
#     "text": "7.49",
#     "confidence": 0.95,
#     "box": [500, 340, 570, 375]
#   }
# ]

# ========================================================

from preprocessing import preprocess
from ocr import ocr

def create_ocr_model(image_path: str) -> list[dict]:
    """
    This function creates OCR model based on the OCR output.
    The OCR model will help us create the parser.
    """

    # Preprocess the image
    cut_image = preprocess(image_path)

    # Apply OCR
    ocr_raw_result = ocr(cut_image)

    ocr_model_list = []

    for bbox, text, confidence in ocr_raw_result:
        ocr_model_list.append(
            {
                "bbox": bbox,
                "text": text,
                "confidence": float(confidence),
            }
        )

    return ocr_model_list


if __name__ == "__main__":

    print(create_ocr_model("./input_images/image_1_jumbo.jpeg"))
