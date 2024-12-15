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

def top_products(conn):
    # 페이지 제목
    st.subheader("1. Top 5 Products by Sales")
    
    # 데이터베이스 쿼리
    query = """
        SELECT 
            GOOD_CLSF_CDNM,
            COUNT(*) AS 계약_건수
        FROM cntt
        GROUP BY GOOD_CLSF_CDNM
        ORDER BY 계약_건수 DESC
        LIMIT 5;
    """
    data = conn.execute(query).fetchdf()
    
    # 데이터프레임 표시
    st.dataframe(data)
    
    # 시각화
    fig, ax = plt.subplots(figsize=(6, 3), dpi=100)  # dpi로 그래프 크기 고정
    sns.barplot(data=data, x="GOOD_CLSF_CDNM", y="계약_건수", ax=ax)

    # 제목 및 축 레이블 설정
    ax.set_title("Top 5 Products by Sales", fontsize=14)
    ax.set_xlabel("Product Classification", fontsize=10)
    ax.set_ylabel("Number of Contracts", fontsize=10)

    # x축 레이블 회전 및 크기 설정
    plt.xticks(rotation=45, fontsize=9)
    plt.yticks(fontsize=9)

    # 여백 최소화
    plt.tight_layout()
    
    # 그래프를 이미지로 저장
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)

    # Streamlit에 그래프 표시 (bbox_inches로 크기 고정)
    st.image(buf, caption="Top 5 Products by Sales", use_container_width=False)

    
    # 페이지 하단 설명 추가
    st.markdown("""
        ---
        ### 설명
        - 총 18개의 상품 분류 중에서 가장 많이 판매된 상품 분류를 조회한 결과입니다.
        - 전체 계약 건수는 **101,349개**이며, 상위 5개 상품의 계약 건수가 전체의 **69.61** %를 차지합니다.
        - **GOOD_CLSF_CDNM (상품분류)**: 해당 상품이 어떠한 분류에 속하는지를 설명하며, 총 18가지로 구성되어 있습니다 (중복 없음).
    """, unsafe_allow_html=True)
