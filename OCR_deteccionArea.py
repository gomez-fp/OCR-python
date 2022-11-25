import cv2
import numpy as np
import imutils
import pytesseract
import mysql.connector
import os
import time

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract' 
cap = cv2.VideoCapture(0)

from mysql.connector import errorcode

mydb = mysql.connector.connect(user='root', password='pipe3108217253',
                                 host='127.0.0.1',
                                 database='vangard')
mycursor = mydb.cursor()

while True:
    ret, frame = cap.read()
    #cv2.imshow('freme', frame)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    area_pts = np.array([[100,80], [565,80], [565,180], [100,180]])  #creacion de area de deteccion
    cv2.drawContours(frame, [area_pts], -1, (0,255,0), 2)

    imAux = np.zeros(shape=(gray.shape[:2]), dtype=np.uint8)
    imAux = cv2.drawContours(imAux, [area_pts], -1, (255), -1)
    image_area = cv2.bitwise_and(gray, gray, mask=imAux)

    #imgBinary = cv2.adaptiveThreshold(image_area, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 85, -30)
    #canny2 = cv2.Canny(image_area,110,200)
    #canny2 = cv2.dilate(canny2,None,iterations=1)
    mascara = np.uint8((image_area<130)*250)

    text = pytesseract.image_to_string(mascara, config ="--psm 10 -c tessedit_char_whitelist=0123456789")
    print('Texto=',text)
    print(len(text))
    time.sleep(1.5)

    hImg,wImg,_= frame.shape
    boxes = pytesseract.image_to_boxes(mascara)
    for b in boxes.splitlines():
        b = b.split(' ')
        x,y,w,h = int(b[1]),int(b[2]),int(b[3]),int(b[4])
        cv2.rectangle(mascara ,(x,hImg-y),(w,hImg-h),(0,0,255),3)
        cv2.putText(mascara, b[0],(x,hImg-y+25),cv2.FONT_HERSHEY_COMPLEX,1,(50,50,255),2)

    if len(text) == 0 or len(text)<5:
        print("sindato")
        
    #if text == text or text == text+1:
        #print("valor tacometro = ",text)
        #sql = "INSERT INTO numeros (Name) VALUES ('{0}')".format(text)
        #mycursor.execute(sql)

        #mydb.commit()
        #print(mycursor.rowcount, "record inserted.")
        
    cv2.imshow('normal', frame)
    cv2.imshow('mascara', mascara)
    #cv2.imshow('canny2', canny2)
    #cv2.imshow('imgBinary', imgBinary)
    
    
    if cv2.waitKey(1) &  0xFF == ord('q'):
         break
cap.release()
cv2.destroyAllWindows()
