# ShortVideo
This repository was created to build a Streamlit APP for our ShortVideo

ModernY短视频平台/
│
├── app.py                 # 主应用入口
├── requirements.txt       # 项目依赖
├── .gitignore             # Git忽略文件
│
├── pages/                 # 多页面应用的其他页面
│   ├── 01_数据分析.py
│   ├── 02_内容创作.py
│   ├── 03_视频编辑.py
│   └── 04_发布管理.py
│
├── modules/               # 功能模块
│   ├── __init__.py
│   ├── data_analysis.py
│   ├── content_creation.py
│   ├── video_editing.py
│   └── publish_management.py
│
├── utils/                 # 工具函数
│   ├── __init__.py
│   ├── data_processing.py
│   └── file_handling.py
│
├── config/                # 配置文件
│   └── settings.py
│
├── data/                  # 数据文件夹
│   ├── raw/
│   └── processed/
│
├── assets/                # 静态资源
│   ├── images/
│   ├── css/
│   └── js/
│
└── tests/                 # 测试文件夹
    ├── __init__.py
    └── test_modules.py