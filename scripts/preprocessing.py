import cv2
import numpy as np

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

    rotated_image_path = show_and_write_image(
        parent_folder_path=source_image_folder_path,
        source_image_name=source_image_name,
        operation_applied="rotate_90_counterclockwise",
        image=rotated_image
    )

    return rotated_image, rotated_image_path

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
        fx=2.5,
        fy=2.5,
        interpolation=cv2.INTER_CUBIC
    )

    resized_image_path = show_and_write_image(
        parent_folder_path=source_image_folder_path,
        source_image_name=source_image_name,
        operation_applied="resize",
        image=resized_image
    )

    return resized_image, resized_image_path

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

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    gray_image_path = show_and_write_image(
        parent_folder_path=source_image_folder_path,
        source_image_name=source_image_name,
        operation_applied="gray",
        image=gray_image
    )

    return gray_image, gray_image_path

def gaussian_blur(image_path: str):

    """
    This function reads the image, applies Gaussian BLur and writes it.
    Also, it returns the modified image.
    """

    # Extract the source image name and the parent folder path of the image_path
    (
        source_image_name,
        source_image_folder_path
    ) = extract_source_image_name_and_folder_path(image_path)

    # Apply Grayscale
    gray_image, gray_image_path = grayscale(image_path)

    # Apply Gaussian Blur
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

    blurred_image_path = show_and_write_image(
        parent_folder_path=source_image_folder_path,
        source_image_name=source_image_name,
        operation_applied="gaussian_blur",
        image=blurred_image
    )

    return blurred_image, blurred_image_path

def dynamic_gaussian_blur(image_path: str):

    # Extract the source image name and the parent folder path of the image_path
    (
        source_image_name,
        source_image_folder_path
    ) = extract_source_image_name_and_folder_path(image_path)

    # Read the image
    image = cv2.imread(image_path)

    # Get the height and width
    h,w = image.shape[:2]

    # We compute a dynamic kernel (e.g. ~1.5% * width)
    k_size = int(w * 0.015)

    # We make sure that the k_size is an odd number...
    if k_size %2 == 0:
        k_size += 1

    # Set the threshold interval
    k_size = max(3, min(k_size, 31))

    # Apply Grayscale
    gray_image, gray_image_path = grayscale(image_path)

    # Apply the Gaussian blurr...
    blurred_image = cv2.GaussianBlur(gray_image, (k_size, k_size), 0)

    # Write and show image
    blurred_image_path = show_and_write_image(
        parent_folder_path=source_image_folder_path,
        source_image_name=source_image_name,
        operation_applied="gaussian_blur",
        image=blurred_image
    )

    return blurred_image, blurred_image_path

