import re
import json
import ollama
from schema import ReceiptSchema
from models import create_ocr_model
from parser import parser


def clean_ocr_text_for_llm(text: str) -> str:
    """
    Clean the OCR text.
    For example:
    '1 , 99' -> '1.99'
    '8 . 96' -> '8.96'
    """

    # Replace the white space between digits
    # if they are separated by , or .
    text = re.sub(r'(\d+)\s*[\,\.]\s*(\d+)', r'\1.\2', text)
    return text


def use_ai_to_correct_text_and_generate_JSON(image_path: str):

    # Run OCR and parse the output received from the OCR
    ocr_model = create_ocr_model(image_path)
    raw_ocr_text = parser(ocr_model)

    if raw_ocr_text is None:
        raw_ocr_text = ""
    else:
        raw_ocr_text = str(raw_ocr_text)

    cleaned_ocr = clean_ocr_text_for_llm(raw_ocr_text)

    # The AI engineering part
    # Create the prompt

    prompt = f"""
    Esti un parser de date structurate pentru bonuri 
    fiscale din Romania.
    
    Sarcina ta este sa extragi informatiile din textul 
    OCR si sa le convertesti in format JSON.

    Atentie stricta la structura JSON 
    pe care trebuie sa o returnezi:
    - 'merchant_name': string (ex: "JUMBO")
    - 'total_amount': float (ex: 8.96)
    - 'items': lista de obiecte, unde fiecare obiect 
    trebuie sa contina EXACT aceste chei:
      - 'name': string (numele produsului, ex: "LAPTE")
      - 'quantity': float (ex: 1.0)
      - 'price': float (ex: 1.99)

    ---
    Text OCR real de procesat:
    {cleaned_ocr}
    """

    # Use the local model (you need to use ollama pull <nume_model> in terminal)
    # Eventually, you need to run: ollama run <model_name>
    response = ollama.chat(
        model='gemma3:12b',
        messages=[
            {'role': 'user', 'content': prompt}
        ],
        format='json',
        options={
            'temperature': 0.1,
            'num_ctx': 4096
        }
    )

    ai_response_text = response['message']['content'].strip()


    print("AI Response: " + ai_response_text)

    # Validate the result using Pydantic
    try:
        # Create dictionary out of the json-formatted string
        data_dict = json.loads(ai_response_text)

        receipt_data = ReceiptSchema(**data_dict)
        print("Validated Response: " + receipt_data.model_dump_json(indent=2))
        return receipt_data

    except Exception as e:
        print(f"Error: {e}")
        return None


if __name__ == "__main__":
    image_path = "./input_images/image_1_jumbo.jpeg"
    use_ai_to_correct_text_and_generate_JSON(image_path)