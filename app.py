import streamlit as st
from modules import data_analysis, content_creation, video_editing, publish_management
from utils import data_processing, file_handling
from config import settings
import os


st.set_page_config(page_title="ModernY短视频平台", layout="wide")

st.title("ModernY短视频智能平台")   


# 页脚
st.markdown("---")
st.write("© 2023 ModernY短视频团队")