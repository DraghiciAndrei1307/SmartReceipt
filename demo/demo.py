from scripts.ai import use_ai_to_correct_text_and_generate_JSON

from scripts.preprocessing import grayscale


def demo_1():
    use_ai_to_correct_text_and_generate_JSON("./input_images/image_1_jumbo.jpeg")

def demo_2():
    use_ai_to_correct_text_and_generate_JSON('./input_images/image_2_jumbo.jpeg')

def demo_3():
    use_ai_to_correct_text_and_generate_JSON('./input_images/image_3_jumbo.jpeg')



if __name__ == '__main__':


    #demo_1()
    #demo_2()
    demo_3()