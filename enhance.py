#!/usr/bin/etc python

import cv2
import numpy as np
from  PIL import Image
import sys

#path =  './' + sys.argv[1]
path =  './'

def enhance_black(filename):
    Number=path+ filename +'.jpg'
    img=cv2.imread(Number,0)
    kernel = np.ones((2,2),np.uint8)
    er_plate = cv2.erode(img,kernel,iterations=1)
    er_invplate = er_plate
    cv2.imwrite(path+ filename +'_enhace.jpg',er_invplate)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def enhance_white(filename):
    Number=path+ filename +'.jpg'
    img=cv2.imread(Number,0)
    kernel = np.ones((2,2),np.uint8)
    dil_plate = cv2.dilate(img,kernel,iterations = 1)
    dil_invplate = dil_plate
    cv2.imwrite(path+ filename +'_enhace.jpg',dil_invplate)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

for i in range(1,14,1):
    enhance_black(str(i))
    enhance_black(str(i) + '_Binary')
    enhance_black(str(i) + '_Blur')
    enhance_black(str(i) + '_Gray')
    enhance_black(str(i) + '_Guassian')
    enhance_black(str(i) + '_Mean')

    enhance_white(str(i) + '_Fourier')
    enhance_white(str(i) + '_Canny')
    

    
          

