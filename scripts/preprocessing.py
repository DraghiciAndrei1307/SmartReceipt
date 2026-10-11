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

def rotate_90_counter_clockwise_and_resize_image(image_path: str):
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
            '/rotated_90_counterclockwise_and_resized.jpeg'
    )

    cv2.imwrite(resized_image_path, resized_image)

def resize_image(image_path: str):
    # Extract the source image name and the parent folder path of the image_path
    (
        source_image_name,
        source_image_folder_path
    ) = extract_source_image_name_and_folder_path(image_path)

    # Read image from image_path, using cv2.imread(...)
    image = cv2.imread(image_path)

    # Resize using specific scale factors on both X and Y axis

    resized_image = cv2.resize(
        image,
        dsize=None,
        fx=3,
        fy=1.5,
        interpolation=cv2.INTER_CUBIC
    )

    resized_image_path = (
            source_image_folder_path +
            '/'+
            source_image_name.split(".")[0] +
            '_resized_image.jpeg'
    )

    cv2.imwrite(resized_image_path, resized_image)

def convert_to_grayscale(image):
    """This function is used convert an image to grayscale."""
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def apply_threshold(image):
    """This function is used apply a threshold to an image."""
    _, thresh = cv2.threshold(
        image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    return thresh

def show_and_write_image(
        parent_folder_path: str,
        source_image_name: str,
        operation_applied: str,
        image
):
    """This function is used construct path (for writing), show and write an image."""

    # Construct the string with path where we will write image
    result_image_path = (
            parent_folder_path +
            '/' + source_image_name.split(".")[0] +
            "_" +
            operation_applied +
            "_image.jpeg"
    )

    # Show the image and destroy it after user presses key
    cv2.imshow(operation_applied.title() + ' image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Write the image at the desired path
    cv2.imwrite(result_image_path, image)


def cut_receipt(image_path: str):
    """
    This function is used cut an image after we rotated it.
    """

    # Extract the source image name and the parent folder path of the image_path

    (
        source_image_name,
        parent_folder_path
    ) = (
        extract_source_image_name_and_folder_path(image_path)
    )

    image = cv2.imread(image_path)

    # Convert image to GrayScale

    gray = convert_to_grayscale(image)

    show_and_write_image(
        parent_folder_path=parent_folder_path,
        source_image_name=source_image_name,
        operation_applied="gray",
        image=gray
    )

    # Apply Thresholding

    thresh = apply_threshold(gray)

    show_and_write_image(
        parent_folder_path=parent_folder_path,
        source_image_name=source_image_name,
        operation_applied="thresh",
        image=thresh
    )

    # Apply the Canny edge detection algorithm

    edged = cv2.Canny(thresh, 30, 200, apertureSize=3, L2gradient=False)

    show_and_write_image(
        parent_folder_path=parent_folder_path,
        source_image_name=source_image_name,
        operation_applied="edged",
        image=edged
    )

    # Using the edged image, find all contours

    contours, hierarchy = cv2.findContours(
        edged,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_NONE
    )

    print("Number of Contours Found = " + str(len(contours)))

    print("Hierarchy: " + str(hierarchy))

    contour_candidates = []
    contour_areas = []
    # For each contour, we compute the area and we try to approximate its shape

    for contour in contours:

        # Approximate shape
        epsilon = 0.02  * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # We are interested in four-sided polygons
        if len(approx) == 4:
            # Compute area
            area = cv2.contourArea(contour)
            if area > 1000:
                print(f"Area: {area}, Points: {len(approx)}")
            contour_candidates.append((contour, area))
            contour_areas.append(area)


    if not contour_candidates:
        raise ValueError("No four-point contours found")

    # Extract max area from the contour_areas list
    max_area = max(contour_areas)

    # Based on the max area, extract the best contour
    best_contour = None
    for contour, area in contour_candidates:
        if area == max_area:
            best_contour = contour

    print("Max area contour =", max_area)

    # Extract its bounding rect
    x, y, w, h = cv2.boundingRect(best_contour)

    print(f"X={x}, Y={y}, W={w}, H={h}")

    print(f"Image dimensions: {image.shape[1]} x {image.shape[0]}")
    print(f"Contour dimensions: {w} x {h}")

    # Show the image before drawing the contours
    cv2.imshow('Raw Image', image)
    cv2.waitKey(0)

    # Create a copy of the raw image and draw contours
    contour_image = image.copy()
    cv2.drawContours(contour_image, contours, -1, (0, 255, 0), 3)
    cv2.imshow('Contours', contour_image)
    cv2.waitKey(0)

    # Cut the raw image
    image = image[y:y+h, x:x+w]
    show_and_write_image(
        parent_folder_path=parent_folder_path,
        source_image_name=source_image_name,
        operation_applied="cut",
        image=image
    )

    # Cut the gray image
    gray = gray[y:y+h, x:x+w]
    show_and_write_image(
        parent_folder_path=parent_folder_path,
        source_image_name=source_image_name,
        operation_applied="gray_and_cut",
        image=gray
    )

    # Cut the threshed image
    thresh = thresh[y:y+h, x:x+w]
    show_and_write_image(
        parent_folder_path=parent_folder_path,
        source_image_name=source_image_name,
        operation_applied="thresh_and_cut",
        image=thresh
    )


if __name__ == '__main__':

    cut_receipt("./input_images/image_1_jumbo.jpeg")
    resize_image("./input_images/image_1_jumbo_cut_image.jpeg")

    print(ocr("./input_images/image_1_jumbo_cut_image_resized_image.jpeg"))
