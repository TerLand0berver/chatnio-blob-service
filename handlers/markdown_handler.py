import markdown
from typing import BinaryIO

def process_markdown(file: BinaryIO) -> str:
    """处理 Markdown 文件，转换为纯文本"""
    content = file.read().decode('utf-8')
    # 转换为HTML然后去除HTML标签
    html = markdown.markdown(content)
    # 简单的HTML标签清理
    text = ''
    in_tag = False
    for char in html:
        if char == '<':
            in_tag = True
        elif char == '>':
            in_tag = False
        elif not in_tag:
            text += char
    return text.strip()
