import requests
import base64
import json
import logging
import streamlit as st
import os

# GitHub API 设置
GITHUB_API_URL = "https://api.github.com"
GITHUB_TOKEN = st.secrets["github"]["GITHUB_TOKEN"]
GITHUB_REPO = st.secrets["github"]["GITHUB_REPO"]
CONTENT_DIR = 'content_scripts'

logging.basicConfig(level=logging.INFO)

def get_github_file(repo, path):
    url = f"{GITHUB_API_URL}/repos/{repo}/contents/{path}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"无法获取文件: {response.json().get('message')}")
        return None

def update_github_file(repo, path, content, message):
    url = f"{GITHUB_API_URL}/repos/{repo}/contents/{path}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}

    file_data = get_github_file(repo, path)
    if not file_data:
        st.error("无法获取文件信息，更新操作无法继续。")
        return False

    sha = file_data['sha']
    data = {
        "message": message,
        "content": base64.b64encode(content.encode()).decode(),
        "sha": sha
    }

    try:
        with st.spinner("正在更新文件..."):
            response = requests.put(url, headers=headers, json=data)
            response.raise_for_status()
            st.success("文件更新成功")
            logging.info("文件更新成功")
            return True
    except requests.exceptions.HTTPError as e:
        st.error(f"更新失败: {e.response.status_code} - {e.response.json().get('message', '未知错误')}")
        logging.error(f"更新错误: {e}")
        return False

def get_content_list():
    try:
        contents = get_github_file(GITHUB_REPO, CONTENT_DIR)
        if contents and isinstance(contents, list):
            return [item['name'] for item in contents if item['name'].endswith('.md')]
        else:
            st.error("无法获取内容列表")
            return []
    except Exception as e:
        st.error(f"获取内容列表时出错: {str(e)}")
        return []

def read_content(filename):
    file_path = f"{CONTENT_DIR}/{filename}"
    file_data = get_github_file(GITHUB_REPO, file_path)
    if file_data:
        content = base64.b64decode(file_data['content']).decode("utf-8")
        return content
    return None

def save_content(title, content):
    filename = f"{title}.md"
    file_path = f"{CONTENT_DIR}/{filename}"
    message = f"Add new content: {title}"
    return update_github_file(GITHUB_REPO, file_path, content, message)

def edit_markdown(file_path):
    file_data = get_github_file(GITHUB_REPO, file_path)
    if file_data:
        content = base64.b64decode(file_data['content']).decode("utf-8")
        return content
    return None