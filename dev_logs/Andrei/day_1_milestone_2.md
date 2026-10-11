# DAY 1 (October 10, 2026)

## Goals

- Finish Milestone 2 - Preprocessing. 

## Steps performed

1) Refactored the ocr.py script. Encapsulated the logic inside the ocr function that receives an image path and returns
a string containing the receipt text.

```python
import os

import easyocr

def ocr(image_path: str) -> str:
    """Simple OCR function to extract text from an image"""

    # Define the Reader object
    reader = easyocr.Reader(['en', 'ro'])

    # Return the text extracted from the image_path
    return reader.readtext(image_path, detail=0)
```

2) The preprocessing step we will consider a particular case. We will try to enhance the quality of a specific image. 

The following steps were performed:
- Apply OCR on the basic image
- Rotate the [image_1_starbucks.jpeg](../../input_images/image_1_starbucks.jpeg) 90 degrees counter clockwise. 
- Apply [OCR function](../../scripts/ocr.py) on the [image_1_starbucks_rotated_90_counter_clockwise.jpeg](../../input_images/image_1_starbucks_rotated_90_counter_clockwise.jpeg) 
- Resize the rotated image [image_1_starbucks_rotated_90_counter_clockwise](../../input_images/image_1_starbucks_rotated_90_counter_clockwise.jpeg)
- Apply OCR function on the [resized_image](../../input_images/resized_image.jpeg)

Results: 

- Apply OCR before preprocessing:

```commandline
['4', '3', '1 ;', '5', '2', '2', '29', '5', '8adase:', '72522883088', '8', '5', '185|2 2', '8f', '3', ';;', '2', 'ș', '2', '4', '5', '595', 'g', '1', '8', '8h', '2', '5', '2', '2', '33', '5', 'g', '889', '1', '5', '1', ';', '8', '888', 'N', 'N', '5', '8', 'ș', '1', '1', '0', 'D', '1', '4', '4', '3', '2', '1', 'ș', '1', '2', 'E2lf', '5', '9', ';', '1', '2', '1', '2', 'E', '2', '8', '2', '4', '2', '5', '91', '5', '3', '8', '9', '8', '[', 'g,2', '38', '0', '2', '2', '8', '5', '5', '28', '{', ';', '4', '2', '8', '~']
```

- Apply OCR after rotation with 90 degrees counter clockwise: 

```commandline
['AMREST COFFEE SRL', 'HuN', 'BUCURESTI', 'BD ,', 'IULIU MANIU', 'NR , 558-560 , SECTORUL', 'C.I.F', 'R02O/19287', 'BON FISCAL', 'u', 'VT Latte', '2 BUC X 23,90', '47 ,80', 'STARBUCKS   CuP', '2 BUC', '0,20', '0,40 A', 'tOThL;', '48,20', 'CREDIT CARD', '48,20', 'NUME : ELENA-ALEXANDRA', 'CASA =', 'NUMAR  NoTA:2513', 'TIP TRANZACTIE;To Go', "10 OCT' 26 11;14 AM", "10 OCT '26 11;14 AM", 'COFIE TITULAR CARD', 'WORKSTATION', '34149', 'SERVER', '39160 61006502', 'CHECK', '2513', 'TABLE', 'DATA', '10.10.2026', 'ORA', '11:14,04', 'CARD', '****1451', 'PAN SEQ', '0o', 'NUME PREFERAT', 'ING PAYHAVE', 'TIP DE CARD', 'ViSASTANDARDDEBIT', 'METOD DE PLAT', 'VISA', 'VARIANT DE PLAT', 'VISASTANDARDDEBIT', 'MOD INTRARE', 'CIP FR CONTACT', 'AID', 'A0oo0oo0o31010', 'MID', '498750004828803', 'TID', 'P4OOPLUS-807064605', 'PTID', '67189160', 'AUTH , CODE', '503247', 'OFERT', 'sJhYiGPBGC7o', 'REFERINC', '2513-694149548044', 'TIP', 'PRODUSE_SERviCII', 'SUMA', 'RON  48,20', 'APROBAT', 'PSTRAI PENTRU EVIDENE', 'TVA', 'VALOARE', 'ToTAL', '4o ', 'A-21,00w', '8,37', '48 ,20', 'TOTAL TAXe:', '8 ,37', 'CASIER:', 'HIPOS1', 'NUMAR BON:', '2778-00075', '10.10.2026', '11:14,14', 'F2000446684', 'BON FISCAL']
```

