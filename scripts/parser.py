# preprocessing -> ocr -> ocr model -> parser

from scripts.models import create_ocr_model

def parser(ocr_model: list[dict]):
    """
    This function parses the OCR model returned
    from the create_ocr_model function.
    """

    # ============================================
    # GROUP USING THE Y COORDINATE
    # ============================================

    # Get the Y value of the upper left corner for each word
    upper_left_corner_values = []

    sum_of_y_differences = 0

    for item in ocr_model:
        upper_left_corner_values.append(
            (
                item["bbox"][0],
                item["text"],
                item["confidence"]
            )
        )

        difference_between_upper_left_and_lower_left_y = (
                item["bbox"][3][1] -
                item["bbox"][0][1]
        )

        sum_of_y_differences += difference_between_upper_left_and_lower_left_y


    # Sort the Y coordinates of the upper left corner
    upper_left_corner_values.sort(key = lambda x: x[0][1])

    print("Left corners = " + str(upper_left_corner_values))

    # Compute the mean value
    len_of_upper_left_corner_values = len(upper_left_corner_values)

    mean = 0.0

    if len_of_upper_left_corner_values == 0:
        return "No valid bbox!"

    mean = round(float(sum_of_y_differences / len(upper_left_corner_values)), 2)

    # We will use this 60% out of the mean value because
    # maybe the difference between 2 rows may be smaller than
    # the height of a row.

    threshold = round(0.6 * mean, 2)

    print("Mean = " + str(mean))
    print("Threshold = " + str(threshold))

    current_y = int(upper_left_corner_values[0][0][1])
    y_groups = []
    current_y_group = []

    for coordinates, text, confidence in upper_left_corner_values:

        y_value = int(coordinates[1])

        if round(float(y_value - current_y), 2) > threshold:
            y_groups.append(current_y_group)
            current_y_group = []

        current_y = y_value
        current_y_group.append((coordinates, text, confidence))

    y_groups.append(current_y_group)

    print("Number of groups = " + str(len(y_groups)))

    for y_group in y_groups:
        print("Current group = " + str(y_group))

    # ============================================
    # GROUP USING THE X COORDINATE
    # ============================================

    # Sort each groups using the x value

    for group in y_groups:
        group.sort(key = lambda x: x[0])

    lines = []

    for y_group in y_groups:
        lines.append(" ".join([item[1] for item in y_group]))

    full_receipt_text = "\n".join(lines)

    print(full_receipt_text)

    return full_receipt_text

if __name__ == "__main__":

    model = create_ocr_model("./input_images/image_1_jumbo.jpeg")

    parser(model)