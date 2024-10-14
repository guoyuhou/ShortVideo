import requests
import base64
import streamlit as st

# GitHub API 设置
GITHUB_API_URL = "https://api.github.com"
GITHUB_TOKEN = st.secrets["github"]["GITHUB_TOKEN"]
GITHUB_REPO = st.secrets["github"]["GITHUB_REPO"]
CONTENT_DIR = 'content_scripts'

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
    if file_data:
        sha = file_data['sha']
    else:
        sha = None

    data = {
        "message": message,
        "content": base64.b64encode(content.encode()).decode(),
    }
    if sha:
        data["sha"] = sha

    try:
        with st.spinner("正在更新文件..."):
            response = requests.put(url, headers=headers, json=data)
            response.raise_for_status()
            st.success("文件更新成功")
            return True
    except requests.exceptions.HTTPError as e:
        st.error(f"更新失败: {e.response.status_code} - {e.response.json().get('message', '未知错误')}")
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

def save_content(filename, content):
    file_path = f"{CONTENT_DIR}/{filename}"
    message = f"Update content: {filename}"
    return update_github_file(GITHUB_REPO, file_path, content, message)

def edit_markdown(file_path):
    file_data = get_github_file(GITHUB_REPO, file_path)
    if file_data:
        content = base64.b64decode(file_data['content']).decode("utf-8")
        return content
    return None
