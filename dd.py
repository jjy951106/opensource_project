from PIL import Image
import http.client, urllib.request, urllib.parse, urllib.error, base64, json

def print_text(json_data):
    result = json.loads(json_data)
    for l in result['regions']:
        for w in l['lines']:
            line = []
            for r in w['words']:
                line.append(r['text'])
            print(' '.join(line))
    return

# Project Oxford API를 호출하는 로직
def ocr_project_oxford(headers, params, data):
    conn = http.client.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
    conn.request("POST", "/vision/v1.0/ocr?%s"  % params, data, headers)
    response = conn.getresponse()
    data = response.read().decode()
    print(data + "\n")
    print_text(data)
    conn.close()
    return

if __name__ == '__main__':
    headers = {
        # 헤더 요청
        'Content-Type' : 'application/octet-stream',
        'Ocp-Apim-Subscription-Key' : 'b1a329ebb78a4995a0462725f40e3013', # project oxford 인증키 입력
        }
    params = urllib.parse.urlencode({
        #파라미터 요청
        'language': 'ko',
        'detectOrientation ': 'true',
        })
    data = open('scannedImage.png', 'rb').read()

    try:
        image_file = 'scannedImage.png'
        im = Image.open(image_file)
        #im.show()
        ocr_project_oxford(headers, params, data)
    except Exception as e:
        print(e)
        
