import os
import json
import pandas as pd
import subprocess

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

def save_dataframe_to_csv(df, csv_file, append=False):
    """
    DataFrame을 CSV 파일로 저장합니다.
    """
    if append and os.path.exists(csv_file):
        df.to_csv(csv_file, mode='a', index=False, header=False, encoding='utf-8-sig')
    else:
        df.to_csv(csv_file, index=False, encoding='utf-8-sig')

def process_youtube_comments(urls, merged_csv_file):
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

        # 각 URL별 개별 CSV 저장 (원한다면 사용)
        # csv_file = f'YoutubeComments_{i}.csv'
        # save_dataframe_to_csv(df, csv_file)

        # 병합된 CSV 파일에 저장
        save_dataframe_to_csv(df, merged_csv_file, append=True)

        # JSON 파일 삭제
        os.remove(json_file)

    print(f"모든 URL의 댓글이 {merged_csv_file} 파일에 저장되었습니다.")

if __name__ == "__main__":
    # 유튜브 URL 목록
    urls = [
        'https://www.youtube.com/shorts/FLvMtj0NnNk'
    ]

    # 댓글을 저장할 병합 CSV 파일 이름
    merged_csv_file = 'MergedYoutubeComments.csv'

    # 프로세스 실행
    process_youtube_comments(urls, merged_csv_file)
