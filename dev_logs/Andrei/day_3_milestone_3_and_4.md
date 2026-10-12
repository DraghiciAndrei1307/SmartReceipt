# DAY 3 (October 12, 2026)

Ok, I managed to create the OCR Model, nothing fancy, just a list of dictionaries in which each element contains 
3 things:
- bbox (coordinates of all corners of the box in which the text can be found)
- text (the actual text of the word extracted by the OCR)
- confidence (accuracy of the extracted text)

Next, I implemented the `parser.py`. The algorithm here is simple:
- Get the reference point (I chose the Y value of the upper left corner)
- Sort the items based on the Y value of the upper left corners
- To determine if 2 words are on the same row, I used `threshold = 0.6 * mean`. `mean` represents the mean value of the 
differences between the y values of the upper left corner and the lower left corner of each bounding box.
- I traversed the list sequentially and calculated the difference between the current_y and the previous_y. If the 
difference was > threshold, then the items were not on the same row.
- After I grouped the items/words on rows, I sorted each group (using x value of the upper left corner this time) 
because some words may be displayed in different order than the correct one we have on the receipt.

The process sample output: 

- Sort list using the y value of the upper left corner
```commandline
Upper Left Corners = [([753, 71], 'JUMBO', 0.98), ([997, 77], 'ECR', 0.95), ([1240, 78], 'SRI', 0.96), ([420, 116], 'STR . COMERTULUI', 0.9), ([1155, 121], '7 ,SAT', 0.5), ([1034, 128], 'NR', 0.98), ([1402, 128], 'DOMNESTI', 0.74), ([626, 174], 'COM', 0.77), ([788, 174], 'DOMNVEST [', 0.31), ([1153, 174], 'JUD', 0.97), ([1320, 180], 'ILFOV', 0.69), ([1070, 220], '2021360', 0.61), ([748, 224], 'TEL', 1.0), ([908, 226], '021', 0.98), ([357, 265], 'COD', 0.89), ([524, 268], 'IDENTIFICARE', 0.66), ([1048, 270], 'FISCALA', 0.97), ([1380, 280], 'K0189/1652', 0.55), ([158, 360], '20', 1.0), ([284, 363], 'CUTITARU', 1.0), ([156, 408], 'POS/TRAN :', 0.91), ([573, 419], '011/', 0.96), ([778, 422], '216', 1.0), ([1757, 481], 'Lel', 0.79), ([368, 518], '1', 1.0), ([444, 518], 'OOO', 0.75), ([689, 521], 'BUC', 1.0), ([937, 524], '1.99', 0.68), ([848, 526], 'X', 0.85), ([152, 558], 'CARIVET', 0.44), ([446, 568], 'A7', 0.98), ([569, 569], 'S0F', 0.43), ([1720, 570], '1 , 99', 0.68), ([931, 571], 'SPI', 0.97), ([728, 572], 'ROTI', 0.84), ([152, 608], '55242800003//1252812', 0.65), ([922, 662], '1 , 49', 0.77), ([438, 665], 'o0O', 0.34), ([679, 665], 'BUC', 0.98), ([361, 667], '1', 1.0), ([841, 671], 'X', 0.9), ([151, 707], 'ETICHETE', 0.6), ([838, 710], 'IOFX6s', 0.4), ([518, 712], 'AUTOCOL', 0.99), ([1798, 712], '49', 1.0), ([1721, 719], '1', 1.0), ([145, 757], '5480480000.38/1240477', 0.97), ([662, 808], 'BUC', 0.99), ([990, 808], '49', 1.0), ([422, 810], 'OOO', 0.79), ([905, 813], '1', 1.0), ([347, 815], '1', 1.0), ([829, 815], 'X', 0.66), ([494, 853], 'AUTOCOL', 0.97), ([823, 856], '1OF)9', 0.33), ([138, 858], 'ETICHETE', 0.98), ([1800, 862], '49', 1.0), ([1718, 864], '1', 1.0), ([1932, 864], 'A', 0.65), ([134, 903], '548049000037/1240476', 0.78), ([402, 958], 'OOO', 0.89), ([646, 958], 'BUC', 1.0), ([810, 958], 'X 3,99', 0.74), ([337, 963], '1', 1.0), ([729, 1006], '72BUC', 0.95), ([134, 1008], 'SERVETELE', 1.0), ([517, 1008], 'UMED', 0.94), ([972, 1010], 'M', 1.0), ([1716, 1016], '3 , 99', 0.53), ([1932, 1016], 'A', 0.18), ([132, 1058], '5213001215419/1238410', 0.99), ([163, 1149], 'FotAL', 0.66), ([1720, 1168], '9e', 0.38), ([1539, 1169], '833', 0.81), ([161, 1243], 'TOTAL-', 0.74), ([403, 1243], 'TVA', 0.99), ([1804, 1270], '56', 1.0), ([1726, 1272], '1', 0.99), ([602, 1293], 'OO"', 0.62), ([480, 1296], '21', 1.0), ([310, 1298], 'A', 0.92), ([162, 1302], 'Tva', 0.68), ([1726, 1322], '1 , 56', 0.53), ([141, 1401], 'CARD', 0.99), ([1717, 1427], '8 . 96', 0.83), ([521, 1443], 'UANDUTE', 0.43), ([310, 1452], 'ART', 0.74), ([136, 1456], 'Nr', 1.0), ([608, 1684], '2 6] 0', 0.44), ([1106, 1687], 'TG 2 T6', 0.12), ([430, 1850], '00/11', 0.54), ([127, 1854], 'EJIKZ :', 0.43), ([522, 1879], "O(Jt J4 , 1' ; ))6 Y2124 14211v1/472 >19' ,10V1 1", 0.0), ([255, 1908], 'UNIu; :', 0.31), ([132, 1910], 'I0', 0.17), ([722, 1922], 'Dain: 10/a895259> UnA:77 47-23', 0.01), ([302, 1956], '00211', 0.77), ([132, 1968], 'BF', 0.31), ([680, 2006], '1I', 0.1), ([974, 2031], 'F [ 5 € ^', 0.16), ([684, 2046], 'E 0 N', 0.54)]
```

