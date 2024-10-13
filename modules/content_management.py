import os
import git
import streamlit as st
import requests
import base64
import logging

# GitHub API 设置
GITHUB_API_URL = "https://api.github.com"
GITHUB_TOKEN = st.secrets["token"]
GITHUB_REPO = st.secrets["repo_name"]
repo_path = 'content_scripts'
repo_url = st.secrets["repo_url"]

logging.basicConfig(level=logging.INFO)

def init_repo():
    if not os.path.exists(repo_path):
        repo = git.Repo.clone_from(repo_url, repo_path)
    else:
        repo = git.Repo(repo_path)
    return repo

def pull_latest_content():
    repo = init_repo()
    origin = repo.remotes.origin
    origin.pull()

def get_content_list():
    pull_latest_content()
    return [f for f in os.listdir(repo_path) if f.endswith('.md')]

def read_content(filename):
    with open(os.path.join(repo_path, filename), 'r', encoding='utf-8') as file:
        content = file.read()
    return content

def save_content(filename, content):
    file_path = os.path.join(repo_path, filename)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    
    update_github(filename, content)

def get_github_file(path):
    url = f"{GITHUB_API_URL}/repos/{GITHUB_REPO}/contents/{path}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"无法获取文件: {response.json().get('message')}")
        return None

def update_github(filename, content):
    path = os.path.join(repo_path, filename)
    url = f"{GITHUB_API_URL}/repos/{GITHUB_REPO}/contents/{path}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}

    file_data = get_github_file(path)
    if not file_data:
        st.error("无法获取文件信息，更新操作无法继续。")
        return False

    sha = file_data['sha']
    data = {
        "message": f"Update {filename}",
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

# 美化Streamlit页面的CSS代码
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
    
    body {
        font-family: 'Roboto', sans-serif;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        color: #333;
    }
    
    .stApp {
        background-color: transparent;
    }
    
    .main .block-container {
        padding: 2rem;
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .main .block-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15);
    }
    
    .stButton>button {
        background-color: #4a90e2;
        color: white;
        border-radius: 25px;
        padding: 0.6rem 1.2rem;
        font-weight: 500;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(74, 144, 226, 0.2);
    }
    
    .stButton>button:hover {
        background-color: #357ae8;
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(74, 144, 226, 0.3);
    }
    
    .stTextInput>div>div>input {
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #4a90e2;
        box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2);
    }
    
    .sidebar .sidebar-content {
        background-color: rgba(248, 249, 250, 0.9);
        border-radius: 10px;
        padding: 1rem;
    }
    
    .stSelectbox {
        border-radius: 8px;
        border: 2px solid #e0e0e0;
    }
    
    .stMarkdown a {
        color: #4a90e2;
        text-decoration: none;
        transition: all 0.2s ease;
    }
    
    .stMarkdown a:hover {
        color: #357ae8;
        text-decoration: underline;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    .main {
        animation: fadeIn 0.5s ease-in-out;
    }
    </style>
""", unsafe_allow_html=True)

# JavaScript代码
st.markdown("""
    <script>
    document.addEventListener('DOMContentLoaded', (event) => {
        const buttons = document.querySelectorAll('button');
        buttons.forEach(button => {
            button.addEventListener('click', function() {
                this.style.transform = 'scale(0.95)';
                setTimeout(() => {
                    this.style.transform = 'scale(1)';
                }, 200);
            });
        });
    
        const inputs = document.querySelectorAll('input[type="text"]');
        inputs.forEach(input => {
            input.addEventListener('focus', function() {
                this.style.transform = 'translateY(-2px)';
                this.style.boxShadow = '0 4px 8px rgba(0,0,0,0.1)';
            });
            input.addEventListener('blur', function() {
                this.style.transform = 'translateY(0)';
                this.style.boxShadow = 'none';
            });
        });
    
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, { threshold: 0.1 });
    
        document.querySelectorAll('.main > div > div').forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(20px)';
            el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            observer.observe(el);
        });
    });
    </script>
""", unsafe_allow_html=True)