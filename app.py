import streamlit as st
from modules import data_analysis, content_creation, video_editing, publish_management
from utils import data_processing, file_handling
from config import settings
import os

def read_markdown_file(markdown_file):
    with open(markdown_file, "r", encoding="utf-8") as file:
        return file.read()

st.set_page_config(page_title="ModernY短视频平台", layout="wide")

st.title("ModernY短视频智能平台")   

# 读取并显示 introduction.md 文件内容
introduction_path = os.path.join("content_scripts", "introduction.md")
introduction_content = read_markdown_file(introduction_path)
st.markdown(introduction_content, unsafe_allow_html=True)

# 页脚
st.markdown("---")
st.write("© 2023 ModernY短视频团队")
