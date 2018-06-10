from PIL import Image
import pytesseract
import pymysql
import cv2
import re

tessdata_dir_config = '--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata"'
tesseract_path = 'C:\\Program Files (x86)\\Tesseract-OCR'
pytesseract.pytesseract.tesseract_cmd = tesseract_path + '\\tesseract'

conn = pymysql.connect(host='localhost', user='root',
                       password='1234',db='food', charset='utf8')
cur = conn.cursor()

conn2 = pymysql.connect(host='localhost', user='root',
                       password='1234',db='nodejsconnect', charset='utf8')
cur2 = conn2.cursor()

name_db = []
search_db = []
result = []

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
    image_file = './' + filename + '.jpg'
    im = Image.open(image_file)
    text = pytesseract.image_to_string(im, lang='kor', config=tessdata_dir_config)
#    print('-------------------- ' + filename + ' ----------------------')
    text = text.replace(':','')
    text = text.replace('\n','')
    text = text.replace('ㅣ','')
    text = text.replace('~','')
    text = text.replace('  ','').replace(',','')
    
    text2 = text.replace(' ','')
    
    for i in range(0, len(name_db), 1):
        if name_db[i] in text2:
            result.append(i)

    for i in range(0, len(search_db), 1):
        if str(search_db[i]) in text2:
            result.append(i)
            
    result = list(set(result))



    
if __name__ == '__main__':
    ss = '_enhace'
    getName()
#    for i  in range(1, 14, 1):
    for i  in range(8, 9, 1):
        #print('-------------------- ' + str(i) + '번째 이미지 ----------------------')
        ocr_tesseract(str(i))
        ocr_tesseract(str(i) + '_Binary')
        ocr_tesseract(str(i) + '_Guassian')
        ocr_tesseract(str(i) + '_Mean')
        ocr_tesseract(str(i) + '_Fourier')
        ocr_tesseract(str(i) + '_Blur')
        ocr_tesseract(str(i) + '_Gray')
        ocr_tesseract(str(i) + '_Canny')
        ocr_tesseract(str(i) + ss)
        ocr_tesseract(str(i) + '_Binary' + ss)
        ocr_tesseract(str(i) + '_Guassian' + ss)
        ocr_tesseract(str(i) + '_Mean' + ss)
        ocr_tesseract(str(i) + '_Fourier' + ss)
        ocr_tesseract(str(i) + '_Blur' + ss)
        ocr_tesseract(str(i) + '_Gray' + ss)
        ocr_tesseract(str(i) + '_Canny' + ss)

        data = ""
        
        for x in result:
            cur.execute("select * from food_additive where _name='%s'" %name_db[x])
            rows = cur.fetchall() # 전부 가져옴
            data += str(rows).replace("'","").replace("((","").replace("),)","")
            data += '/'
        print(data)
        print("update photopath set context2 = '%s' where path = '%s'" %(data, str(8)))
        cur2.execute("update photopath set context = '%s' where path = '%s'" %(data, str(8)))
            #for data in rows:
                #print(data)
        conn2.commit() # 작업을 db로 넘기는 명령.
        cur2.close()  #cur을 먼저 종료하고
        conn2.close() #conn을 종료
        cur.close()  #cur을 먼저 종료하고
        conn.close() #conn을 종료

        result = []
