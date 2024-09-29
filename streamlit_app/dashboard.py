# streamlit_app/dashboard.py

import os
import pandas as pd
import streamlit as st
import plotly.express as px
import logging
from datetime import datetime

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def show_dashboard():
    st.title("Overall Performance Dashboard")

    # 自动刷新设置
    st.sidebar.subheader("Auto Refresh")
    refresh_interval = st.sidebar.slider("Refresh Interval (seconds)", min_value=10, max_value=600, value=60)

    # JavaScript 代码用于定时刷新
    st.markdown(
        f"""
        <script>
        function refreshPage() {{
            setTimeout(function(){{
                window.location.reload();
            }}, {refresh_interval * 1000}); // 设置自动刷新时间（毫秒）
        }}
        refreshPage();
        </script>
        """,
        unsafe_allow_html=True
    )

    # 获取当前文件目录，并生成相对路径
    base_dir = os.path.dirname(os.path.abspath(__file__))
    performance_data_filename = os.path.join(base_dir, "../state/PerformanceData-BJ-Aug.csv")

    # 读取数据
    try:
        df = pd.read_csv(performance_data_filename)
        logging.info(f"成功读取数据文件: {performance_data_filename}")
    except FileNotFoundError:
        logging.error(f"文件未找到: {performance_data_filename}")
        st.error(f"File {performance_data_filename} not found.")
        return
    except Exception as e:
        logging.error(f"读取数据文件时发生错误: {e}")
        st.error(f"Error loading data file: {e}")
        return

    # 确保创建时间列是 datetime 类型
    df['创建时间(createTime)'] = pd.to_datetime(df['创建时间(createTime)'])
    
    # 日期选择器
    st.sidebar.header("Date Range Selector")
    start_date = st.sidebar.date_input("Start Date", df['创建时间(createTime)'].min().date())
    end_date = st.sidebar.date_input("End Date", df['创建时间(createTime)'].max().date())

    # 数据过滤
    filtered_df = df[(df['创建时间(createTime)'].dt.date >= start_date) &
                     (df['创建时间(createTime)'].dt.date <= end_date)]

    # 显示自动刷新的时间
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.sidebar.write(f"Last Refreshed: {current_time}")

    # 大指标块
    st.subheader("Key Metrics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Total Contracts", value=len(filtered_df))
    
    with col2:
        st.metric(label="Total Adjusted Refund Money", value=f"{filtered_df['合同金额(adjustRefundMoney)'].sum():,.2f}")
    
    with col3:
        st.metric(label="Average Adjusted Refund Money", value=f"{filtered_df['合同金额(adjustRefundMoney)'].mean():,.2f}")

    # 显示数据概览
    st.subheader("Data Overview")
    st.write(filtered_df.head())

    # 管家业绩统计
    st.subheader("Housekeeper Performance")
    housekeeper_stats = filtered_df.groupby('管家(serviceHousekeeper)').agg({
        '合同金额(adjustRefundMoney)': 'sum',
        '合同ID(_id)': 'count'
    }).rename(columns={'合同金额(adjustRefundMoney)': 'Total Amount', '合同ID(_id)': 'Number of Contracts'}).reset_index()
    
    st.write(housekeeper_stats)

    # 奖励类型分布
    st.subheader("Reward Type Distribution")
    reward_type_counts = filtered_df['奖励类型'].value_counts()
    fig_reward_type = px.bar(reward_type_counts, x=reward_type_counts.index, y=reward_type_counts.values, 
                            labels={'x': 'Reward Type', 'y': 'Count'}, title='Reward Type Distribution')
    st.plotly_chart(fig_reward_type)

    # 合同金额趋势
    st.subheader("Contract Amount Trend")
    df_resampled = filtered_df.resample('M', on='创建时间(createTime)').sum()['合同金额(adjustRefundMoney)']
    st.line_chart(df_resampled)

    # 其他数据展示
    st.subheader("Detailed Data")
    st.dataframe(filtered_df)

if __name__ == "__main__":
    show_dashboard()
