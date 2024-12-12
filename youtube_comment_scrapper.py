import os
import json
import pandas as pd
import subprocess
from datetime import datetime

def download_comments(url, output_file):
    """
    youtube-comment-downloader를 사용하여 특정 URL의 댓글을 JSON 파일로 다운로드합니다.
    """
    try:
        subprocess.run(
            ['youtube-comment-downloader', '--url', url, '--output', output_file],
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"명령어 실행 중 오류 발생: {e}")
        return False
    return True

def json_to_dataframe(json_file):
    """
    JSON 파일을 읽어 Pandas DataFrame으로 변환합니다.
    """
    with open(json_file, 'r', encoding='utf-8') as f:
        json_data = [json.loads(line) for line in f]
    return pd.DataFrame(json_data)

def filter_comments_by_date(df, start_date, end_date):
    """
    DataFrame에서 특정 기간 내 댓글만 필터링합니다.
    start_date, end_date: 'YYYY-MM-DD' 형식의 문자열
    """
    # UNIX 타임스탬프를 datetime으로 변환
    df['time_parsed'] = pd.to_datetime(df['time_parsed'], unit='s')
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    return df[(df['time_parsed'] >= start_date) & (df['time_parsed'] <= end_date)]

def save_dataframe_to_csv(df, csv_file, append=False):
    """
    DataFrame을 CSV 파일로 저장합니다.
    """
    if append and os.path.exists(csv_file):
        df.to_csv(csv_file, mode='a', index=False, header=False, encoding='utf-8-sig')
    else:
        df.to_csv(csv_file, index=False, encoding='utf-8-sig')

def process_youtube_comments(urls, merged_csv_file, start_date=None, end_date=None):
    """
    여러 YouTube URL에서 댓글을 다운로드하고 병합된 CSV 파일로 저장합니다.
    """
    for i, url in enumerate(urls):
        json_file = f'YoutubeComments_{i}.json'

        # 댓글 다운로드
        if not download_comments(url, json_file):
            continue

        # JSON 데이터를 DataFrame으로 변환
        df = json_to_dataframe(json_file)

        # 특정 기간으로 댓글 필터링
        if start_date and end_date:
            df = filter_comments_by_date(df, start_date, end_date)

        # 병합된 CSV 파일에 저장
        save_dataframe_to_csv(df, merged_csv_file, append=True)

        # JSON 파일 삭제
        os.remove(json_file)

    print(f"모든 URL의 댓글이 {merged_csv_file} 파일에 저장되었습니다.")

if __name__ == "__main__":
    # 유튜브 URL 목록
    urls = [
        'https://youtu.be/rBnPsx25XsM?si=XQ75mYnXPfzi-szU'  # 예시 URL
    ]

    # 댓글을 저장할 병합 CSV 파일 이름
    merged_csv_file = 'FilteredYoutubeComments.csv'

    # 필터링 기간 설정
    start_date = '2024-12-10'  # 시작 날짜
    end_date = '2024-12-11'    # 종료 날짜

    # 프로세스 실행
    process_youtube_comments(urls, merged_csv_file, start_date, end_date)
