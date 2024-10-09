import streamlit as st
from modules import data_analysis, content_creation, video_editing, publish_management
from utils import data_processing, file_handling
from config import settings

st.set_page_config(page_title="ModernY短视频平台", layout="wide")

# 侧边栏
with st.sidebar:
    st.title("ModernY短视频")
    menu = st.selectbox("选择功能", ["主页", "数据分析", "内容创作", "视频编辑", "发布管理"])

# 主页面
st.title("ModernY短视频智能平台")

# 公共信息区域

if menu == "主页":
    st.header("欢迎来到ModernY短视频智能平台")
    st.write("这里是您的个人仪表板")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("最近的数据概览")
        data_analysis.show_recent_stats()
    with col2:
        st.subheader("待办事项")
        content_creation.show_todo_list()

elif menu == "数据分析":
    data_analysis.render_page()

elif menu == "内容创作":
    content_creation.render_page()

elif menu == "视频编辑":
    video_editing.render_page()

elif menu == "发布管理":
    publish_management.render_page()

# 页脚
st.markdown("---")
st.write("© 2023 ModernY短视频团队")