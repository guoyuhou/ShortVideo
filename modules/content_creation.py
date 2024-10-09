import streamlit as st

def show_todo_list():
    todos = [
        "完成'夏日美食'视频脚本",
        "联系@美食博主 进行合作",
        "准备下周直播内容"
    ]
    for todo in todos:
        st.checkbox(todo)

def render_page():
    st.header("内容创作")
    
    st.subheader("创意灵感生成器")
    topic = st.text_input("输入主题关键词")
    if st.button("生成创意"):
        # 这里应该调用AI接口生成创意
        st.write("基于主题 '{}' 的创意建议:".format(topic))
        st.write("1. 探索{}的历史演变".format(topic))
        st.write("2. {}在不同文化中的表现形式".format(topic))
        st.write("3. {}相关的有趣事实Top 10".format(topic))
    
    st.subheader("脚本编辑器")
    script = st.text_area("在这里编写您的视频脚本", height=300)
    if st.button("保存脚本"):
        st.success("脚本已保存!")