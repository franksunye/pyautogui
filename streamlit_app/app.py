import streamlit as st
import sys
import os

# 获取当前文件的目录，并将其加入 sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, '..'))

from streamlit_app.dashboard import show_dashboard
st.set_page_config(page_title="Data Visualization Dashboard", layout="wide")

def main():
    st.title("Data Visualization with Streamlit!")
    # 可以在此定义页面导航或者功能模块切换
    show_dashboard()

if __name__ == "__main__":
    main()
