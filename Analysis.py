import streamlit as st
from TopProducts import top_products
from CustomerAge import customer_age
from FraudAnalysis import fraud_analysis

def analysis(conn):
    st.title("Insurance Data Analysis")

    # 탭 생성
    tab1, tab2, tab3, tab4 = st.tabs([
        "1. Top 5 Products",
        "2. Customer Age Analysis",
        "3. Fraud Analysis1",
        "4. Fraud Analysis2"
    ])

    # Top 5 Products
    with tab1:
        top_products(conn)  # conn 전달

    # Customer Age Analysis
    with tab2:
        customer_age(conn)  # conn 전달

    # Fraud Analysis 2
    with tab3:
        fraud_analysis(conn)  # conn 전달
