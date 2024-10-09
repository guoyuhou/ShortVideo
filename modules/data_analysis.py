import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data.raw.bilibili_data import data
def load_data():
    
    df = pd.DataFrame(data["视频列表"])
    df['日期'] = pd.to_datetime(df['日期'], format='%Y.%m.%d')
    df['点赞'] = df['点赞'].astype(int)
    df['评论'] = df['评论'].astype(int)
    df['转发'] = df['转发'].astype(int)
    df['播放量'] = df['播放量'].fillna(0).astype(int)
    df['弹幕'] = df['弹幕'].fillna(0).astype(int)
    return df, data

def get_overall_stats():
    _, overall_data = load_data()
    return overall_data['粉丝'], overall_data['视频'], overall_data['获赞数']

def get_recent_stats():
    df, _ = load_data()
    return df.sort_values('日期', ascending=False).head(7)[['日期', '点赞', '评论', '转发']]

def get_video_performance_trend():
    df, _ = load_data()
    return px.scatter(df, x='日期', y='点赞', size='播放量', color='评论',
                      hover_name='标题', size_max=60)

def get_interaction_rate_analysis():
    df, _ = load_data()
    df['互动率'] = (df['点赞'] + df['评论'] + df['转发']) / df['播放量']
    return px.bar(df.sort_values('互动率', ascending=False).head(10), 
                  x='标题', y='互动率', color='播放量')

def get_video_duration_vs_views():
    df, _ = load_data()
    df['时长(分钟)'] = df['时长'].apply(lambda x: int(x.split(':')[0]) + int(x.split(':')[1])/60)
    return px.scatter(df, x='时长(分钟)', y='播放量', size='点赞', color='评论',
                      hover_name='标题', trendline="ols")

def get_popular_topics():
    df, _ = load_data()
    topics = df['标题'].str.extract('「(.+?)」').dropna()
    topic_counts = topics[0].value_counts().head(10)
    return px.pie(values=topic_counts.values, names=topic_counts.index, title='热门话题分布')

def get_publish_time_analysis():
    df, _ = load_data()
    df['发布小时'] = df['日期'].dt.hour
    hour_performance = df.groupby('发布小时')['播放量'].mean().sort_values(ascending=False)
    return px.bar(x=hour_performance.index, y=hour_performance.values, labels={'x': '发布小时', 'y': '平均播放量'})