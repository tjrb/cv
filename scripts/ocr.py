import cv2
import os
import easyocr as eo

#os.chdir('..')
#print(os.getcwd())
reader=eo.Reader(['pt'])
img=cv2.imread("data/images/descarregar.jpg")
#height,width, _ = img.shape()
#print("{}x{}".format(height,width))
#img=cv2.resize(img,(400,400),cv2.IMREAD_UNCHANGED)

img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
imgG = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

imgtrh=cv2.adaptiveThreshold(imgG,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,5)
#_,imgtrh=cv2.threshold(imgtrh,0,255,cv2.THRESH_BINARY_INV)

#contours,_=cv2.findContours(imgtrh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#cv2.drawContours(img,contours,-1,(0,0,200),1)

text=reader.readtext(img)
print(text)

cv2.namedWindow("ori",cv2.WINDOW_AUTOSIZE)
cv2.namedWindow("edi",cv2.WINDOW_AUTOSIZE)
cv2.imshow("ori",img)
cv2.imshow("edi",imgtrh)
cv2.waitKey(0)
cv2.destroyAllWindows()
