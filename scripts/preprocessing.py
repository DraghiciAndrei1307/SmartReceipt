import cv2

#from ocr import ocr


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

def cut_receipt(image_path: str):
    """
    This function is used cut an image after we rotated it.
    """

    # Extract the source image name and the parent folder path of the image_path

    (
        source_image_name,
        parent_folder_path
    ) = extract_source_image_name_and_folder_path(image_path)

    image = cv2.imread(image_path)

    # Convert image to GrayScale

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    edged = cv2.Canny(gray, 20, 30, apertureSize=5, L2gradient=True)

    edged_image_path = (
            parent_folder_path +
            '/edged_image.jpeg'
    )

    cv2.imshow('Canny Edges After Contouring', edged)
    cv2.waitKey(0)

    cv2.imwrite(edged_image_path, edged)

    contours, hierarchy = cv2.findContours(
        edged,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_NONE
    )

    print("Number of Contours Found = " + str(len(contours)))

    print("Hierarchy: " + str(hierarchy))

    contour_areas = []

    for contour in contours:
        contour_areas.append((cv2.contourArea(contour)))

    max_area = max(contour_areas)

    index = contour_areas.index(max_area)

    print("The max area can be found at: " + str(index))

    print("Max area contour=" + str(max(contour_areas)))

    x,y,w,h = cv2.boundingRect(contours[index])

    print("X=" + str(x))
    print("Y=" + str(y))
    print("W=" + str(w))
    print("H=" + str(h))

    cv2.drawContours(image, contours, index, (0, 255, 0), 3)

    cv2.imshow('Contours', image)
    cv2.waitKey(0)

    image = image[y:y+h, x:x+w]

    cv2.imshow('Contours', image)
    cv2.waitKey(0)

if __name__ == '__main__':

    # rotate_90_counter_clockwise("./input_images/image_1_starbucks.jpeg")

    # resize_image("./input_images/image_1_starbucks.jpeg")

    # print(ocr("./input_images/image_1_starbucks.jpeg"))
    # print(ocr("./input_images/image_1_starbucks_rotated_90_counter_clockwise.jpeg"))
    # print(ocr("./input_images/resized_image.jpeg"))

    cut_receipt("./input_images/image_1_starbucks_rotated_90_counter_clockwise.jpeg")
