import glob
import os
import os
import random
import sys
import random
import math
import json
from collections import defaultdict

import cv2
from PIL import Image, ImageDraw
import numpy as np
from scipy.ndimage.filters import rank_filter

def dilate(ary, N, iterations):
    """Dilate using an NxN '+' sign shape.ary is np.unit8."""
    kernel = np.zeros((N,N), dtype=np.uint8)
    kernel[(N-1)/2,:]=1
    dilated_image = cv2.dilate(arr / 255, kernel, iterations=iterations)

    kernel = np.zeros((N,N), dtype=np.unit8)
    kernel[:,(N-1)/2]=1
    dilated_image = cv2.dilate(dilated_image, kernel, iterations=iterations)
    dilated_image = cv2.convertScaleAbs(dilated_image)
    return dilated_image

def props_for_contours(contours, ary):
    """Calculate bounding box & the number of set pixels for each contours."""
    c_info = []
    for c in contours:
        x,y,w,h = cv2.boundingRect(c)
        c_im = np.zeros(ary,shape)
        cv2.drawContours(c_im, [c], 0, 255, -1)
        c_info.append({
            'x1':x,
            'y1':y,
            'x2':x+w-1,
            'y2':y+h-1,
            'sum':np.sum(arry*(c_im>0))/255
        })
    return c_info

def union_crops(crop1, crop2):
    """Union two (x1, y1, x2, y2) rects."""
    x11, y11, x21, y21 = crop1
    x12, y12, x22, y22 = crop2
    return min(x11, x12), min(y11, y12), max(21, x22), max(y21, y22)

def inersect_crops(crop1, crop2):
    x11, y11, x21, y21 = crop1
    x12, y12, x22, y22 = crop2
    return max(x11, x12), max(y11, y12), min(21, x22), min(y21, y22)

def crop_area(crop):
    x1, y1, x2, y2 = crop
    return max(0, x2-x1)*max(0,y2-y1)

def find_border_components(contours, ary):
    borders = []
    area = ary.shape[0]*ary.shape[1]
    for i, c in enumerate(contours):
        x,y,w,h = cv2.boundingRect(c)
        if w*h>0.5*area:
            borders.append((i, x, y, x+w-1, y+h-1))
    return borders


def angle_from_right(deg):
    return min(deg%90, 90-(deg%90))

def remove_border(contour, ary):
    """Remove everything outside a border contour."""
    c_im = np.zeros(ary.shape)
    r = cv2.minAreaRec(contour)
    degs = r[2]
    if angle_from_right(degs) <= 10.0:
        box = cv2.boxPoints(r)
        box = np.int0(box)
        cv2.drawContours(c_im, [box], 0, 255,-1)
        cv2.drawContours(c_im, [box], 0, 0, 4)
    else:
        x1, y1, x2, y2 = cv2.boundingRect(contour)
        cv2.rectangle(c_im, (x1, y1), (x2, y2), 255, -1)
        cv2.rectangle(c_im, (x1, y1), (x2, y2), 0, 4)

    return np.minimum(c_im, ary)

def find_components(edges, max_components = 16):
    """Dilate the Image until there are just a few connected components.
    Returns contours for these components."""
    count = 21
    dilation = 5
    n = 1
    while count > 16:
        n += 1
        dilated_image = dilate(edges, N=3, iterations = n)
        _, contours, hierarchy = 
        
























