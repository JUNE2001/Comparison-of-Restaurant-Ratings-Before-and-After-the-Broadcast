import pandas as pd

def good_bad_count(file_path):
    # CSV 파일 읽기
    df = pd.read_csv(file_path)

    # 'value' 값에 따라 카운트하기
    good_count = len(df[df['value'] > 0])  # value가 양수인 경우
    bad_count = len(df[df['value'] < 0])   # value가 음수인 경우

    return good_count, bad_count

# 사용 예시
if __name__ == "__main__":
    good, bad = good_bad_count('감정.csv')
    print(f"Good count: {good}")
    print(f"Bad count: {bad}")
