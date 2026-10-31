from scripts.ai import use_ai_to_correct_text_and_generate_JSON
from scripts.new_preprocessing_approach import new_preprocessing


def demo_1():
    use_ai_to_correct_text_and_generate_JSON("./input_images/demo_live.jpeg")
    # new_preprocessing("./input_images/demo_live.jpeg")
def demo_2():
    use_ai_to_correct_text_and_generate_JSON('./input_images/image_2_jumbo.jpeg')

def demo_3():
    use_ai_to_correct_text_and_generate_JSON('./input_images/image_3_jumbo.jpeg')



if __name__ == '__main__':

    demo_1()
    #demo_2()
    #demo_3()
