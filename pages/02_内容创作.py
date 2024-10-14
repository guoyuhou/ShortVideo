import streamlit as st
from modules import content_management

st.title("内容创作")

# 获取内容列表
content_list = content_management.get_content_list()

# 创建选择框
selected_content = st.selectbox("选择要编辑的内容", ["新建文档"] + content_list)

if selected_content == "新建文档":
    new_filename = st.text_input("输入新文档的文件名（不包含.md扩展名）")
    if new_filename:
        selected_content = f"{new_filename}.md"

if selected_content:
    # 读取选中的内容
    content = content_management.read_content(selected_content) if selected_content != "新建文档" else ""
    
    # 创建一个文本区域用于编辑内容
    edited_content = st.text_area("编辑内容（支持Markdown格式）", value=content, height=400)

    if st.button("保存内容"):
        if edited_content:
            if content_management.save_content(selected_content, edited_content):
                st.success(f"内容 '{selected_content}' 已成功保存！")
        else:
            st.warning("请输入内容。")
