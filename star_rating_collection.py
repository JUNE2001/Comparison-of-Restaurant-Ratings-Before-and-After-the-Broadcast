import requests
from datetime import datetime

def get_place_id(api_key, place_name, place_location):
    """
    장소 이름과 위치로 Google Places API를 사용해 장소 ID를 가져옵니다.
    """
    search_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    search_params = {
        'input': f"{place_name} {place_location}",
        'inputtype': 'textquery',
        'fields': 'place_id',
        'key': api_key
    }
    response = requests.get(search_url, params=search_params)
    data = response.json()
    
    if data['status'] == 'OK' and data.get('candidates'):
        return data['candidates'][0]['place_id']
    else:
        raise ValueError(f"Error finding place ID. Status: {data['status']}, Candidates: {data.get('candidates')}")

def get_place_reviews(api_key, place_id):
    """
    장소 ID로 Google Places API를 사용해 장소 리뷰 및 별점을 가져옵니다.
    """
    details_url = "https://maps.googleapis.com/maps/api/place/details/json"
    details_params = {
        'place_id': place_id,
        'fields': 'name,rating,reviews',
        'language': 'ko',  # 한국어로 리뷰 요청
        'key': api_key
    }
    response = requests.get(details_url, params=details_params)
    data = response.json()
    
    if data['status'] == 'OK':
        return data['result']
    else:
        raise ValueError(f"Error fetching place details. Status: {data['status']}")

def print_reviews(place_name, reviews, max):
    """
    장소 리뷰 정보를 출력합니다.
    """
    print(f"Reviews for {place_name}:")
    if reviews:
        for review in reviews[:max]:  # 최대 20개 리뷰 출력
            review_time = datetime.fromtimestamp(review['time']).strftime('%Y-%m-%d %H:%M:%S')
            print(f"Rating: {review['rating']}")
            print(f"Review: {review['text']}")
            print(f"Date: {review_time}\n")
    else:
        print("No reviews found.")

# 메인 실행부
if __name__ == "__main__":
    API_KEY = ''  # 발급받은 API 키를 여기에 입력하세요.
    PLACE_NAME = '쵸이닷'
    PLACE_LOCATION = '서울'
    
    try:
        # 장소 ID 가져오기
        place_id = get_place_id(API_KEY, PLACE_NAME, PLACE_LOCATION)
        print(f"Place ID found: {place_id}")
        
        # 리뷰 및 별점 가져오기
        place_details = get_place_reviews(API_KEY, place_id)
        place_name = place_details['name']
        reviews = place_details.get('reviews', [])
        
        # 리뷰 출력
        print_reviews(place_name, reviews)
    except ValueError as e:
        print(e)
