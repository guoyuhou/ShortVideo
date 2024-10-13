import streamlit as st
from modules import content_management
import os

st.title("内容创作")

# 获取内容列表
content_list = content_management.get_content_list()

# 创建选择框
selected_content = st.selectbox("选择要查看的内容", content_list)

if selected_content:
    # 读取并显示选中的内容
    content = content_management.read_content(selected_content)
    st.markdown(content, unsafe_allow_html=True)

# 添加新内容的功能
st.subheader("添加新内容")
new_title = st.text_input("输入新内容的标题")
new_content = st.text_area("输入新内容（支持Markdown格式）", height=300)

if st.button("保存新内容"):
    if new_title and new_content:
        filename = f"{new_title}.md"
        with open(os.path.join('content_scripts', filename), 'w', encoding='utf-8') as file:
            file.write(new_content)
        st.success(f"内容 '{new_title}' 已成功保存！")
    else:
        st.warning("请输入标题和内容。")