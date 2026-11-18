"""
This module contains the functions that apply different OCR
technologies that we use in our code...
"""

# =================================================
#           DOCUMENTATION...
# =================================================
# Links:
# https://www.jaided.ai/easyocr/
# https://stackoverflow.com/questions/40416072/reading-a-file-using-a-relative-path-in-a-python-project
# https://docs.python.org/3/library/os.path.html#os.path.dirname
# https://docs.python.org/3/library/os.path.html#os.path.join
# https://docs.python.org/3/library/os.path.html#os.path.abspath

# =================================================
#           IMPORTS...
# =================================================
import cv2
import easyocr
import pytesseract
from pytesseract import Output

# =================================================
#           EasyOCR FUNCTION...
# =================================================
def ocr(image_path: str) -> list:
    """Simple OCR function to extract text from an image"""

    # Define the Reader object
    reader = easyocr.Reader(['en', 'ro'])

    # Return the text extracted from the image_path
    return reader.readtext(image_path)

# =================================================
#           TESSERACT OCR FUNCTION...
# =================================================
def tesseract_ocr(image_path: str) -> list:
    """
    Simple OCR function to extract text from an image,
    using tesseract and pytesseract...
    """

    # Set the PATH to the 'tesseract.exe'...
    pytesseract.pytesseract.tesseract_cmd = (
        r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    )

    # Read the image
    image = cv2.imread(image_path)

    # Convert from BGR (OpenCV) into RGB (Tesseract)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Extract text
    data = pytesseract.image_to_data(rgb_image, lang='ron+eng', output_type=Output.DICT)

    ocr_results = []
    n_boxes = len(data['text'])

    for i in range(n_boxes):
        text = data['text'][i].strip()

        # Ignore the empty lines or empty spaces accidentally detected...
        if text:
            # Normalize the 'confidence' from Tesseract between 0 and 1
            conf = float(data['conf'][i]) / 100.0
            if conf < 0:
                conf = 0.0

            x = data['left'][i]
            y = data['top'][i]
            w = data['width'][i]
            h = data['height'][i]

            # Create the 4-corner format (the bbox) which the parser will use next...
            bbox = [
                [x, y],  # upper-left
                [x + w, y],  # upper-right
                [x + w, y + h],  # lower-right
                [x, y + h]  # lower-left
            ]

            ocr_results.append((bbox, text, conf))

    return ocr_results
