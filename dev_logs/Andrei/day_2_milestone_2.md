# DAY 1 (October 11, 2026)

Ok, for the moment I am still at the cutting just the receipt out of the image. The thing is that I need to undestand 
the Canny edge detection algorithm in order to do that...

Also, after I managed to detect the edges, I need to perform additional checks so that I can correctly identify the 
edge with the biggest area and with a shape that resembles a receipt. 

The process is as follows: 

- We will try to cut the image first:
  - to cut the image we performed initially:
    - grayscale 
    - applied the canny edge detection algorithm on the image to detect all the edges
    - tried to select the correct contour based on the max area and the shaped it defined 
    (we are interested in 4-sided polygons)
    - based on the selected contour, we cut the raw image 
    - `Conclusion`: we could not correctly select the right contour as the contour we wanted had interrupted margins
  - Next, we tried to apply thresholding after grayscale. This approach resulted in the detection of the correct contour

Result comparison:
- Raw image: 
```commandline
['JUuMEO EcR', 'SRL', 'SIR.COMERTUHL UI, nR', 'SAT (tcmnest[', 'COM DDOMNESTL,JU) . IL Fov', 'TFL 021 .2021360', 'COD   ZDE NTIF ICARE', '[', 'iSCALA K018sy216452', '20 CUTITARU', "POS/TRAN : 011/ '216", 'Lel', '1 ,00O', 'EUC X 1,99', 'CARNET A7 5uF Roti Spi', '1,99 ^', '552428000037/1252812', '1,00o', 'BUC X 1 ,49', 'ETICHETE  AUTOCoL   IOFXe;', '1,49 /', '548048000038/1240477', '1,000', 'BUC X', '1 ,49', 'ETICHETE AUTOCOL', 'JOFX9', '1,49 A', '548049000037/1240476', '1,0oo', 'BUC x 3,99', 'SERVETELE UED 725UC M', '3,99 A', '5213001215419/1238410', 'TOTAL', '8', '96', 'total  TVA', '1,56', 'TvA A', '21 ,OO', '1,56', 'CARD', 'Nr', 'ART', 'VANDUTE', '8,96', '2 61010710216 5', 'EJMRZ =', '06y211', "T7Thi : 76XM Ys7'aYwv/lzulu/472399at?1 1", '1', '(u6211', 'Ttn : 761/161/*2n2>', 'Mra ;', 'K', '7UJLHI %57999467', '8 0 N', '1T S€ ^7', '1/-4/-23']
```

- Cut operation applied on the raw image:
```commandline
['JUMEO ECR', 'SRL', 'SIR.COMERTUHL U1, nR', 'SAT (DomneST[', 'COM DDOMNESTL,JU . IL Fo', 'TFL 021 .2021360', 'COD   IDFNTIFICARE FiSCALA  K0189216452', '20 CUTITARU', "Pos/tRAn : 011/ '216", 'Ler', '1 ,00o', 'BUC X 1,99', 'CARNE T A7 5uF Roti SPi', '1,99 ^', '552428000J037/1252812', '1,O0o', 'BUC X 1,49', 'ETICHETE AUTOCOL   IOFYes', '1,49 /', '548048000038/1240477', '1,000', 'BUC X', '1,49', 'ETICHETE  AUTOCOL', 'JOFX9', '1,49 A', '548049000037/1240476', '1,OoO', 'BUC x 3,99', 'SERVETELE UMED 72EUC M', '3,99 A', '5213001215419/1238410', 'TOTAL', '96', 'total  TVA', '1,56', 'TvA A', '21 ,0O', '1,56', 'CARD', 'Nr', 'ART', 'VaNDUIE', '8,96', '2 61010710216', 'EJTRZ : 06y211', "Il> UNJI ' :", '~7874 U Y57" 4wMVZutzuHnu/A72319auvt', '1', '(u6y211', 'Tota . 767/ I(w* 2n2>', 'OA', 'K', 'HUJLHI %5799467', '6 0 N F 1 5 € A /', '1/4/-23']
```

