import os
import json
import pandas as pd
import subprocess

# 유튜브 URL 목록
urls = [
    'https://www.youtube.com/shorts/FLvMtj0NnNk'
]

# 댓글을 저장할 CSV 파일 이름
merged_csv_file = 'MergedYoutubeComments.csv'

# 여러 URL을 순회하며 댓글을 추출
for i, url in enumerate(urls):
    # JSON 파일 이름
    json_file = f'YoutubeComments_{i}.json'

    # youtube-comment-downloader 명령어 실행
    try:
        subprocess.run(
            ['youtube-comment-downloader', '--url', url, '--output', json_file],
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"명령어 실행 중 오류 발생: {e}")
        continue

    # JSON 파일 읽기
    with open(json_file, 'r', encoding='utf-8') as f:
        json_data = []
        for line in f:
            json_data.append(json.loads(line))

    # JSON 데이터를 DataFrame으로 변환
    df = pd.DataFrame(json_data)

    # CSV 파일로 저장 (각 URL별로 저장하고 싶으면 주석 해제)
    csv_file = f'YoutubeComments_{i}.csv'
    df.to_csv(csv_file, index=False, encoding='utf-8-sig')  # 한글 깨짐 방지

    # 기존 CSV 파일과 병합
    if os.path.exists(merged_csv_file):
        df.to_csv(merged_csv_file, mode='a', index=False, header=False, encoding='utf-8-sig')
    else:
        df.to_csv(merged_csv_file, index=False, encoding='utf-8-sig')

    # JSON 파일 삭제
    os.remove(json_file)

print(f"모든 URL의 댓글이 {merged_csv_file} 파일에 저장되었습니다.")
