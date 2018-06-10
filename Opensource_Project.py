from PIL import Image
import pytesseract
import pymysql
import cv2
import re
import os
import sys
import numpy as np
import mahotas

tessdata_dir_config = '--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata"'
tesseract_path = 'C:\\Program Files (x86)\\Tesseract-OCR'
pytesseract.pytesseract.tesseract_cmd = tesseract_path + '\\tesseract'

conn = pymysql.connect(host='localhost', user='root',
                       password='1234',db='food_additive', charset='utf8')
cur = conn.cursor()

conn2 = pymysql.connect(host='localhost', user='root',
                       password='1234',db='nodejsconnect', charset='utf8')
cur2 = conn2.cursor()

arg_id = sys.argv[1]
arg_path = sys.argv[2]
#arg_id = '1'
#arg_path = 'picture\\8.jpg'

name_db = []
search_db = []
result = []
path = './' + arg_path.replace('.jpg','')

def getName():
    global name_db
    global search_db
    cur.execute('select _name from food_additive')
    rows = cur.fetchall()

    for data in rows:
        name_db.append(str(data).replace('("','').replace('",)','').replace("',)",'').replace("('",''))

    for data in name_db:
        search_db.append(str(data).replace('("','').replace('",)','').replace('.','').replace(',','')
                         .replace('-','').replace('α','').replace('β','').replace('δ','').replace('ｄ','')
                         .replace('5','').replace('d','').replace('D','').replace('l','').replace("'",'')
                         .replace('L','').replace('N','').replace('γ','').replace('ε','').replace('ε','')
                         .replace('  ','').replace(' ','').replace("',)",'').replace("('",''))

def ocr_tesseract(filename):
    global result
    im = Image.open(filename + '.jpg')
    text = pytesseract.image_to_string(im, lang='kor', config=tessdata_dir_config)
    text = text.replace(':','')
    text = text.replace('\n','')
    text = text.replace('ㅣ','')
    text = text.replace('~','')
    text = text.replace('  ','').replace(',','')
    text = text.replace('외국','외귝').replace('국내','귝내')
    
    text2 = text.replace(' ','')
    
    for i in range(0, len(name_db), 1):
        if name_db[i] in text2:
            result.append(i)

    for i in range(0, len(search_db), 1):
        if str(search_db[i]) in text2:
            result.append(i)

    os.remove(filename + '.jpg')

def canny():
    Number=path+'.jpg'
    img=cv2.imread(Number,cv2.IMREAD_COLOR)
    copy_img=img.copy()
    img2=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    cv2.imwrite(path+'_Gray.jpg',img2)
    enhance_black(path+'_Gray')
    blur = cv2.GaussianBlur(img2,(3,3),0)
    cv2.imwrite(path+'_Blur.jpg',blur)
    enhance_black(path + '_Blur')
    canny=cv2.Canny(blur,100,200)
    cv2.imwrite(path+'_Canny.jpg',canny)
    enhance_white(path+'_Canny')
    
def thresholding():
    img = cv2.imread(path+'.jpg',0)
    ret,th1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
    th2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
                                cv2.THRESH_BINARY,55,4)
    th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                                cv2.THRESH_BINARY,55,4)
    mahotas.imsave(path + '_Binary.jpg',th1)
    enhance_black(path + '_Binary')
    mahotas.imsave(path + '_Mean.jpg',th2)
    enhance_black(path + '_Mean')
    mahotas.imsave(path + '_Guassian.jpg',th3)
    enhance_black(path + '_Guassian')

def fourier():
    img = cv2.imread(path+'.jpg', cv2.IMREAD_GRAYSCALE)

    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)

    rows , cols = img.shape
    crow, ccol = int(rows/2), int(cols/2)

    ranges = 10

    fshift[crow-ranges:crow+ranges, ccol-ranges:ccol+ranges] = 0

    f_ishift = np.fft.ifftshift(fshift)
    img_back = np.fft.ifft2(f_ishift)
    img_back = np.abs(img_back)

    cv2.imwrite(path + '_Fourier.jpg',img_back)
    enhance_white(path + '_Fourier')

def enhance_black(filename):
    img=cv2.imread(filename + '.jpg',0)
    kernel = np.ones((2,2),np.uint8)
    er_plate = cv2.erode(img,kernel,iterations=1)
    er_invplate = er_plate
    cv2.imwrite(filename +'_enhace.jpg',er_invplate)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    ocr_tesseract(filename)
    ocr_tesseract(filename +'_enhace')

def enhance_white(filename):
    img=cv2.imread(filename + '.jpg',0)
    kernel = np.ones((2,2),np.uint8)
    dil_plate = cv2.dilate(img,kernel,iterations = 1)
    dil_invplate = dil_plate
    cv2.imwrite(filename +'_enhace.jpg',dil_invplate)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    ocr_tesseract(filename)
    ocr_tesseract(filename +'_enhace')
    
if __name__ == '__main__':
    getName()
    thresholding()
    canny()
    fourier()
            
    result = list(set(result))

    data = ""
        
    for x in result:
        cur.execute("select * from food_additive where _name='%s'" %name_db[x])
        rows = cur.fetchall() # 전부 가져옴
        data += str(rows).replace("'","").replace("((","").replace("),)","")
        data += '/'
    cur2.execute("update photopath set context2 = '%s' where id = %s" %(data, arg_id))
        #for data in rows:
        #print(data)
    conn2.commit() # 작업을 db로 넘기는 명령.
    cur2.close()  #cur을 먼저 종료하고
    conn2.close() #conn을 종료
    cur.close()  #cur을 먼저 종료하고
    conn.close() #conn을 종료
    
    print('1')
