import streamlit as st

def home(conn):
    st.title("양수경의 보험 DB 분석 페이지 입니다!")
    
    # Table Viewer
    st.subheader("Table Viewer")
    selected_table = st.selectbox("원하는 테이블을 선택하세요.", ["cust", "cntt", "claim"])
    query = f"SELECT * FROM {selected_table} LIMIT 100"
    data = conn.execute(query).fetchdf()
    st.dataframe(data)
    
    # Displaying the image
    st.image("/home/casey/Pictures/casey_fraud.png", caption="보험 DB ERD", use_container_width=False)


