import csv
import io
from typing import BinaryIO

def process_csv(file: BinaryIO) -> str:
    """处理 CSV 文件，转换为文本格式"""
    content = file.read().decode('utf-8')
    csv_file = io.StringIO(content)
    reader = csv.reader(csv_file)
    
    # 将CSV转换为格式化文本
    text_content = []
    for row in reader:
        text_content.append(" | ".join(row))
    
    return "\n".join(text_content)
