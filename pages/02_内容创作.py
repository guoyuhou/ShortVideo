import streamlit as st
from modules import content_management

st.title("内容创作")

# 获取内容列表
content_list = content_management.get_content_list()

# 创建选择框
selected_content = st.selectbox("选择要查看或编辑的内容", [""] + content_list)

if selected_content:
    # 读取选中的内容
    content = content_management.read_content(selected_content)
    
    # 展示 Markdown 内容
    st.markdown("## 当前文档内容")
    st.markdown(content)
    
    st.markdown("---")
    st.markdown("## 编辑文档")
    
    # 创建一个文本区域用于编辑内容
    edited_content = st.text_area("编辑内容（支持Markdown格式）", value=content, height=400)

    if st.button("保存修改"):
        if edited_content != content:
            if content_management.save_content(selected_content, edited_content):
                st.success(f"内容 '{selected_content}' 已成功更新！")
                st.experimental_rerun()  # 重新运行应用以显示更新后的内容
        else:
            st.info("内容未发生变化，无需保存。")

# 添加新文档的功能
st.markdown("---")
st.markdown("## 创建新文档")
new_filename = st.text_input("输入新文档的文件名（包含.md扩展名）")
new_content = st.text_area("输入新文档内容（支持Markdown格式）", height=200)

if st.button("创建新文档"):
    if new_filename and new_content:
        if new_filename.endswith('.md'):
            if content_management.save_content(new_filename, new_content):
                st.success(f"新文档 '{new_filename}' 已成功创建！")
                st.experimental_rerun()  # 重新运行应用以更新文档列表
        else:
            st.warning("文件名必须以 .md 结尾。")
    else:
        st.warning("请输入文件名和内容。")