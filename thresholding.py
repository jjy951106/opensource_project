import cv2
import mahotas
import sys
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image

path =  './' + sys.argv[1]

img = cv2.imread(path+'.jpg',0)
# img = cv2.medianBlur(img,5)

ret,th1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
th2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
             cv2.THRESH_BINARY,55,4)
th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
             cv2.THRESH_BINARY,55,4)

mahotas.imsave(path + '_Binary.jpg',th1)
mahotas.imsave(path + '_Mean.jpg',th2)
mahotas.imsave(path + '_Guassian.jpg',th3)
