import os
import markdown

def get_content_list(directory='content_scripts'):
    """获取内容脚本列表"""
    return [f for f in os.listdir(directory) if f.endswith('.md')]

def read_content(filename, directory='content_scripts'):
    """读取并转换markdown内容"""
    with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
        content = file.read()
    return markdown.markdown(content)