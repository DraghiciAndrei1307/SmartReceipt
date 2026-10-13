import re
import ollama
import json
from scripts.models import create_ocr_model
from scripts.parser import parser

from scripts.schema import ReceiptSchema

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
    
    REGULI STRICTE:
    1. NU AI VOIE SA INVENTEZI DATE! Daca o valoare nu este vizibila
    clar sau lipseste, foloseste `null` pentru string-uri sau `0.0` 
    pentru numere. Nu ghici!
    2. Fii foarte atent la numerele cu spatii sau puncte despartite 
    (de exemplu: "8 . 96" înseamna 8.96).
    3. Extrage totalul exact de pe bon (de obicei in zona cu 
    "TOTAL" sau "CARD"). 
    4. NU include în lista de produse ("items") datele de antet ale 
    magazinului (numele firmei, adresa, CUI-ul, "CUTITARU", "POS/TRAN", etc.). 
    Lista de produse incepe abia dupa liniile cu articole/prețuri si 
    se termina inainte de "TOTAL" / "CARD". 

    Atentie stricta la structura JSON 
    pe care trebuie sa o returnezi:
    - 'merchant_name': string 
    - 'total_amount': float
    - 'items': lista de obiecte, unde fiecare obiect 
    trebuie sa contina EXACT aceste chei:
      - 'name': string (numele produsului)
      - 'quantity': float 
      - 'price': float

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
        format=ReceiptSchema.model_json_schema(),
        options={
            'temperature': 0.1, # controls the "creativity";
                                # we do not want the AI to invent anything;
                                # it should choose the most probable and
                                # correct tokens
            'num_ctx': 4096 # context window/how much text it can "remember"
        }
    )

    ai_response_text = response['message']['content'].strip()

    validated_receipt = ReceiptSchema.model_validate_json(ai_response_text)

    print("AI response: " + ai_response_text)
    print("Validated response: " + json.dumps(validated_receipt.model_dump(), indent=2))

if __name__ == "__main__":
    image_path = "./input_images/image_1_jumbo.jpeg"
    use_ai_to_correct_text_and_generate_JSON(image_path)
