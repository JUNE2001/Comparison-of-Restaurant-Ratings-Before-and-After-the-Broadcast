#https://console.cloud.google.com/apis/credentials?project=authentic-wharf-443001-s6 #API키 발급 주소

from googleapiclient.discovery import build

def get_youtube_urls(api_key, search_query, max_results=20):
    # YouTube Data API 클라이언트 생성
    youtube = build("youtube", "v3", developerKey=api_key)
    
    # 검색 요청
    request = youtube.search().list(
        part="snippet",
        q=search_query,
        type="video",  # 동영상만 검색
        maxResults=max_results
    )
    response = request.execute()
    
    # 동영상 URL 추출
    video_urls = []
    for item in response.get("items", []):
        video_id = item["id"]["videoId"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        video_urls.append(video_url)
    
    return video_urls

# API 키 입력
api_key = "AIzaSyDcyPygjXsqK_FkkI9wE9xGXiffHtb5P_4"  # 여기에 발급받은 API 키를 입력하세요

# 검색어와 결과 개수 설정
search_term = input("검색어를 입력하세요: ")
max_results = 20

# 동영상 URL 가져오기
videos = get_youtube_urls(api_key, search_term, max_results)
print("\n=== 검색 결과 ===")
for url in videos:
    print(url)
