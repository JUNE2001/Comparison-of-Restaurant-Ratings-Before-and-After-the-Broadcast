import requests
from datetime import datetime

# API 키 및 식당 정보 설정
API_KEY = ''  # 발급받은 API 키를 여기에 입력하세요.
PLACE_NAME = '모수'
PLACE_LOCATION = '서울'

# 장소 검색 URL
search_url = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
search_params = {
    'input': f"{PLACE_NAME} {PLACE_LOCATION}",
    'inputtype': 'textquery',
    'fields': 'place_id',
    'key': API_KEY
}

# 장소 ID 가져오기
response = requests.get(search_url, params=search_params)
place_data = response.json()

if place_data['status'] == 'OK' and place_data.get('candidates'):
    place_id = place_data['candidates'][0]['place_id']
    print(f"Place ID found: {place_id}")
    
    # 리뷰 및 별점 가져오기
    details_url = f"https://maps.googleapis.com/maps/api/place/details/json"
    details_params = {
        'place_id': place_id,
        'fields': 'name,rating,reviews',
        'language': 'ko',  # 한국어로 리뷰 요청
        'key': API_KEY
    }
    
    details_response = requests.get(details_url, params=details_params)
    details_data = details_response.json()
    
    if details_data['status'] == 'OK':
        print(f"Reviews for {details_data['result']['name']}:")
        reviews = details_data['result'].get('reviews', [])
        
        # 최대 20개 리뷰 출력
        if reviews:
            for review in reviews[:20]:
                review_time = datetime.fromtimestamp(review['time']).strftime('%Y-%m-%d %H:%M:%S')
                print(f"Rating: {review['rating']}")
                print(f"Review: {review['text']}")
                print(f"Date: {review_time}\n")  # 리뷰 작성 날짜 출력
        else:
            print("No reviews found.")
    else:
        print("Error fetching place details.")
else:
    print(f"Error finding place ID. Status: {place_data['status']}, Candidates: {place_data.get('candidates')}")
