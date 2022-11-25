import cv2
import numpy as np
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract' 

placa = []
imagen = cv2.imread('contador.jpeg')
gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
#gray = cv2.blur(gray,(3,3))
canny = cv2.Canny(gray,40,300)
canny = cv2.dilate(canny,None,iterations=0)

area_pts = np.array([[400,480], [765,480], [765,580], [400,580]])  #creacion de area de deteccion
cv2.drawContours(imagen, [area_pts], -1, (0,255,0), 2)

imAux = np.zeros(shape=(gray.shape[:2]), dtype=np.uint8)
imAux = cv2.drawContours(imAux, [area_pts], -1, (255), -1)
image_area = cv2.bitwise_and(gray, gray, mask=imAux)

#fgmask = fgbg.apply(image_area)
#fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
#fgmask = cv2.dilate(fgmask, None, iterations=2)

#print('area=',area_pts)
canny2 = cv2.Canny(image_area,140,350)
canny2 = cv2.dilate(canny2,None,iterations=1)
mascara = np.uint8((image_area<130)*250)

#text = pytesseract.image_to_string(mascara, config ="--psm 10")
#print('Texto=',text)
### DETECCION POR CARACTER Y MUESTRA EN AREA
hImg,wImg,_= imagen.shape
boxes = pytesseract.image_to_boxes(imagen)
for b in boxes.splitlines():
    b = b.split(' ')
    x,y,w,h = int(b[1]),int(b[2]),int(b[3]),int(b[4])
    cv2.rectangle(imagen ,(x,hImg-y),(w,hImg-h),(0,0,255),3)

cv2.imshow('umbral', mascara)
cv2.imshow('Imagen', imagen)
#cv2.imshow('Imagen2', gray)
#cv2.imshow('imAux', image_area)
cv2.moveWindow('Imagen',45,10)
cv2.waitKey(0)
