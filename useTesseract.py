from PIL import Image
import pytesseract

tessdata_dir_config = '--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata"'
tesseract_path = 'C:\\Program Files (x86)\\Tesseract-OCR'
pytesseract.pytesseract.tesseract_cmd = tesseract_path + '\\tesseract'


def ocr_tesseract():
    image_file = 'F:\\Users\\dogyun\\Desktop\\까치\\scannedImage.jpg'
    im = Image.open(r'F:\\Users\\dogyun\\Desktop\\까치\\scannedImage.jpg')
    print(pytesseract.image_to_string(im, lang='kor', config=tessdata_dir_config))
    im.show()

if __name__ == '__main__':
    ocr_tesseract()
    
