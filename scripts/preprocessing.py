import cv2

from scripts.ocr import ocr


def extract_source_image_name_and_folder_path(image_path: str):
    """
    This function extracts the source image name,
    and its parent folder path.
    """

    splitted_image_path = image_path.split('/')

    return splitted_image_path[-1], "/".join(splitted_image_path[:-1])

def rotate_90_counter_clockwise(image_path: str):
    """
    This function rotates the image 90 degree counterclockwise
    around the origin and writes it. Also, it returns the
    modified image.
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

    _ = show_and_write_image(
        parent_folder_path=source_image_folder_path,
        source_image_name=source_image_name,
        operation_applied="rotate_90_counterclockwise",
        image=rotated_image
    )

    return rotated_image

def rotate_90_counter_clockwise_and_resize_image(image_path: str):
    """This function is used resize an image."""

    # Extract the source image name and the parent folder path of the image_path
    (
        source_image_name,
        source_image_folder_path
    ) = extract_source_image_name_and_folder_path(image_path)

    # Rotate image with 90 degrees counterclockwise around the origin
    rotated_image = rotate_90_counter_clockwise(image_path)

    # Resize using specific scale factors on both X and Y axis

    resized_image = cv2.resize(
        rotated_image,
        dsize=None,
        fx=3,
        fy=1.5,
        interpolation=cv2.INTER_CUBIC
    )

    _ = show_and_write_image(
        parent_folder_path=source_image_folder_path,
        source_image_name= source_image_name,
        operation_applied="rotate_90_counterclockwise_resize",
        image=resized_image
    )

    return resized_image

def resize(image_path: str):
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

    _ = show_and_write_image(
        parent_folder_path=source_image_folder_path,
        source_image_name=source_image_name,
        operation_applied="resize",
        image=resized_image
    )

    return resized_image

def grayscale(image_path: str):

    """
    This function reads the image, applies grayscale and writes it.
    Also, it returns the modified image.
    """


    # Extract the source image name and the parent folder path of the image_path
    (
        source_image_name,
        source_image_folder_path
    ) = extract_source_image_name_and_folder_path(image_path)

    # Read image from image_path, using cv2.imread(...)
    image = cv2.imread(image_path)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    show_and_write_image(
        parent_folder_path=source_image_folder_path,
        source_image_name=source_image_name,
        operation_applied="gray",
        image=gray
    )

    return gray

def thresh(image_path: str):
    """
    This function reads the image, applies threshold and writes it.
    Also, it returns the modified image.
    """

    # Extract the source image name and the parent folder path of the image_path
    (
        source_image_name,
        source_image_folder_path
    ) = extract_source_image_name_and_folder_path(image_path)

    # Convert the image to Grayscale

    gray = grayscale(image_path)

    # Apply thresh
    _, threshed_image = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    # Write image
    _ = show_and_write_image(
        parent_folder_path=source_image_folder_path,
        source_image_name=source_image_name,
        operation_applied="thresh",
        image=threshed_image
    )

    return threshed_image

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
            ".jpeg"
    )

    # Show the image and destroy it after user presses key
    cv2.imshow(operation_applied.title() + ' image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Write the image at the desired path
    cv2.imwrite(result_image_path, image)

    return result_image_path

def cut(image_path: str):
    """
    This function reads the image, cuts it and writes it.
    Also, it returns the path to the modified image.
    """

    # Extract the source image name and the parent folder path of the image_path
    (
        source_image_name,
        parent_folder_path
    ) = (
        extract_source_image_name_and_folder_path(image_path)
    )

    # Read image from image_path, using cv2.imread(...)
    image = cv2.imread(image_path)

    # Convert image to GrayScale
    gray = grayscale(image_path)

    _ = show_and_write_image(
        parent_folder_path=parent_folder_path,
        source_image_name=source_image_name,
        operation_applied="gray",
        image=gray
    )

    # Apply Thresholding (also performs Grayscaling)
    threshed = thresh(image_path)

    _ = show_and_write_image(
        parent_folder_path=parent_folder_path,
        source_image_name=source_image_name,
        operation_applied="thresh",
        image=threshed
    )

    # Apply the Canny edge detection algorithm

    edged = cv2.Canny(threshed, 30, 200, apertureSize=3, L2gradient=False)

    _ = show_and_write_image(
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
    cut_image_path = show_and_write_image(
        parent_folder_path=parent_folder_path,
        source_image_name=source_image_name,
        operation_applied="cut",
        image=image
    )

    # Cut the gray image
    gray = gray[y:y+h, x:x+w]

    _ = show_and_write_image(
        parent_folder_path=parent_folder_path,
        source_image_name=source_image_name,
        operation_applied="gray_cut",
        image=gray
    )

    # Cut the threshed image
    threshed = threshed[y:y+h, x:x+w]

    _ = show_and_write_image(
        parent_folder_path=parent_folder_path,
        source_image_name=source_image_name,
        operation_applied="thresh_cut",
        image=threshed
    )

    return image, cut_image_path

def preprocess(image_path: str):
    cut_image, cut_image_path = cut(image_path)
    return resize(cut_image_path)



if __name__ == '__main__':


    cut_image = cut("./input_images/image_1_jumbo.jpeg")
    resized_image = resize("./input_images/image_1_jumbo_cut.jpeg")
    _ = grayscale("./input_images/image_1_jumbo_cut_resize.jpeg")
    _ = thresh("./input_images/image_1_jumbo_cut_resize.jpeg")

    print(ocr("./input_images/image_1_jumbo.jpeg"))
    print(ocr("./input_images/image_1_jumbo_cut_resize.jpeg"))
    print(ocr("./input_images/image_1_jumbo_cut_resize_gray.jpeg"))
    print(ocr("./input_images/image_1_jumbo_cut_resize_thresh.jpeg"))


