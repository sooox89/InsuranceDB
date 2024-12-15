import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import font_manager, rc
import io

# 한글 폰트 설정
font_path = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"  # 시스템에 설치된 한글 폰트 경로
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

def customer_age(conn):
    st.subheader("2. Customer Age Analysis")
    
    # SQL 쿼리 실행
    query = """
        SELECT 
            CASE 
                WHEN AGE BETWEEN 0 AND 5 THEN '영유아'
                WHEN AGE BETWEEN 6 AND 19 THEN '아동,청소년'
                WHEN AGE BETWEEN 20 AND 29 THEN '20대'
                WHEN AGE BETWEEN 30 AND 39 THEN '30대'
                WHEN AGE BETWEEN 40 AND 49 THEN '40대'
                WHEN AGE BETWEEN 50 AND 59 THEN '50대'
                WHEN AGE BETWEEN 60 AND 69 THEN '60대'
                WHEN AGE BETWEEN 70 AND 79 THEN '70대'
                ELSE '80대이상'
            END AS 연령대,
            AVG(DMND_AMT) AS 평균_청구_금액
        FROM claim
        JOIN cust ON claim.CUST_ID = cust.CUST_ID
        GROUP BY 연령대
        ORDER BY 연령대;
    """
    result = conn.execute(query).fetchdf()
    
    # 평균 청구 금액에 천 단위 콤마 추가
    result['평균_청구_금액'] = result['평균_청구_금액'].astype(int).apply(lambda x: f"{x:,}")

    # 시각화를 위해 정수로 변환된 컬럼 추가
    result['평균_청구_금액(int)'] = result['평균_청구_금액'].str.replace(",", "").astype(int)
    
    # Streamlit 데이터프레임 표시
    st.dataframe(result)

    # 시각화
    fig, ax = plt.subplots(figsize=(6, 5), dpi=100)  # dpi로 그래프 크기 고정
    sns.barplot(data=result, x='연령대', y='평균_청구_금액(int)', palette='viridis', ax=ax)
    
    # 그래프 제목 및 축 레이블 설정
    ax.set_title('연령대별 평균 청구 금액', fontsize=14)
    ax.set_xlabel('연령대', fontsize=12)
    ax.set_ylabel('평균 청구 금액 (원)', fontsize=12)
    plt.xticks(rotation=45, ha='right')

    # 막대 위에 금액 라벨 추가
    for index, row in result.iterrows():
        ax.text(index, row['평균_청구_금액(int)'], row['평균_청구_금액'], ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()

    # 그래프를 이미지로 저장
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)

    # Streamlit에 이미지로 표시
    st.image(buf, caption="연령대별 평균 청구 금액", use_container_width=False)
