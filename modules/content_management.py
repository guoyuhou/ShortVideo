import os
import markdown
import git
import streamlit as st

repo_path = 'content_scripts'
repo_url = st.secrets["github"]["repo_url"]
github_token = st.secrets["github"]["token"]
github_repo_name = st.secrets["github"]["repo_name"]

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
    return markdown.markdown(content)

def save_content(filename, content):
    repo = init_repo()
    file_path = os.path.join(repo_path, filename)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    
    repo.git.add(file_path)
    repo.git.commit('-m', f'Update {filename}')
    origin = repo.remotes.origin
    origin.push()

def update_github(filename):
    # 不适用GitHub包。请你修改
    pass