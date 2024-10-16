import streamlit as st
import ffmpeg
import os
import tempfile
import requests
import m3u8

def download_m3u8_content(m3u8_url):
    response = requests.get(m3u8_url)
    if response.status_code != 200:
        return None
    
    m3u8_obj = m3u8.loads(response.text)
    base_url = m3u8_url.rsplit('/', 1)[0] + '/'
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.m3u8', mode='w') as tmp_m3u8:
        for segment in m3u8_obj.segments:
            segment_url = base_url + segment.uri if not segment.uri.startswith('http') else segment.uri
            segment_response = requests.get(segment_url)
            if segment_response.status_code == 200:
                with tempfile.NamedTemporaryFile(delete=False, suffix='.ts', mode='wb') as tmp_ts:
                    tmp_ts.write(segment_response.content)
                tmp_m3u8.write(f"file '{tmp_ts.name}'\n")
    
    return tmp_m3u8.name

def convert_m3u8_to_mp4(m3u8_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
        output_file = tmp_file.name
    
    try:
        (
            ffmpeg
            .input(m3u8_file)
            .output(output_file, vcodec='libx264', acodec='aac')
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
        return output_file
    except ffmpeg.Error as e:
        st.error(f"FFmpeg 错误: {e.stderr.decode()}")
        return None

st.title("M3U8 转 MP4 工具箱")

m3u8_url = st.text_input("输入 M3U8 URL")

if m3u8_url:
    if st.button("转换为 MP4"):
        with st.spinner("正在下载并转换中..."):
            local_m3u8 = download_m3u8_content(m3u8_url)
            if local_m3u8:
                output_file = convert_m3u8_to_mp4(local_m3u8)
                if output_file:
                    st.success("转换成功!")
                    
                    with open(output_file, "rb") as file:
                        btn = st.download_button(
                            label="下载 MP4 文件",
                            data=file,
                            file_name="converted_video.mp4",
                            mime="video/mp4"
                        )
                    
                    os.remove(local_m3u8)
                    os.remove(output_file)
                else:
                    st.error("转换失败，请检查您的 M3U8 文件是否有效。")
            else:
                st.error("无法下载 M3U8 内容，请检查 URL 是否正确。")

st.write("注意: 此工具需要在服务器上安装 FFmpeg。")