import striprtf.striprtf
from typing import BinaryIO

def process_rtf(file: BinaryIO) -> str:
    """处理 RTF 文件，转换为纯文本"""
    content = file.read().decode('utf-8', errors='ignore')
    return striprtf.striprtf.rtf_to_text(content)
