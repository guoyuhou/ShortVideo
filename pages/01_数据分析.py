import streamlit as st
from modules import data_analysis

st.set_page_config(page_title="数据分析 - ModernY短视频平台", layout="wide")

st.title("数据分析")

# 整体数据概览
st.subheader("整体数据概览")
fans, videos, likes = data_analysis.get_overall_stats()
col1, col2, col3 = st.columns(3)
col1.metric("粉丝数", f"{fans:,}")
col2.metric("视频数", videos)
col3.metric("总获赞数", f"{likes:,}")

# 最近数据概览
st.subheader("最近数据概览")
recent_data = data_analysis.get_recent_stats()
st.line_chart(recent_data.set_index('日期'))

# 视频表现趋势
st.subheader("视频表现趋势")
fig = data_analysis.get_video_performance_trend()
st.plotly_chart(fig)

# 互动率分析
st.subheader("互动率分析")
fig = data_analysis.get_interaction_rate_analysis()
st.plotly_chart(fig)

# 视频时长vs播放量
st.subheader("视频时长vs播放量")
fig = data_analysis.get_video_duration_vs_views()
st.plotly_chart(fig)

# 热门话题分析
st.subheader("热门话题分析")
fig = data_analysis.get_popular_topics()
st.plotly_chart(fig)

# 发布时间分析
st.subheader("发布时间分析")
fig = data_analysis.get_publish_time_analysis()
st.plotly_chart(fig)