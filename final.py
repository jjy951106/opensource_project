import cv2
import mahotas
import sys
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
import pytesseract
import argparse
import os

path =  './8'

def fourier():
	img = cv2.imread(path+'.jpg', cv2.IMREAD_GRAYSCALE)
	
    #푸리에 변환 함수들
	f = np.fft.fft2(img)
	fshift = np.fft.fftshift(f)

	rows , cols = img.shape
	crow, ccol = int(rows/2), int(cols/2)

    #범위 상수. 여러번 실시하여 적당한 상수를 찾음.
	ranges = 60

	fshift[crow-ranges:crow+ranges, ccol-ranges:ccol+ranges] = 0

    #변환된 이미지에서 특정 부분만 추출.
	f_ishift = np.fft.ifftshift(fshift)
	img_back = np.fft.ifft2(f_ishift)
	img_back = np.abs(img_back) 

	cv2.imwrite(path+'2.jpg',img_back)

#fourier()

img = cv2.imread(path+'.jpg',0)
img = cv2.medianBlur(img,5)

ret,th1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
th2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
             cv2.THRESH_BINARY,11,2)
th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
             cv2.THRESH_BINARY,11,2)

tessdata_dir_config = '--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata"'
tesseract_path = 'C:\\Program Files (x86)\\Tesseract-OCR'
pytesseract.pytesseract.tesseract_cmd = tesseract_path + '\\tesseract'
# Example config: '--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata"'
# It's important to include double quotes around the dir path.

text = pytesseract.image_to_string(th1, lang='kor', config=tessdata_dir_config)
print(text)
