import requests
import base64
import json
import uuid
import time

# 네이버 Clova OCR API 인증 정보
client_id = 'YOUR_CLIENT_ID'
client_secret = 'VVBkV1VqZGdHcnhqY29TT0JXTHpsWEVQeE91bWhhT2g='

# 이미지 파일 경로
image_path = 'input/1.jpg'

# 이미지 파일을 Base64로 인코딩
with open(image_path, 'rb') as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

# 네이버 Clova OCR API 호출
url = 'https://9llq90txrp.apigw.ntruss.com/custom/v1/22591/1c853d5da8562c67532ab3fc99c8b3ecd9d89a90d1a013f429090e6b526e27ac/general'

# headers = {
#     'Content-Type': 'application/json',
#     'X-OCR-SECRET': client_secret
# }
# data = {
#     'lang': 'ko',
#     'images': [
#         {
#             'format': 'jpg',
#             'data': encoded_image
#         }
#     ]
# }
# response = requests.post(url, headers=headers, json=data)
# result = json.loads(response.content)


request_json = {
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

payload = {'message': json.dumps(request_json).encode('UTF-8')}
files = [
  ('file', open(image_path,'rb'))
]
headers = {
  'X-OCR-SECRET': client_secret
}
response = requests.request("POST", url, headers=headers, data = payload, files = files)
result = json.loads(response.text.encode('utf8'))



# print(result)

# 오류 처리
if 'error' in result:
    print('OCR API 오류:', result['error']['message'])
    exit()

# 추출된 텍스트를 메모장으로 저장
text = ''
for image in result['images']:
    for field in image['fields']:
        for inferText in field['inferText']:
            text += inferText + ' '

# 저장할 파일 경로와 이름
output_path = 'output/output1.txt'

# 추출된 텍스트를 메모장에 저장
with open(output_path, 'w', encoding='utf-8') as output_file:
    output_file.write(text)

print('텍스트 추출이 완료되었습니다. 결과를', output_path, '에 저장했습니다.')
