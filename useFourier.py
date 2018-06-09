import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import sys

path =  './' + sys.argv[1]

def fourier():
	img = cv2.imread(path+'.jpg', cv2.IMREAD_GRAYSCALE)
	
    #푸리에 변환 함수들
	f = np.fft.fft2(img)
	fshift = np.fft.fftshift(f)

	rows , cols = img.shape
	crow, ccol = int(rows/2), int(cols/2)

    #범위 상수. 여러번 실시하여 적당한 상수를 찾음.
	ranges = 5

	fshift[crow-ranges:crow+ranges, ccol-ranges:ccol+ranges] = 0

    #변환된 이미지에서 특정 부분만 추출.
	f_ishift = np.fft.ifftshift(fshift)
	img_back = np.fft.ifft2(f_ishift)
	img_back = np.abs(img_back)

	cv2.imwrite(path + '_Fourier.jpg',img_back)

fourier()