- Compute the mean value and threshold
```commandline
Mean = 55.28
Threshold = 33.17
```

- Group items/words based on the difference between the `current_y` and `previous_y`
```commandline
Number of groups = 26
Current group = [([753, 71], 'JUMBO', 0.98), ([997, 77], 'ECR', 0.95), ([1240, 78], 'SRI', 0.96)]
Current group = [([420, 116], 'STR . COMERTULUI', 0.9), ([1155, 121], '7 ,SAT', 0.5), ([1034, 128], 'NR', 0.98), ([1402, 128], 'DOMNESTI', 0.74)]
Current group = [([626, 174], 'COM', 0.77), ([788, 174], 'DOMNVEST [', 0.31), ([1153, 174], 'JUD', 0.97), ([1320, 180], 'ILFOV', 0.69)]
Current group = [([1070, 220], '2021360', 0.61), ([748, 224], 'TEL', 1.0), ([908, 226], '021', 0.98)]
Current group = [([357, 265], 'COD', 0.89), ([524, 268], 'IDENTIFICARE', 0.66), ([1048, 270], 'FISCALA', 0.97), ([1380, 280], 'K0189/1652', 0.55)]
Current group = [([158, 360], '20', 1.0), ([284, 363], 'CUTITARU', 1.0)]
Current group = [([156, 408], 'POS/TRAN :', 0.91), ([573, 419], '011/', 0.96), ([778, 422], '216', 1.0)]
Current group = [([1757, 481], 'Lel', 0.79)]
Current group = [([368, 518], '1', 1.0), ([444, 518], 'OOO', 0.75), ([689, 521], 'BUC', 1.0), ([937, 524], '1.99', 0.68), ([848, 526], 'X', 0.85), ([152, 558], 'CARIVET', 0.44), ([446, 568], 'A7', 0.98), ([569, 569], 'S0F', 0.43), ([1720, 570], '1 , 99', 0.68), ([931, 571], 'SPI', 0.97), ([728, 572], 'ROTI', 0.84)]
Current group = [([152, 608], '55242800003//1252812', 0.65)]
Current group = [([922, 662], '1 , 49', 0.77), ([438, 665], 'o0O', 0.34), ([679, 665], 'BUC', 0.98), ([361, 667], '1', 1.0), ([841, 671], 'X', 0.9)]
Current group = [([151, 707], 'ETICHETE', 0.6), ([838, 710], 'IOFX6s', 0.4), ([518, 712], 'AUTOCOL', 0.99), ([1798, 712], '49', 1.0), ([1721, 719], '1', 1.0)]
Current group = [([145, 757], '5480480000.38/1240477', 0.97)]
Current group = [([662, 808], 'BUC', 0.99), ([990, 808], '49', 1.0), ([422, 810], 'OOO', 0.79), ([905, 813], '1', 1.0), ([347, 815], '1', 1.0), ([829, 815], 'X', 0.66)]
Current group = [([494, 853], 'AUTOCOL', 0.97), ([823, 856], '1OF)9', 0.33), ([138, 858], 'ETICHETE', 0.98), ([1800, 862], '49', 1.0), ([1718, 864], '1', 1.0), ([1932, 864], 'A', 0.65)]
Current group = [([134, 903], '548049000037/1240476', 0.78)]
Current group = [([402, 958], 'OOO', 0.89), ([646, 958], 'BUC', 1.0), ([810, 958], 'X 3,99', 0.74), ([337, 963], '1', 1.0)]
Current group = [([729, 1006], '72BUC', 0.95), ([134, 1008], 'SERVETELE', 1.0), ([517, 1008], 'UMED', 0.94), ([972, 1010], 'M', 1.0), ([1716, 1016], '3 , 99', 0.53), ([1932, 1016], 'A', 0.18)]
Current group = [([132, 1058], '5213001215419/1238410', 0.99)]
Current group = [([163, 1149], 'FotAL', 0.66), ([1720, 1168], '9e', 0.38), ([1539, 1169], '833', 0.81)]
Current group = [([161, 1243], 'TOTAL-', 0.74), ([403, 1243], 'TVA', 0.99), ([1804, 1270], '56', 1.0), ([1726, 1272], '1', 0.99), ([602, 1293], 'OO"', 0.62), ([480, 1296], '21', 1.0), ([310, 1298], 'A', 0.92), ([162, 1302], 'Tva', 0.68), ([1726, 1322], '1 , 56', 0.53)]
Current group = [([141, 1401], 'CARD', 0.99), ([1717, 1427], '8 . 96', 0.83), ([521, 1443], 'UANDUTE', 0.43), ([310, 1452], 'ART', 0.74), ([136, 1456], 'Nr', 1.0)]
Current group = [([608, 1684], '2 6] 0', 0.44), ([1106, 1687], 'TG 2 T6', 0.12)]
Current group = [([430, 1850], '00/11', 0.54), ([127, 1854], 'EJIKZ :', 0.43), ([522, 1879], "O(Jt J4 , 1' ; ))6 Y2124 14211v1/472 >19' ,10V1 1", 0.0), ([255, 1908], 'UNIu; :', 0.31), ([132, 1910], 'I0', 0.17), ([722, 1922], 'Dain: 10/a895259> UnA:77 47-23', 0.01)]
Current group = [([302, 1956], '00211', 0.77), ([132, 1968], 'BF', 0.31)]
Current group = [([680, 2006], '1I', 0.1), ([974, 2031], 'F [ 5 € ^', 0.16), ([684, 2046], 'E 0 N', 0.54)]
```

