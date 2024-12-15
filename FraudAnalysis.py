import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import font_manager, rc
import io

# 한글 폰트 설정
font_path = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"  # 시스템에 설치된 한글 폰트 경로
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

def fraud_analysis(conn):
    st.subheader("4. Fraud Analysis")
    
    # 데이터 쿼리
    query = """
    SELECT 
        claim.CUST_ID AS 고객_ID,
        claim.HOSP_CODE AS 의료기관_코드,
        claim.POLY_NO AS 보험_계약_번호,
        COUNT(DISTINCT claim.CLAIM_ID) AS 방문_횟수,
        SUM(claim.DMND_AMT) AS 총_청구금액,
        MAX(cust.SIU_CUST_YN) AS 보험_사기_여부
    FROM claim
    JOIN cntt ON claim.POLY_NO = cntt.POLY_NO
    JOIN cust ON claim.CUST_ID = cust.CUST_ID
    GROUP BY claim.CUST_ID, claim.HOSP_CODE, claim.POLY_NO
    ORDER BY 방문_횟수 DESC;
    """
    df = conn.execute(query).fetchdf()
    
    # 보험 사기 데이터 필터링
    fraud_cases = df[df['보험_사기_여부'] == 'Y']
    
    # 데이터프레임 표시
    st.markdown("#### 보험 사기 관련 데이터")
    st.dataframe(fraud_cases)
    
    # 통계 요약
    total_fraud_cases = fraud_cases.shape[0]
    total_fraud_amount = fraud_cases['총_청구금액'].sum()
    st.markdown(f"""
    - 총 **{total_fraud_cases}건**의 보험 사기 사례가 발견되었습니다.
    - 보험 사기와 관련된 총 청구 금액은 **{total_fraud_amount:,.0f}원**입니다.
    """)

    # 시각화 1: 보험 사기 여부별 청구 금액 분포
    fraud_distribution = df.groupby('보험_사기_여부')['총_청구금액'].sum().reset_index()
    fig1, ax1 = plt.subplots(figsize=(6, 4), dpi=100)
    sns.barplot(data=fraud_distribution, x='보험_사기_여부', y='총_청구금액', palette='viridis', ax=ax1)
    ax1.set_title("보험 사기 여부에 따른 총 청구 금액 분포", fontsize=14)
    ax1.set_xlabel("보험 사기 여부", fontsize=12)
    ax1.set_ylabel("총 청구 금액 (원)", fontsize=12)
    plt.tight_layout()

    # 그래프를 이미지로 저장
    buf1 = io.BytesIO()
    fig1.savefig(buf1, format="png", bbox_inches="tight")
    buf1.seek(0)

    # Streamlit에 이미지로 표시
    st.image(buf1, caption="보험 사기 여부에 따른 총 청구 금액 분포", use_container_width=False)

    # 시각화 2: 사기 관련 방문 횟수 상위 10명
    top_visits = fraud_cases.sort_values('방문_횟수', ascending=False).head(10)
    fig2, ax2 = plt.subplots(figsize=(8, 5), dpi=100)
    sns.barplot(data=top_visits, x='고객_ID', y='방문_횟수', palette='magma', ax=ax2)
    ax2.set_title("사기 관련 방문 횟수 상위 10 고객", fontsize=14)
    ax2.set_xlabel("고객 ID", fontsize=12)
    ax2.set_ylabel("방문 횟수", fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # 그래프를 이미지로 저장
    buf2 = io.BytesIO()
    fig2.savefig(buf2, format="png", bbox_inches="tight")
    buf2.seek(0)

    # Streamlit에 이미지로 표시
    st.image(buf2, caption="사기 관련 방문 횟수 상위 10 고객", use_container_width=False)