def thresh(image_path: str):
    """
    This function reads the image, applies threshold and writes it.
    Also, it returns the modified image.

    MAKE SURE YOU USE A GRAY IMAGE!
    """

    # Extract the source image name and the parent folder path of the image_path
    (
        source_image_name,
        source_image_folder_path
    ) = extract_source_image_name_and_folder_path(image_path)

    # Read image from image_path as grayscale using cv2.IMREAD_GRAYSCALE
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Apply thresh
    _, threshed_image = cv2.threshold(
        image,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    # Write image
    threshed_image_path = show_and_write_image(
        parent_folder_path=source_image_folder_path,
        source_image_name=source_image_name,
        operation_applied="thresh",
        image=threshed_image
    )

    return threshed_image, threshed_image_path

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

def cut_using_thresholding(image_path: str):
    """
    This function reads the image, cuts it and writes it.
    Also, it returns the path to the modified image.

    MAKE SURE YOU USE A THRESHED IMAGE!
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

    # Apply Gaussian Blur

    blurred, blurred_image_path = dynamic_gaussian_blur(image_path)

    threshed_image, threshed_image_path = thresh(blurred_image_path)

    # Using the edged image, find all contours

    contours, hierarchy = cv2.findContours(
        threshed_image,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_NONE
    )

    #print("Number of Contours Found = " + str(len(contours)))

    #print("Hierarchy: " + str(hierarchy))

    contour_candidates = []
    contour_areas = []
    # For each contour, we compute the area and we try to approximate its shape

    for contour in contours:

        # Approximate shape
        # margin of error (epsilon) = 2% out of the perimeter
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

    # print("Max area contour =", max_area)

    # Extract its bounding rect
    x, y, w, h = cv2.boundingRect(best_contour)

    # print(f"X={x}, Y={y}, W={w}, H={h}")
    #
    # print(f"Image dimensions: {image.shape[1]} x {image.shape[0]}")
    # print(f"Contour dimensions: {w} x {h}")

    # Show the image before drawing the contours
    cv2.imshow('Raw Image', image)
    cv2.waitKey(0)

    # Create a copy of the raw image and draw contours
    contour_image = image.copy()
    cv2.drawContours(contour_image, contours, -1, (0, 255, 0), 3)

    _ = show_and_write_image(
        parent_folder_path=parent_folder_path,
        source_image_name=source_image_name,
        operation_applied="draw_contours",
        image=contour_image
    )

    # Cut the raw image
    image = image[y:y+h, x:x+w]
    cut_image_path = show_and_write_image(
        parent_folder_path=parent_folder_path,
        source_image_name=source_image_name,
        operation_applied="cut",
        image=image
    )

    return image, cut_image_path


def fine_deskew(image_path: str):
    """
    Corectează înclinația fină a textului din interiorul bonului decupat.
    """
    (
        source_image_name,
        source_image_folder_path
    ) = extract_source_image_name_and_folder_path(image_path)

    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 1. Binarizare inversată (textul devine alb, fundalul negru)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # 2. Găsim coordonatele tuturor pixelilor albi (textul)
    coords = np.column_stack(np.where(thresh > 0))

    # Dacă nu avem destui pixeli, returnăm imaginea neschimbată
    if len(coords) < 10:
        return image, image_path

    # 3. Calculăm cel mai mic dreptunghi care cuprinde textul și extragem unghiul
    angle = cv2.minAreaRect(coords)[-1]

    # Ajustăm unghiul în funcție de convenția OpenCV
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    print(f"Unghiul detectat pentru deskew fin: {angle:.2f} grade")

    # Rotim imaginea doar dacă unghiul este semnificativ (ex: mai mare de 0.5 grade)
    if abs(angle) > 0.5:
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)

        # Rotim imaginea completând fundalul cu alb (pentru a nu strica OCR-ul)
        image = cv2.warpAffine(
            image, M, (w, h),
            flags=cv2.INTER_CUBIC,
            borderMode=cv2.BORDER_CONSTANT,
            borderValue=(255, 255, 255)
        )

    # Salvăm imaginea deskewed
    deskewed_image_path = show_and_write_image(
        parent_folder_path=source_image_folder_path,
        source_image_name=source_image_name,
        operation_applied="deskew",
        image=image
    )

    return image, deskewed_image_path


def cut_using_canny(image_path: str):
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

    # Remove the noise from the gray image.

    # 'ksize' means Kernel Size/Blur window (matrix of pixels)
    #

    # sigmaX - standard deviation

    blurred, blurred_image_path = dynamic_gaussian_blur(image_path)

    # Apply the Canny edge detection algorithm.

    # We have 2 thresholds (lower=30 and upper=200).
    # They are used to remove the noise from an image and are
    # used to determine which lines are edges and which
    # ones are not.
    # These thresholds represent gradient intensity limits(
    # sudden change in color/light).

    # Everything which is above upper threshold is accepted.
    # Everything which is below the lower threshold is rejected.
    # Everything (pixel) between thresholds is checked against its
    # neighbours. If a neighbour has the gradient intensity (how
    # fast the luminosity changes from one pixel to another) above
    # the upper threshold, then the pixel is accepted.
    # No "strong" neighbours, then the pixel is rejected.

    # L2gradient = False -> gradient intensity is calculated using:
    # abs(dx) + abs(dy)

    # L2gradient = True -> gradient intensity is calculated using:
    # sqrt(pow(dx,2) + pow(dy, 2))

    edged = auto_canny(blurred_image_path)

    kernel = np.ones((3, 3), np.uint8)
    edged_dilated = cv2.dilate(edged, kernel, iterations=1)

    # Using the edged image, find all contours

    contours, hierarchy = cv2.findContours(
        edged_dilated,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_NONE
    )

    if not contours:
        raise ValueError("Niciun contur detectat în imagine! Verifică iluminarea.")

        # Filtrăm contururile după arie (să ocupe cel puțin 5% din imagine)
    min_area = image.shape[0] * image.shape[1] * 0.05
    contour_candidates = []

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > min_area:
            contour_candidates.append((contour, area))

    if not contour_candidates:
        # Fallback de urgență: luăm cel mai mare contur brut existent
        best_contour = max(contours, key=cv2.contourArea)
    else:
        # Luăm conturul cu cea mai mare arie
        best_contour = max(contour_candidates, key=lambda x: x[1])[0]


    # Extract its bounding rect
    x, y, w, h = cv2.boundingRect(best_contour)

    # print(f"X={x}, Y={y}, W={w}, H={h}")
    #
    # print(f"Image dimensions: {image.shape[1]} x {image.shape[0]}")
    # print(f"Contour dimensions: {w} x {h}")

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

    return image, cut_image_path

def auto_canny(image_path: str):
    # Extract the source image name and the parent folder path of the image_path
    (
        source_image_name,
        source_image_folder_path
    ) = extract_source_image_name_and_folder_path(image_path)

    # Read image from image_path, using cv2.imread(...)
    image = cv2.imread(image_path)

    # Compute the median value of the image pixels...

    sigma = 0.33

    median_value = np.median(image)

    lower = int(max(0, (1.0 - sigma) * median_value))
    upper = int(min(255, (1.0 + sigma) * median_value))

    edged = cv2.Canny(image, lower, upper)

    return edged

def preprocess_using_thresholding(image_path: str):
    """
    This function applies grayscale, then it applies
    thresholding to find contours and obtain the
    bounding rect which is used to cut the image.
    """

    # Cut image using Thresholding...
    cut_image, cut_image_path = cut_using_thresholding(image_path)

    # Apply deskewing
    deskew_image, deskew_path = fine_deskew(cut_image_path)

    # Apply thresholding
    final_thresh_image, final_thresh_path = thresh(deskew_path)

    return resize(final_thresh_path)

def preprocess_using_canny(image_path: str):
    cut_image, cut_image_path = cut_using_canny(image_path)
    return resize(cut_image_path)

if __name__ == '__main__':
    pass
    # cut_image = cut("./input_images/image_1_jumbo.jpeg")
    # resized_image = resize("./input_images/image_1_jumbo_cut.jpeg")
    # _ = grayscale("./input_images/image_1_jumbo_cut_resize.jpeg")
    # _ = thresh("./input_images/image_1_jumbo_cut_resize.jpeg")
    #
    # print(ocr("./input_images/image_1_jumbo.jpeg"))
    # print(ocr("./input_images/image_1_jumbo_cut_resize.jpeg"))
    # print(ocr("./input_images/image_1_jumbo_cut_resize_gray.jpeg"))
    # print(ocr("./input_images/image_1_jumbo_cut_resize_thresh.jpeg"))


