# Links:
# https://www.jaided.ai/easyocr/
# https://stackoverflow.com/questions/40416072/reading-a-file-using-a-relative-path-in-a-python-project
# https://docs.python.org/3/library/os.path.html#os.path.dirname
# https://docs.python.org/3/library/os.path.html#os.path.join
# https://docs.python.org/3/library/os.path.html#os.path.abspath

import os

import easyocr

image_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        '..',
        'input_images',
        'image_2_starbucks.jpeg'
    )
)

reader = easyocr.Reader(['en', 'ro'])

result = reader.readtext(image_path, detail=0)

print(result)
