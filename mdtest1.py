data = [
    ['이름', '나이', '이메일'],
    ['John', '25', 'john@example.com'],
    ['Alice', '30', 'alice@example.com'],
    ['Bob', '35', 'bob@example.com']
]

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
