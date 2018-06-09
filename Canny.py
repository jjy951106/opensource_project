import cv2
import numpy as np
import pytesseract
from  PIL import Image
import sys

path =  './' + sys.argv[1]

def ExtractNumber():
          Number=path+'.jpg'
          img=cv2.imread(Number,cv2.IMREAD_COLOR)
          copy_img=img.copy()
          img2=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
          cv2.imwrite(path+'_Gray.jpg',img2)
          blur = cv2.GaussianBlur(img2,(3,3),0)
          cv2.imwrite(path+'_Blur.jpg',blur)
          canny=cv2.Canny(blur,100,200)
          cv2.imwrite(path+'_Canny.jpg',canny)
          
ExtractNumber()
