from scripts.ai import use_ai_to_correct_text_and_generate_JSON
from scripts.receipt_preprocessor import ReceiptPreprocessor


# =================================================
#           APPLY OTSU THRESHOLDING FUNCTION...
# =================================================

def apply_otsu_thresholding(image_path: str) -> str:
    receipt_preprocessor_instance = ReceiptPreprocessor()

    # APPLY GRAYSCALE

    (
        grayscale_image,
        grayscale_image_path
    ) =  receipt_preprocessor_instance.factory.operation(
        operation_applied=receipt_preprocessor_instance.factory.GRAYSCALE,
        image_path="./input_images/image_1_lidl.jpeg"
    )

    # APPLY CLAHE...
    (
        top_hat_image,
        top_hat_image_path
    ) =  receipt_preprocessor_instance.factory.operation(
        operation_applied=receipt_preprocessor_instance.factory.REMOVE_SHADOWS_AND_TEXTURE,
        image_path=grayscale_image_path
    )

    # APPLY DYNAMIC GAUSSIAN BLUR
    (
        blurred_image,
        blurred_image_path
    ) = receipt_preprocessor_instance.factory.operation(
        operation_applied=receipt_preprocessor_instance.factory.DYNAMIC_GAUSSIAN_BLUR,
        image_path=top_hat_image_path
    )

    # APPLY OTSU THRESHOLDING
    (
        thresholded_image,
        thresholded_image_path
    ) = receipt_preprocessor_instance.factory.operation(
        operation_applied=receipt_preprocessor_instance.factory.OTSU_THRESHOLDING,
        image_path=blurred_image_path
    )

    return thresholded_image_path


# =================================================
#           DEMO 1...
# =================================================

def demo_1():
    #use_ai_to_correct_text_and_generate_JSON("./input_images/image_1_lidl.jpeg")



    print(use_ai_to_correct_text_and_generate_JSON('./input_images/image_1_lidl.jpeg'))


# =================================================
#           DEMO 2...
# =================================================

def demo_2():
    use_ai_to_correct_text_and_generate_JSON('./input_images/image_2_jumbo.jpeg')


# =================================================
#           DEMO 3...
# =================================================

def demo_3():
    use_ai_to_correct_text_and_generate_JSON('./input_images/image_3_jumbo.jpeg')


# =================================================
#           IF WE RUN DIRECTLY THIS MODULE...
# =================================================

if __name__ == '__main__':

    # Execute the first demo...
    demo_1()

    # Execute the second demo...
    #demo_2()

    # Execute the third demo...
    #demo_3()
