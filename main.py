import streamlit as st
import duckdb
import urllib.request
import os

# Streamlit 설정
st.set_page_config(
    page_title="Insurance Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# DuckDB 파일 다운로드 함수
def download_duckdb_file():
    url = "https://drive.google.com/uc?id=1DEykM4iaDCjRD6fSuYZI8vIwA1j2e-qC"
    local_path = "Insurance.duckdb"

    # 파일이 이미 다운로드되어 있으면 스킵
    if not os.path.exists(local_path):
        try:
            st.info("DuckDB 파일을 다운로드 중입니다. 잠시만 기다려주세요...")
            urllib.request.urlretrieve(url, local_path)
            st.success("DuckDB 파일 다운로드 완료!")
        except Exception as e:
            st.error(f"DuckDB 파일 다운로드 실패: {e}")
            st.stop()
    return local_path

# DuckDB 연결
duckdb_path = download_duckdb_file()
conn = duckdb.connect(duckdb_path, read_only=True)

# Streamlit 앱 페이지 렌더링
from Home import home
from Analysis import analysis

# 사이드바 네비게이션
page = st.sidebar.radio("Go to", ["Home", "Analysis"])

# 선택된 페이지 렌더링
if page == "Home":
    home(conn)
elif page == "Analysis":
    analysis(conn)
