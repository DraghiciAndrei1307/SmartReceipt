# Links:
# https://www.jaided.ai/easyocr/
# https://stackoverflow.com/questions/40416072/reading-a-file-using-a-relative-path-in-a-python-project
# https://docs.python.org/3/library/os.path.html#os.path.dirname
# https://docs.python.org/3/library/os.path.html#os.path.join
# https://docs.python.org/3/library/os.path.html#os.path.abspath

import easyocr

def ocr(image_path: str) -> str:
    """Simple OCR function to extract text from an image"""

    # Define the Reader object
    reader = easyocr.Reader(['en', 'ro'])

    # Return the text extracted from the image_path
    return reader.readtext(image_path, detail=0)

# if __name__ == "__main__":
#     print(ocr("./input_images/image_2_starbucks.jpeg"))


