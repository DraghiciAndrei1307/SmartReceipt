import cv2

from ocr import ocr

def extract_source_image_name_and_folder_path(image_path: str):
    """
    This function extracts the source image name,
    and its parent folder path.
    """

    splitted_image_path = image_path.split('/')

    return splitted_image_path[-1], "/".join(splitted_image_path[:-1])

def rotate_90_counter_clockwise(image_path: str):
    """
    This function rotates 90 degree
    counterclockwise around the origin.
    """

    # Extract the source image name and the parent folder path of the image_path
    (
        source_image_name,
        source_image_folder_path
    ) = extract_source_image_name_and_folder_path(image_path)

    # Read image from image_path, using cv2.imread(...)
    image = cv2.imread(image_path)

    # Rotate image counterclockwise with 90 degrees around the origin
    rotated_image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)

    # Generate rotated image new path
    rotated_image_path = (
            source_image_folder_path +
            '/' +
            source_image_name.split(".")[0] +
            "_rotated_90_counter_clockwise." +
            source_image_name.split(".")[1]
    )

    # Save rotated image
    cv2.imwrite(rotated_image_path, rotated_image)

    # We return the rotated image path and its parent folder path.
    # For the moment, we keep everything inside the same folder.
    return rotated_image, rotated_image_path, source_image_folder_path

def resize_image(image_path: str):
    """This function is used resize an image."""

    # Rotate image with 90 degrees counterclockwise around the origin
    (
        rotated_image,
        rotated_image_path,
        parent_folder_path
    ) = rotate_90_counter_clockwise(image_path)

    # Resize using specific scale factors on both X and Y axis

    resized_image = cv2.resize(
        rotated_image,
        dsize=None,
        fx=3,
        fy=1.5,
        interpolation=cv2.INTER_CUBIC
    )

    resized_image_path = (
            parent_folder_path +
            '/resized_image.jpeg'
    )

    cv2.imwrite(resized_image_path, resized_image)

if __name__ == '__main__':

    # rotate_90_counter_clockwise("./input_images/image_1_starbucks.jpeg")

    # resize_image("./input_images/image_1_starbucks.jpeg")

    print(ocr("./input_images/image_1_starbucks.jpeg"))
    print(ocr("./input_images/image_1_starbucks_rotated_90_counter_clockwise.jpeg"))
    print(ocr("./input_images/resized_image.jpeg"))
