import streamlit as st
import pandas as pd
import plotly.express as px

def show_recent_stats():
    # 这里应该从数据库或API获取实际数据
    data = pd.DataFrame({
        '日期': pd.date_range(start='2023-01-01', periods=7),
        '播放量': [1000, 1200, 1100, 1300, 1500, 1400, 1600],
        '点赞数': [100, 120, 110, 130, 150, 140, 160]
    })
    st.line_chart(data.set_index('日期'))

def render_page():
    st.header("数据分析")
    
    # 假设的数据
    video_data = pd.DataFrame({
        '视频标题': ['视频1', '视频2', '视频3', '视频4', '视频5'],
        '播放量': [10000, 15000, 8000, 12000, 20000],
        '点赞数': [1000, 1500, 800, 1200, 2000],
        '评论数': [100, 150, 80, 120, 200]
    })
    
    st.subheader("视频表现概览")
    st.dataframe(video_data)
    
    st.subheader("播放量vs点赞数")
    fig = px.scatter(video_data, x='播放量', y='点赞数', size='评论数', hover_name='视频标题')
    st.plotly_chart(fig)