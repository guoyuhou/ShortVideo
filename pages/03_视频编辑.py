import streamlit as st
import ffmpeg
import os
import tempfile

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

uploaded_file = st.file_uploader("上传 M3U8 文件", type=['m3u8'])

if uploaded_file is not None:
    # 保存上传的文件
    with tempfile.NamedTemporaryFile(delete=False, suffix='.m3u8') as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        m3u8_path = tmp_file.name

    if st.button("转换为 MP4"):
        with st.spinner("正在转换中..."):
            output_file = convert_m3u8_to_mp4(m3u8_path)
        
        if output_file:
            st.success("转换成功!")
            
            # 提供下载按钮
            with open(output_file, "rb") as file:
                btn = st.download_button(
                    label="下载 MP4 文件",
                    data=file,
                    file_name="converted_video.mp4",
                    mime="video/mp4"
                )
            
            # 清理临时文件
            os.remove(m3u8_path)
            os.remove(output_file)
        else:
            st.error("转换失败，请检查您的 M3U8 文件是否有效。")

st.write("注意: 此工具需要在服务器上安装 FFmpeg。")