- Apply grayscale after cutting:
```commandline
['JUMEO ECR', 'SRL', 'SIR.COMERTUHL U1, nR', 'SAT (DomneST[', 'COM . DOMNE ST[,JU) . IL Fov', 'TFL 021 .2021360', 'COD   IDFNTIFICARE FiSCALA  K0189216452', '20 CUTITARU', "Pos/tRAn : 011/ '216", 'Ler', '1 ,00o', 'BUC X 1,99', 'CARNE T A7 5uF Roti SPi', '1,99 ^', '552428000J037/1252812', '1,O0o', 'BUC X 1,49', 'ETICHETE   AUTOCOL   IOFXes', '1,49 /', '548048000038/1240477', '1,000', 'BUC X', '1,49', 'ETICHETE  AUTOCOL', 'JOFX9', '1,49 A', '548049000037/1240476', '1,Ooo', 'BUC x 3,99', 'SERVETELE UMED 72EUC M', '3,99 A', '5213001215419/1238410', 'TOTAL', '96', 'total  TVA', '1,56', 'TvA A', '21 ,OOK', '1 ,56', 'CARD', 'Nr', 'ART', 'VaNDUIE', '8,96', '2 61010710216', 'EJIRZ : 06y211', "Il UJt ' :", '~7874 U Y57" 4wMVZutzuHnu/A72319auvt', '06s211', 'Tat^ . 761/ I6* 2n12', 'OA', 'K/', 'HULH /519996', '8 0 N | 1 5 € A 7', '1/4/-23']
```

- Apply grayscale and thresholding after cutting:
```commandline
["IHu1 [ ; | 'a", '.Il; mu tuh uu m:', '2i |', '1u 34 ` ,1 7', "Fim.uA '1 , I' h FFu", '1v/|', '/1j% /+', '124 Id h  Jizua', 'f  h Mjan', '/ j i', 'UAM1î% )', 'F€, NaAn.', '{JF 1', '2J6 ,', 'J .Fu Ji', 'Țsh/ .', '1,4', 'Eiswu', "h 'H", '1ai', '1 , : %', "',h2 {a n J 13/!127/812", '_M Hn', '[IH ` X', '49)', 'EMOic Auta', "Iuj 'fi", '1.49', "'543)HSXHCN J38/1240)4777", '1 .(ufuj', 'EUC X', '1,4', 'l:i [CHEYE  AiTC)CO)', 'JIFX9', '1.4 A', '5+{84)4194c77137/1240j765', '1 ,Ooo', 'BIJC X 3,90', 'shETELE (ED 72BUJC; M', '3 ,97)', 'A', '5213701215419/12384J0', 'TOTAL', '83', '96', 'Jofal', 'TVA', '556', 'NA A', "'21 , (Joy", '1,56', 'CAk)', 'N:1 . Vhmh NJIi', '8 ,96', '1105776', 'ill', 'M1/| /', 'Ili /aI1', '"Annn,|\' ,PRAonhnusm?;nhll', '7/1// /', "hln J1 'Jn", 'I::|/ ./', '2 >', "'HhH  ,75 ;J M)", '12111']
```

- Resize after the cutting (best result so far):
```commandline
['JUMBO', 'EC R', 'SRI', 'STR . COMERTULUI', 'NR', '7 ,SAT', 'DOMNESTI', 'COM', 'DOMNVEST [', 'JUD', 'ILFOV', 'TEL', '021', '2021360', 'COD', 'IDENTIFICARE', 'FISCALA', 'K0189/1652', '20', 'CUTITARU', 'POS/TRAN :', '011/', '216', 'Lel', '1', 'OOO', 'BUC', 'X', '1.99', 'CARIVET', 'A7', 'S0F', 'ROTI', 'SPI', '1 , 99', '55242800003//1252812', '1', 'o0O', 'BUC', 'X', '1 , 49', 'ETICHETE', 'AUTOCOL', 'IOFX6s', '1', '49', '548048000038/1240477', '1', 'OOO', 'BUC', 'X', '1', '49', 'ETICHETE', 'AUTOCOL', '1OFX9', '1', '49', 'A', '548049000037/1240476', '1', 'OOO', 'BUC', 'X 3,99', 'SERVETELE', 'UMED', '72BUC', 'M', '3 , 99', 'Â', '5213001215419/1238410', 'FotAL', '9e5', 'TOTAL-', 'TVA', '1', '56', 'Tva', 'A', '21', 'OO"', '1 , 56', 'CARD', 'Nr-', 'ART .', 'VANDUTE', '8 . 96', '2 6] 0 1', '1ro 2 T6', 'EJIRZ :', '00/11', 'I0', 'UNiu :', "O(Jt J4 , 1'  ))6 Y2t24 42151/472 >19' ,A0V1 1", 'BF', '00211', 'DATA: 10/10/20120', 'OFA : 1/-4/-23', '11', '7UUUS 19)EU)', 'E 0 N', 'F T s C ^ |']
```

UPDATE: 

I refactored the functions from preprocessing and tried the following approaches:
- Approach 1: grayscale -> threshold -> cut -> resize -> OCR
- Approach 2: grayscale -> threshold -> cut -> resize -> grayscale -> OCR
- Approach 2: grayscale -> threshold -> cut -> resize -> grayscale -> Threshold -> OCR

The result is that the best approach is the first one. The grayscale approach is not adding significant value. And the thresholding is far from the desired result.

## Resources 

- [EasyOCR Documentation](https://www.jaided.ai/easyocr/)

