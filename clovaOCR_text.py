import requests
import base64
import json
import uuid
import time

# https://console.ncloud.com/ocr/domain

# 위 주소에 GateWay 연결주소 입력
api_url = ''

# Document OCR Secret Key 입력
secret_key = ''

# image 파일 입력
image_file = 'input/1.jpg'
output_file = 'output/output1.json'

# CLOVA OCR 형식
requests_json = {
    'images': [
        {
            'format': 'jpg',
            'name': 'demo',

        }
    ],
    'requestId': str(uuid.uuid4()),
    'version': 'V2',
    'timestamp': int(round(time.time() * 1000))
}

payload = {
    'message': json.dumps(requests_json)
}
files = [
  ('file', open(image_file,'rb'))
]
headers = {
    'X-OCR-SECRET': secret_key,

}

response = requests.request("POST", api_url, headers=headers, data = payload, files = files)
# print(response.text)

info_list = []

result = response.json()

for image in result['images']:
    if 'receipt' in image:
        receipt = image['receipt']
        if 'result' in receipt:
            result_info = receipt['result']
            if 'storeInfo' in result_info:
                store_info = result_info['storeInfo']
                if 'name' in store_info:
                    name = store_info['name']
                    if 'text' in name:
                        info_list.append('name: ' + name['text'])

            if 'paymentInfo' in result_info:
                paymentInfo = result_info['paymentInfo']
                if 'date' in paymentInfo:
                    date = paymentInfo['date']
                    if 'text' in date:
                        info_list.append('date: ' + date['text'])

            if 'totalPrice' in result_info:
                totalPrice = result_info['totalPrice']
                if 'price' in totalPrice:
                    price = totalPrice['price']
                    if 'text' in price:
                        info_list.append('price: ' + price['text'])

for info in info_list:
    print(info)

# print(len(info_list))

# 파일 저장
# with open(output_file, 'w', encoding='utf-8') as outfile:
    # json.dump(res, outfile, indent=4, ensure_ascii=False)


