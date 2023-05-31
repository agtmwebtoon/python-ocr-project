import re

'''
Convert Sentence to Markdown Table 

텍스트를 마크다운 테이블 형태로 변화하는 함수
- 완벽하게 변환하지는 않지만 기본적인 형식으로 변환해줌
- 실행 후 각자 원하는 테이블에 간단한 수정 필요  

Example 
구분|죄종|발생검거|건수|
|---|---|---|---|
0|중부|살인|발생|2.0
1|중부|살인|검거|2.0
2|중부|강도|발생|3.0

'''


def strToTable(text):
    sort = ""  # 테이블 정렬 설정
    tableList = []

    sentenceList = text.split('\n')  # 줄바꿈 기준으로 분류
    for idx, sentence in enumerate(sentenceList):
        tableValue = ''
        # print('sentence : ', sentence)
        if idx == 1:
            tableList.append(sort)
        wordList = re.split('[\t]', sentence)  # 빈칸 기준으로 분류
        if idx == 0:
            sort = '|---'*(len(wordList))
        for word in wordList:
            tableValue += word + '|'
            # print('word \t: ', word)
        tableList.append(tableValue)

    # 테이블 텍스트 출력
    for text in tableList:
         print(text)

# 주피터 노트북 텍스트 복사 붙여넣기 후
# 코드에서 인식할 수 있게 텍스트 정리
text ="범죄명   강간.추행   강도   살인   절도   폭력   종합\n" \
      "장소                  \n" \
      "교통수단   0.324718   0.000000   0.000000   0.021027   0.008415   0.070832\n" \
      "금융기관   0.000940   0.011494   0.015385   0.049738   0.001592   0.015830\n" \
      "기타   1.000000   0.770115   1.000000   1.000000   1.000000   0.954023\n" \
      "노상   0.463346   1.000000   0.338462   0.429235   0.929990   0.632207\n" \
      "단독주택   0.185620   0.172414   0.461538   0.103110   0.135661   0.211669\n" \
      "사무실   0.062030   0.091954   0.015385   0.031379   0.046585   0.049467\n" \
      "상점   0.044643   0.390805   0.015385   0.202586   0.032295   0.137143\n" \
      "숙박업소, 목욕탕   0.182801   0.103448   0.061538   0.038097   0.011485   0.079474\n" \
      "아파트, 연립 다세대   0.133459   0.206897   0.184615   0.069200   0.107611   0.140356\n" \
      "역, 대합실   0.085056   0.000000   0.000000   0.016380   0.010310   0.022349\n" \
      "유원지   0.027726   0.022989   0.030769   0.016886   0.016072   0.022888\n" \
      "유흥 접객업소   0.187030   0.149425   0.123077   0.093632   0.100258   0.130684\n" \
      "학교   0.015508   0.000000   0.000000   0.018404   0.007695   0.008321"

strToTable(text)