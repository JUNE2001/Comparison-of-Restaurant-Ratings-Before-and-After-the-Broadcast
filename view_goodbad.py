import matplotlib.pyplot as plt

# 원형 그래프를 그리는 함수
def plot_pie_chart(positive, negative):
    # 데이터
    labels = ['Positive', 'Negative']
    sizes = [positive, negative]
    colors = ['#4CAF50', '#FF5733']  # 긍정은 초록색, 부정은 빨간색

    # 원형 그래프 생성
    plt.figure(figsize=(6,6))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90, wedgeprops={'edgecolor': 'black'})

    # 그래프 제목
    plt.title('Sentiment Distribution')

    # 그래프 출력
    plt.axis('equal')  # 원형으로 보이도록
    plt.show()
    
# 실행
if __name__ == '__main__':
    # 긍정과 부정 값 입력
    positive = 60
    negative = 40

    # 원형 그래프 그리기
    plot_pie_chart(positive, negative)
