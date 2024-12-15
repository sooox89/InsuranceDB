import streamlit as st
import duckdb
from Home import home
from Analysis import analysis

st.set_page_config(
    page_title="Insurance Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)
# DuckDB 연결
conn = duckdb.connect('Insurance.duckdb', read_only=True)

# 사이드바를 사용한 네비게이션
st.sidebar.title("Navigation")

page = st.sidebar.radio("Go to", ["Home", "Analysis"])

# 선택된 페이지 렌더링
if page == "Home":
    home(conn)
elif page == "Analysis":
    analysis(conn)

