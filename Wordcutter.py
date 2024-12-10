import requests
import json
import csv
import os
import pandas as pd

# 전역 변수로 API 키 설정
API_KEY = "AIzaSyDnp_wXSpGmaGcIujrFzbU0gqPSk-R22ZQ"

def analyze_sentiment(text_content: str, language_code: str = "en") -> dict:
    """
    Google Cloud Natural Language API를 호출하여 감정 분석을 수행합니다.

    매개변수:
        text_content: 분석할 텍스트.
        language_code: 텍스트의 언어 (기본값은 "en").

    반환값:
        API 응답 데이터 (JSON 형식).
    """
    url = f"https://language.googleapis.com/v1/documents:analyzeSentiment?key={API_KEY}"

    document = {
        "document": {
            "type": "PLAIN_TEXT",
            "content": text_content,
            "language": language_code,
        },
        "encodingType": "UTF8",
    }

    response = requests.post(url, headers={"Content-Type": "application/json"}, data=json.dumps(document))
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API 에러: {response.status_code}, {response.text}")

def extract_word_level_sentiment_from_comments(comments: list) -> list:
    """
    여러 댓글을 처리하여 각 단어의 감정 점수와 강도를 추출합니다.

    매개변수:
        comments: 분석할 댓글 리스트.

    반환값:
        단어별 감정 분석 결과 리스트.
    """
    all_word_sentiment_data = []

    for comment in comments:
        words = comment.split()
        for word in words:
            try:
                result = analyze_sentiment(word)
                document_sentiment = result.get("documentSentiment", {})
                all_word_sentiment_data.append({
                    "comment": comment,
                    "word": word,
                    "score": document_sentiment.get("score", 0),
                    "magnitude": document_sentiment.get("magnitude", 0),
                })
            except Exception as e:
                print(f"단어 '{word}' 분석 중 에러 발생 (댓글: '{comment}') - {e}")
                all_word_sentiment_data.append({
                    "comment": comment,
                    "word": word,
                    "score": "Error",
                    "magnitude": "Error",
                })

    return all_word_sentiment_data

def save_sentiment_to_csv(word_sentiment_data: list, output_file: str) -> None:
    """
    단어별 감정 분석 결과를 CSV 파일로 저장합니다.

    매개변수:
        word_sentiment_data: 단어별 감정 분석 결과 리스트.
        output_file: 저장할 CSV 파일 경로.
    """
    with open(output_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["comment", "word", "score", "magnitude"])
        writer.writeheader()
        writer.writerows(word_sentiment_data)

def analyze_sentiment_from_csv(input_csv_file, text_column, output_csv_file):
    """
    CSV 파일에서 특정 열의 텍스트 데이터를 추출하여 감정 분석을 수행하고 결과를 저장합니다.

    매개변수:
        input_csv_file: 입력 CSV 파일 경로.
        text_column: 텍스트가 포함된 열 이름.
        output_csv_file: 감정 분석 결과를 저장할 CSV 파일 경로.
    """
    # 1. 입력 CSV 파일 읽기
    if not os.path.exists(input_csv_file):
        print(f"입력 CSV 파일 '{input_csv_file}'이(가) 존재하지 않습니다.")
        return

    try:
        df = pd.read_csv(input_csv_file, encoding="utf-8-sig")
    except Exception as e:
        print(f"CSV 파일 읽기 중 오류 발생: {e}")
        return

    # 2. 지정된 열에서 텍스트 데이터 추출
    if text_column not in df.columns:
        print(f"지정된 열 '{text_column}'이(가) CSV 파일에 존재하지 않습니다.")
        return

    comments = df[text_column].dropna().tolist()

    # 3. 감정 분석 수행
    word_sentiment_results = extract_word_level_sentiment_from_comments(comments)

    # 4. 감정 분석 결과 저장
    save_sentiment_to_csv(word_sentiment_results, output_csv_file)
    print(f"감정 분석 결과가 '{output_csv_file}' 파일에 저장되었습니다.")


# 사용 예시
if __name__ == "__main__":
    comments = [
        "이 제품 정말 마음에 들어요! 제 삶을 더 편하게 해줍니다.",
        "서비스가 정말 최악이었어요. 너무 실망했습니다.",
        "이건 제가 경험한 것 중 최고입니다!",
        "가끔은 작동하지만, 다른 때는 완전히 실패해요."
    ]
    print("댓글 감정 분석을 시작합니다...")
    word_sentiment_results = extract_word_level_sentiment_from_comments(comments)
    save_sentiment_to_csv(word_sentiment_results, "multiple_comments_sentiment_analysis.csv")
    print("단어별 감정 분석 결과가 'multiple_comments_sentiment_analysis.csv' 파일에 저장되었습니다.")