- Sort each row based on the x coordinate and construct the final receipt text:
```commandline
JUMBO ECR SRI
STR . COMERTULUI NR 7 ,SAT DOMNESTI
COM DOMNVEST [ JUD ILFOV
TEL 021 2021360
COD IDENTIFICARE FISCALA K0189/1652
20 CUTITARU
POS/TRAN : 011/ 216
Lel
CARIVET 1 OOO A7 S0F BUC ROTI X SPI 1.99 1 , 99
55242800003//1252812
1 o0O BUC X 1 , 49
ETICHETE AUTOCOL IOFX6s 1 49
5480480000.38/1240477
1 OOO BUC X 1 49
ETICHETE AUTOCOL 1OF)9 1 49 A
548049000037/1240476
1 OOO BUC X 3,99
SERVETELE UMED 72BUC M 3 , 99 A
5213001215419/1238410
FotAL 833 9e
TOTAL- Tva A TVA 21 OO" 1 1 , 56 56
Nr CARD ART UANDUTE 8 . 96
2 6] 0 TG 2 T6
EJIKZ : I0 UNIu; : 00/11 O(Jt J4 , 1' ; ))6 Y2124 14211v1/472 >19' ,10V1 1 Dain: 10/a895259> UnA:77 47-23
BF 00211
1I E 0 N F [ 5 € ^
```

As you can see, the final text is not perfect, but this will be solved in the next step where we will define the JSON 
schema of a receipt and will use it alongside the final text obtained at this step as input for the AI in order to
fix the current discrepancies and to structure the data inside a JSON structured output.
