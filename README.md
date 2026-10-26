# 방송 전후 음식점 평점 및 반응 비교

방송에 소개된 음식점을 대상으로 YouTube 댓글의 감정과 Google Maps 리뷰 평점을 수집하여, 방송 전후 소비자 반응의 변화를 확인하는 프로젝트입니다.

## 프로젝트 목적

- YouTube에서 음식점 관련 영상 검색
- 영상 댓글 수집 및 기간별 필터링
- Google Cloud Natural Language API를 이용한 댓글 감정 분석
- Google Places API를 이용한 음식점 리뷰와 별점 수집
- 긍정·부정 댓글 비율 시각화
- 방송 시점을 기준으로 월별 평균 별점 변화 비교

## 분석 과정

```text
음식점 이름 입력
    ↓
YouTube Data API로 관련 영상 검색
    ↓
영상 댓글 수집 및 기간 필터링
    ↓
Google Natural Language API로 감정 분석
    ↓
긍정·부정 댓글 비율 시각화
    ↓
Google Places API로 음식점 리뷰 수집
    ↓
월별 평균 별점 계산 및 방송 시점 비교
```

## 주요 기능

### YouTube 영상 및 댓글 수집

`youtubelist.py`에서 YouTube Data API를 사용해 음식점 관련 영상을 검색합니다. `youtube_comment_scrapper.py`는 검색된 영상의 댓글을 수집하고, 지정한 기간에 해당하는 댓글만 CSV 파일로 저장합니다.

### 댓글 감정 분석

`Wordcutter.py`에서 Google Cloud Natural Language API를 호출하여 댓글별 감정 점수와 감정 강도를 계산합니다.

- `score > 0`: 긍정
- `score < 0`: 부정
- `magnitude`: 감정의 강도

분석 결과는 `SentimentAnalysisResults.csv`에 저장됩니다.

### 음식점 리뷰 및 별점 수집

`star_rating_collection.py`에서 Google Places API를 이용해 음식점의 Place ID, 리뷰, 작성 시점 및 별점을 가져옵니다.

### 결과 시각화

- `view_goodbad.py`: 긍정·부정 댓글 비율을 원형 그래프로 표시
- `view_result.py`: 월별 평균 별점과 방송 시점을 선 그래프로 표시
- 리뷰가 없는 월은 선형 보간법을 이용해 결측값 처리


## 실행 환경

- Python 3.10 이상 권장
- YouTube Data API v3
- Google Places API
- Google Cloud Natural Language API

## 설치 방법

```bash
git clone https://github.com/JUNE2001/Comparison-of-Restaurant-Ratings-Before-and-After-the-Broadcast.git
cd Comparison-of-Restaurant-Ratings-Before-and-After-the-Broadcast
pip install pandas numpy scipy matplotlib requests google-api-python-client youtube-comment-downloader
```

## API 설정

Google Cloud Console에서 다음 API를 활성화해야 합니다.

1. YouTube Data API v3
2. Places API
3. Cloud Natural Language API


```powershell
$env:GOOGLE_API_KEY="YOUR_API_KEY"
```

```python
import os

API_KEY = os.environ["GOOGLE_API_KEY"]
```

## 분석 대상 설정

`main.py`에서 분석할 음식점, 지역, 기간 및 방송 시점을 설정합니다.

```python
item = "쵸이닷"
PLACE_LOCATION = "서울"

start_date = "2023-06-01"
end_date = "2024-06-01"

# 그래프에 표시할 방송 시점
highlight_dates = ["2024-01", "2024-03", "2024-05"]

# 검색할 YouTube 영상 수와 출력할 리뷰 수
max_results = 1
max_reviews = 20
```

## 실행 방법

```bash
python main.py
```


## 결과 파일

### `MergedYoutubeComments.csv`

수집한 YouTube 댓글과 작성 시점 등의 원본 데이터를 저장합니다.

### `SentimentAnalysisResults.csv`

| 컬럼 | 설명 |
| --- | --- |
| `comment` | 분석한 댓글 |
| `score` | 감정 점수 |
| `magnitude` | 감정의 강도 |

## 분석 시 주의사항

- 검색된 YouTube 영상이 실제 방송 영상과 일치하는지 확인해야 합니다.
- 감정 분석은 반어법, 유행어 및 문맥을 정확하게 반영하지 못할 수 있습니다.
- Google Places API가 반환하는 리뷰 수는 제한적이므로 전체 이용자 평가를 대표하지 않을 수 있습니다.
- 선형 보간으로 생성된 값은 실제 관측값이 아닙니다.
- 방송 전후의 변화가 방송만으로 발생했다고 단정할 수 없으며 계절, 가격 및 메뉴 변경 등의 외부 요인을 고려해야 합니다.