We can notice here an improvement, but there are still inconsistencies...

For example:
- `t0ThL` instead of `TOTAL`
- `CASA =` instead of `CASA: 1`
- `TIP TRANZACTIE;To Go` instead of `TIP TRANZACTIE:TO GO`
- etc.

The next step here would be to try to zoom in and see if the output is more consistent...

- Apply OCR after rotation with 90 degrees counterclockwise around the origin and resize with a factor of 3 on X and a factor of 1.5 on Y, using the `INTER_CUBIC` method.  

As the documentation says, the INTER_CUBIC method should in general be used for "Enlarging" as it offers "Higher quality for upscaling".

```commandline
['AMREST', 'COFfEE', 'SRL', 'MUN', 'BUCURESTI', 'BD', 'IULIU', 'MANIU', 'NR', '558', '560', 'SECTURUL', '6', 'C.I.F', 'R020119287', 'BON FISCAL', 'Ca', 'VT', 'LATTE', '2', 'BUC', '23', '90', '47', '80', '6', 'STARBUCKS', 'CUP', '2', 'BUC', '0', '20', '0', '40', 'A', 'TOTAL :', '48 ,20', 'CREDIT', 'CARD', '48', '2o', 'NUNE', 'ELENA-ALEXANDRA', 'CAS4', '1', 'NUMAR', 'NOTA', '2513', 'TIP', 'TRANZACTIE:TO', 'Go', '10', 'OCT', '26', '11 : 14', 'AM', '10', 'OCT', '26', '11 : 14', 'AM', 'COPIE', 'TITULAR', 'CARD', 'WORKSTATION', '34149', 'SERVER', '39160', '61006502', 'CHECK', '2513', 'TABLE', '0', 'DATA', '10', '10 . 2026', 'ORA', '11 : 14:04', 'CARD', '*a**1451', 'PAN', 'SEQ', '0o', 'NUME', 'PREFERAT', 'ING', 'PMYWAVE', 'TIP', 'DE', 'CARD', 'VISASTANDARDDEBIT', 'METOD', 'DE', 'PLAT', 'YISA', 'VARIANT', 'DE PLAT', 'VISASTANOARDDEBIT', 'MoD', 'INTRARE', 'CIP', 'FR', 'CONTACT', 'AID', 'Aooo0ooo031010', 'MID', '498750004828803', 'TID', 'P4OOPLUS-807064605', 'PTID', '67189160', 'AUTH', 'CODE', '503247', 'OFERT', '5JMYIGPBGC70', 'REFERINC', '2513-694149548044', 'TIP', 'PRODUSE', 'SERVICII', 'SUMg', 'RON', '48', '20', 'APROBAT', 'PSTRAI', 'PENTRU', 'EVIDENE', 'TvA', 'VALOARE', 'TOTAL', 'A-21', 'O0%', '8', '37', '48', '20', 'TOTAL', 'TAYE:', '8,37', 'CASIER :', 'HPOS1', 'NUMAR', 'BON', '2778-00075', '10', '10', '2026', '11 : 14:14', '42000446684', 'BON', 'FISCAL']
```

Regarding the improvements, we can see that we have fewer items that contain a group of characters that are not separated 
by white spaces. Also, the quality of the extracted words is better. 

The next step is to cut the image and then apply Grayscale on it.

Personal note: I think I need to cut the receipt before trying to resize...

3) Cut the receipt

To cut the receipt, we need to identify its contours and then threshold it.

## Resources 

- [EasyOCR Documentation](https://www.jaided.ai/easyocr/)

