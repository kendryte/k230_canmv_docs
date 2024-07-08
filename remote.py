import os
import glob
import re

def remove_content_between_markers(text, start_pattern, end_pattern):
    """
    移除从start_pattern开始到end_pattern（不包括end_pattern）之间所有内容。
    """
    # 使用正则表达式匹配并移除指定范围内的内容，不包括end_pattern
    pattern = re.escape(start_pattern) + '(.*?)(?=\n## ' + re.escape(end_pattern) + '|$)'
    return re.sub(pattern, '', text, flags=re.DOTALL)

def process_files(directory='.'):
    """
    遍历指定目录及其子目录下所有的Markdown文件，移除从'## 前言'到'## 1. 概述'（不包括该行）之间的所有内容。
    """
    markdown_files = glob.glob(os.path.join(directory, '**', '*.md'), recursive=True)
    
    for file_path in markdown_files:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # 应用函数移除指定内容
        cleaned_content = remove_content_between_markers(content, '## 前言', '1. 概述')
        
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(cleaned_content)

# 从当前目录开始遍历
process_files('.')