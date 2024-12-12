import youtubelist as yl
import youtube_comment_scrapper as ycs
import Wordcutter as w
import goodbadCount as gbC
import view_goodbad as vgb
import star_rating_collection as src
import view_result as vr

api_key = 'AIzaSyDnp_wXSpGmaGcIujrFzbU0gqPSk-R22ZQ' ## api key 값
item = '가야가야' ## 식당명
PLACE_LOCATION = '서울' ## 식당 위치 지역

start_date = "2023-06-01"
end_date = "2024-06-01"
highlight_dates = ["2024-01", "2024-03", "2024-05"] ## 강조하고 싶은 날짜

max_results = 5 ## 유튜브 리스트 수
max_reviews = 20 ## 수집 리뷰
##videos = yl.get_youtube_urls(api_key, item, max_results)

## 키값 아낄 때 쓰는 용도
videos = ['https://www.youtube.com/watch?v=Q8O4fyMWYWw', 'https://www.youtube.com/watch?v=ny3mUuwHqO4']

merged_csv_file = 'MergedYoutubeComments.csv' ## 댓글 저장 csv명

ycs.process_youtube_comments(videos, merged_csv_file, start_date, end_date)


# output_csv_file = 'SentimentAnalysisResults.csv'
# w.analyze_sentiment_from_csv(merged_csv_file, 'text', output_csv_file)

# good, bad = gbC.good_bad_count('SentimentAnalysisResults.csv', 'score')
# vgb.plot_pie_chart(good, bad)

# place_id = src.get_place_id(api_key, item, PLACE_LOCATION)
# place_details = src.get_place_reviews(api_key, place_id)
# place_name = place_details['name']
# reviews = place_details.get('reviews', [])
# src.print_reviews(place_name, reviews, max_reviews)

# ratings = vr.preprocess_reviews_to_monthly_ratings(reviews)
# vr.plot_monthly_ratings_with_multiple_vertical_lines(start_date, end_date, ratings, highlight_dates)


