import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from data.raw.bilibili_data import data

# 加载数据
@st.cache_data
def load_data():
    df = pd.DataFrame(data["视频列表"])
    df['日期'] = pd.to_datetime(df['日期'], format='%Y.%m.%d')
    df['点赞'] = df['点赞'].astype(int)
    df['评论'] = df['评论'].astype(int)
    df['转发'] = df['转发'].astype(int)
    df['播放量'] = df['播放量'].fillna(0).astype(int)
    df['弹幕'] = df['弹幕'].fillna(0).astype(int)
    return df, data

def show_recent_stats():
    df, _ = load_data()
    recent_data = df.sort_values('日期', ascending=False).head(7)
    st.line_chart(recent_data.set_index('日期')[['点赞', '评论', '转发']])

def render_page():
    st.header("数据分析")
    
    df, overall_data = load_data()
    
    st.subheader("整体数据概览")
    col1, col2, col3 = st.columns(3)
    col1.metric("粉丝数", f"{overall_data['粉丝']:,}")
    col2.metric("视频数", overall_data['视频'])
    col3.metric("总获赞数", f"{overall_data['获赞数']:,}")
    
    st.subheader("视频表现趋势")
    fig = px.scatter(df, x='日期', y='点赞', size='播放量', color='评论',
                     hover_name='标题', size_max=60)
    st.plotly_chart(fig)
    
    st.subheader("互动率分析")
    df['互动率'] = (df['点赞'] + df['评论'] + df['转发']) / df['播放量']
    fig = px.bar(df.sort_values('互动率', ascending=False).head(10), 
                 x='标题', y='互动率', color='播放量')
    st.plotly_chart(fig)
    
    st.subheader("视频时长vs播放量")
    df['时长(分钟)'] = df['时长'].apply(lambda x: int(x.split(':')[0]) + int(x.split(':')[1])/60)
    fig = px.scatter(df, x='时长(分钟)', y='播放量', size='点赞', color='评论',
                     hover_name='标题', trendline="ols")
    st.plotly_chart(fig)
    
    st.subheader("热门话题分析")
    topics = df['标题'].str.extract('「(.+?)」').dropna()
    topic_counts = topics[0].value_counts().head(10)
    fig = px.pie(values=topic_counts.values, names=topic_counts.index, title='热门话题分布')
    st.plotly_chart(fig)
    
    st.subheader("发布时间分析")
    df['发布小时'] = df['日期'].dt.hour
    hour_performance = df.groupby('发布小时')['播放量'].mean().sort_values(ascending=False)
    fig = px.bar(x=hour_performance.index, y=hour_performance.values, labels={'x': '发布小时', 'y': '平均播放量'})
    st.plotly_chart(fig)
