import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import interp1d
import numpy as np

def fill_missing_ratings_linear(ratings, month_labels):
    """
    ratings 딕셔너리에서 결측치를 직선 보간법으로 채웁니다.
    비어있는 달은 이전 달과 이후 달을 직선적으로 연결하여 채웁니다.
    
    Parameters:
        ratings (dict): 날짜별 별점 데이터 (예: {"2023-06": 4.1, "2023-07": 3.9, ...}).
        month_labels (list of str): "YYYY-MM" 형식의 월 리스트.
    
    Returns:
        dict: 결측치가 직선 보간법으로 채워진 ratings 딕셔너리.
    """
    # 날짜를 datetime 형식으로 변환
    months = pd.to_datetime(month_labels, format="%Y-%m")
    ratings_values = [ratings.get(month.strftime("%Y-%m"), None) for month in months]

    # 비어있는 값들에 대해 직선 보간법을 사용하여 채우기
    not_none_indices = [i for i, val in enumerate(ratings_values) if val is not None]
    not_none_values = [ratings_values[i] for i in not_none_indices]

    # datetime을 숫자로 변환 (timestamp)하여 보간을 수행
    not_none_months = [months[i].timestamp() for i in not_none_indices]
    
    # 직선 보간법을 사용하여 결측치 보간
    f = interp1d(not_none_months, not_none_values, kind='linear', fill_value="extrapolate")
    
    # 보간된 값들 채우기
    interpolated_ratings = {}
    for i, month in enumerate(month_labels):
        if ratings_values[i] is None:
            interpolated_ratings[month] = f(months[i].timestamp())  # 보간된 값
        else:
            interpolated_ratings[month] = ratings_values[i]  # 기존 값
    
    return interpolated_ratings

def plot_monthly_ratings_with_multiple_vertical_lines(start_date, end_date, ratings, highlight_dates, title="Monthly Average Ratings"):
    """
    특정 기간의 달별 별점 평균 그래프를 표시하고, 여러 개의 세로선을 추가합니다.
    
    Parameters:
        start_date (str): 시작 날짜 (예: "2023-06-01").
        end_date (str): 종료 날짜 (예: "2024-06-01").
        ratings (dict): 날짜별 별점 데이터 (예: {"2023-06": 4.1, "2023-07": 3.9, ...}).
        highlight_dates (list of str): 세로선을 표시할 날짜들의 리스트 (예: ["2024-01", "2024-03"]).
        title (str): 그래프 제목.
    """
    # 기간 생성
    date_range = pd.date_range(start=start_date, end=end_date, freq='MS')  # 매월 시작일 기준
    month_labels = [date.strftime("%Y-%m") for date in date_range]  # "YYYY-MM" 형식으로 라벨 생성
    
    # 결측치를 채운 ratings 딕셔너리로부터 값 추출
    filled_ratings = fill_missing_ratings_linear(ratings, month_labels)
    ratings_values = [filled_ratings.get(month, 0) for month in month_labels]  # 해당 월에 별점이 없으면 0으로 설정

    # 길이가 맞지 않으면 에러가 발생하므로 ratings의 길이를 month_labels와 맞춰야 함
    if len(ratings_values) != len(month_labels):
        raise ValueError(f"Ratings length {len(ratings_values)} does not match the number of months {len(month_labels)}")

    # 각 highlight_date에 대해 인덱스를 찾고 세로선 추가
    plt.figure(figsize=(14, 6))  # 그래프 크기 설정
    plt.plot(month_labels, ratings_values, marker='o', linestyle='-', color='purple', label='Average Rating')  # 선형 그래프 생성
    
    # 비어있는 달에 대한 표시
    for i, month in enumerate(month_labels):
        if ratings.get(month) is None:
            plt.scatter(month, 0, color='red', zorder=5)  # 비어있는 달에 빨간색 점 추가
            plt.text(month, 0.1, "Missing", ha='center', fontsize=10, color='red')  # "Missing" 텍스트 추가

    # highlight_dates에 대해서 세로선 표시
    for highlight_date in highlight_dates:
        if highlight_date in month_labels:
            highlight_index = month_labels.index(highlight_date)  # 해당 날짜의 인덱스 찾기
            plt.axvline(x=highlight_index, color='r', linestyle='--', label=f"Highlight: {highlight_date}")  # 세로선 추가
    
    # 제목과 레이블 설정
    plt.title(title, fontsize=16)
    plt.xlabel("Month", fontsize=12)
    plt.ylabel("Average Rating", fontsize=12)
    plt.ylim(0, 5)  # 별점 범위 설정 (0~5)
    plt.grid(True, linestyle='--', alpha=0.6)  # 격자 표시
    
    # x축 라벨 회전
    plt.xticks(rotation=45, fontsize=10)
    plt.yticks(fontsize=10)  # y축 글꼴 크기 설정
    
    # 범례 추가
    plt.legend(fontsize=12)
    plt.tight_layout()  # 레이아웃 정리
    plt.show()  # 그래프 표시


if __name__ == "__main__":
    # 데이터 준비
    start_date = "2023-06-01"
    end_date = "2024-06-01"
    
    # ratings를 딕셔너리로 변경 (날짜: 별점)
    ratings = {
        "2023-06": 4.1, "2023-07": 3.9, "2023-08": 4.2, "2023-09": 4.0,
        # "2023-10": None, "2023-11": None, "2023-12": None,  # 2023-10, 2023-11, 2023-12 비어있음
        "2024-01": 3.8, "2024-02": 4.6, "2024-03": 4.7, "2024-04": 4.1,
        "2024-05": 4.3, "2024-06": 4.5
    }
    
    highlight_dates = ["2024-01", "2024-03", "2024-05"]  # 세로선을 표시할 날짜들

    # 함수 호출
    plot_monthly_ratings_with_multiple_vertical_lines(start_date, end_date, ratings, highlight_dates)
