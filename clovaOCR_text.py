import requests
import base64
import json
import uuid
import time
import markdown

# import subprocess
# import pypandoc
# import subprocess

# from markdown2pdf import convert #작동안됨
# import aspose.words as aw #워터마크있음
import aspose.words as aw

# https://console.ncloud.com/ocr/domain

# 위 주소에 GateWay 연결주소 입력
api_url = ''

# Document OCR Secret Key 입력
secret_key = ''

# image 파일 입력
image_file = 'input/5.jpg'

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

store_list = []
product_list = []
total_price = ""

result = response.json()

# json 파일 저장
# output_file = 'output/output7.json'
# with open(output_file, 'w', encoding='utf-8') as outfile:
#     json.dump(result, outfile, indent=4, ensure_ascii=False)


# 상호명
# 점
# 주소
# 날짜

# 상품명
# 수량
# 단가
# 금액

# 총 금액


for image in result['images']:
    if 'receipt' in image:
        receipt = image['receipt']
        if 'result' in receipt:
            result_info = receipt['result']

            # 가게 정보
            if 'storeInfo' in result_info:
                store_info = result_info['storeInfo']
                # 상호명
                if 'name' in store_info:
                    name = store_info['name']
                    if 'text' in name:
                        # info_list.append('상호명 : ' + name['text'])
                        store_list.append(name['text'])
                else:
                    store_list.append('상호명없음')

                # 점
                if 'subName' in store_info:
                    subName = store_info['subName']
                    if 'text' in subName:
                        # info_list.append('점 : ' + subName['text'])
                        store_list.append(subName['text'])
                else:
                    store_list.append('점없음')

                # 주소
                for addresses in store_info['addresses']:
                    if 'text' in addresses:
                        # info_list.append('주소 : ' + addresses['text'])
                        store_list.append(addresses['text'])


            # 날짜
            if 'paymentInfo' in result_info:
                paymentInfo = result_info['paymentInfo']
                if 'date' in paymentInfo:
                    date = paymentInfo['date']
                    if 'text' in date:
                        # info_list.append('구매날짜 : ' + date['text'])
                        store_list.append(date['text'])
            else:
                store_list.append('날짜없음')

            # 품목 정보
            for subResults in result_info['subResults']:
                for items in subResults['items']:
                    # 상품명
                    if 'name' in items:
                        name = items['name']
                        if 'text' in name:
                            # info_list.append('품 명 : ' + name['text'])
                            product_list.append(name['text'])
                    else:
                        product_list.append('품명없음')

                    # 수량
                    if 'count' in items:
                        count = items['count']
                        if 'text' in count:
                            # info_list.append('수량 : ' + count['text'])
                            product_list.append(count['text'])
                    else:
                        product_list.append('수량없음')

                    # 금액 정보
                    if 'price' in items:
                        price = items['price']
                        # 단가
                        if 'unitPrice' in price:
                            unitPrice = price['unitPrice']
                            if 'text' in unitPrice:
                                # info_list.append('단가 : ' + unitPrice['text'])
                                product_list.append(unitPrice['text'])
                        else:
                            product_list.append('단가없음')

                        # 금액
                        if 'price' in price:
                            price = price['price']
                            if 'text' in price:
                                # info_list.append('금액 : ' + price['text'])
                                product_list.append(price['text'])
                        else:
                            product_list.append('금액없음')




            #총 금액
            if 'totalPrice' in result_info:
                totalPrice = result_info['totalPrice']
                if 'price' in totalPrice:
                    price = totalPrice['price']
                    if 'text' in price:
                        # info_list.append('총 금액 : ' + price['text'])
                        totalPrice = price['text']
                        # print(totalPrice)

            else:
                totalPrice = '총금액없음'



# for info in info_list:
#     print(info)
#     print(f"- {info}")

for store in store_list:
    print(store)

print('----------')

for product in product_list:
    print(product)
print('----------')

print(totalPrice)


# data = [
#     ['이름', '나이', '이메일'],
#     ['John', '25', 'john@example.com'],
#     ['Alice', '30', 'alice@example.com'],
#     ['Bob', '35', 'bob@example.com']
# ]

data = [
    ['상호명', '점', '주소', '날짜'],
    store_list,
    ['상품명', '수량', '단가', '금액'],
    product_list,
    '총금액',
    total_price]



# 데이터를 표 형식의 마크다운으로 변환하는 함수
def convert_data_to_markdown(data):
    markdown = '| ' + ' | '.join(data[0]) + ' |\n'
    markdown += '| ' + ' | '.join(['---'] * len(data[0])) + ' |\n'
    for row in data[1:]:
        markdown += '| ' + ' | '.join(row) + ' |\n'
    return markdown

# 마크다운 파일 열기
with open('output.md', 'w', encoding="utf-8") as file:
    # 기존의 마크다운 내용 작성
    file.write('# 데이터\n\n')

    # 파이썬에서 처리된 데이터를 마크다운으로 변환하여 삽입
    markdown_data = convert_data_to_markdown(data)
    file.write(markdown_data)


input_file = 'output.md'
output_file = 'output.pdf'

# 명령 실행
subprocess.run(['pandoc', input_file, '-o', output_file])


# input_file = 'output.md'
# output_file = 'output.pdf'
#
# # 마크다운 파일을 PDF로 변환
# pypandoc.convert_file(input_file, 'pdf', outputfile=output_file, extra_args=['-s'])

