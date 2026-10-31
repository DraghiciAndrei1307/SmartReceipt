# Links:
# https://www.jaided.ai/easyocr/
# https://stackoverflow.com/questions/40416072/reading-a-file-using-a-relative-path-in-a-python-project
# https://docs.python.org/3/library/os.path.html#os.path.dirname
# https://docs.python.org/3/library/os.path.html#os.path.join
# https://docs.python.org/3/library/os.path.html#os.path.abspath
import cv2
import easyocr
import pytesseract
from pytesseract import Output


def ocr(image_path: str) -> list:
    """Simple OCR function to extract text from an image"""

    # Define the Reader object
    reader = easyocr.Reader(['en', 'ro'])

    # Return the text extracted from the image_path
    return reader.readtext(image_path)

def tesseract_ocr(image_path: str) -> list:

    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

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

        # Ignorăm liniile goale sau spațiile albe detectate accidental
        if text:
            # Tesseract dă confidența de la 0 la 100. O aducem între 0 și 1.
            conf = float(data['conf'][i]) / 100.0
            if conf < 0:
                conf = 0.0

            x = data['left'][i]
            y = data['top'][i]
            w = data['width'][i]
            h = data['height'][i]

            # Construim formatul de 4 colțuri (bbox) pe care îl folosește parserul tău
            bbox = [
                [x, y],  # Stânga-sus
                [x + w, y],  # Dreapta-sus
                [x + w, y + h],  # Dreapta-jos
                [x, y + h]  # Stânga-jos
            ]

            ocr_results.append((bbox, text, conf))

    return ocr_results

# if __name__ == "__main__":
#     print(ocr("./input_images/image_2_starbucks.jpeg"))


