import requests
import base64
import json
import uuid
import time

# https://console.ncloud.com/ocr/domain

# 위 주소에 GateWay 연결주소 입력
# api_url = 'https://4bkpwd0u5u.apigw.ntruss.com/custom/v1/22680/8753239e7f66c7d91d7966bd868c13c4a9f8a4df644cbcbca8f1f17044628919/document/receipt'
api_url = ''

# Document OCR Secret Key 입력
# secret_key = 'Y2tXWnZWellKeElXYnliSkhkT3RYUXZYSEVzVm12THE='
secret_key = ''

# image 파일 입력
image_file = 'input/3.jpg'

# CLOVA OCR 형식
requests_json = {
    'images': [
        {
            'format': 'jpg',
            'name': 'demo'
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
  ('file', open(image_file, 'rb'))
]
headers = {
    'X-OCR-SECRET': secret_key,

}

response = requests.request("POST", api_url, headers=headers, data = payload, files = files)
# print(response.text)

info_list = []

result = response.json()

# json 파일 저장
# output_file = 'output/output7.json'
# with open(output_file, 'w', encoding='utf-8') as outfile:
#     json.dump(result, outfile, indent=4, ensure_ascii=False)

# 상호명
# 점
# 주소
# 날짜
# 구매품목
# 금액

for image in result['images']:
    if 'receipt' in image:
        receipt = image['receipt']
        if 'result' in receipt:
            result_info = receipt['result']

            if 'storeInfo' in result_info:
                store_info = result_info['storeInfo']
                # 상호명
                if 'name' in store_info:
                    name = store_info['name']
                    if 'text' in name:
                        info_list.append('상호명 : ' + name['text'])
                # 점
                if 'subName' in store_info:
                    subName = store_info['subName']
                    if 'text' in subName:
                        info_list.append('점 : ' + subName['text'])
                # 주소
                for addresses in store_info['addresses']:
                    if 'text' in addresses:
                        info_list.append('주소 : ' + addresses['text'])


            # 날짜
            if 'paymentInfo' in result_info:
                paymentInfo = result_info['paymentInfo']
                if 'date' in paymentInfo:
                    date = paymentInfo['date']
                    if 'text' in date:
                        info_list.append('구매날짜 : ' + date['text'])

            info_list.append('----------')
            # 구매품목
            for subResults in result_info['subResults']:
                for items in subResults['items']:
                    # 상품명
                    if 'name' in items:
                        name = items['name']
                        if 'text' in name:
                            info_list.append('품 명 : ' + name['text'])

                    # 수량
                    if 'count' in items:
                        count = items['count']
                        if 'text' in count:
                            info_list.append('수량 : ' + count['text'])

                    if 'price' in items:
                        price = items['price']
                        # 단가
                        if 'unitPrice' in price:
                            unitPrice = price['unitPrice']
                            if 'text' in unitPrice:
                                info_list.append('단가 : ' + unitPrice['text'])
                        # 금액
                        if 'price' in price:
                            price = price['price']
                            if 'text' in price:
                                info_list.append('금액 : ' + price['text'])
                    info_list.append('----------')

           #총 금액
            if 'totalPrice' in result_info:
                totalPrice = result_info['totalPrice']
                if 'price' in totalPrice:
                    price = totalPrice['price']
                    if 'text' in price:
                        info_list.append('총 금액 : ' + price['text'])



for info in info_list:
    print(info)
    # print(f"- {info}")





