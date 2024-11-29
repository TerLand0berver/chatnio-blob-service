from fastapi import UploadFile, File
from io import BytesIO
from typing import Tuple

from config import ENABLE_AZURE_SPEECH, MAX_FILE_SIZE
from handlers import (
    pdf,
    word,
    ppt,
    xlsx,
    image,
    speech,
)
from store.store import process_all
from .markdown_handler import process_markdown
from .csv_handler import process_csv
from .rtf_handler import process_rtf

async def read_file_size(file: UploadFile) -> float:
    """Read file size and return it in MiB."""

    # dont using file.read() directly because it will consume the file content
    file_size = 0
    while chunk := await file.read(20480):  # read chunk of 20KiB per iteration
        file_size += len(chunk)
    await file.seek(0)
    return file_size / 1024 / 1024


async def process_file(
        file: UploadFile = File(...),
        enable_ocr: bool = False,
        enable_vision: bool = True,
        save_all: bool = False,
) -> (str, str):
    """Process file and return its contents."""

    if MAX_FILE_SIZE > 0:
        file_size = await read_file_size(file)
        if file_size > MAX_FILE_SIZE:
            raise ValueError(f"File size {file_size:.2f} MiB exceeds the limit of {MAX_FILE_SIZE} MiB.")

    filename = file.filename.lower()

    if save_all:
        # save all types of files to storage
        return "file", await process_all(file)

    file_content = await file.read()
    file.file.seek(0)

    # 获取文件类型
    if filename.endswith(('.txt', '.log', '.ini', '.conf')):
        return 'text', file_content.decode('utf-8')
    elif filename.endswith('.md'):
        return 'markdown', process_markdown(BytesIO(file_content))
    elif filename.endswith('.csv'):
        return 'csv', process_csv(BytesIO(file_content))
    elif filename.endswith('.rtf'):
        return 'rtf', process_rtf(BytesIO(file_content))
    elif filename.endswith(('.doc', '.docx')):
        return "docx", word.process(file)
    elif filename.endswith('.pdf'):
        return "pdf", await pdf.process(
            file,
            enable_ocr=enable_ocr,
            enable_vision=enable_vision,
        )
    elif filename.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
        return "image", await image.process(
            file,
            enable_ocr=enable_ocr,
            enable_vision=enable_vision,
        )
    elif speech.is_audio(filename):
        if speech.ENABLE_AZURE_SPEECH:
            return "audio", speech.process(file)
        else:
            if save_all:
                return "file", await process_all(file)
            raise ValueError("Audio processing is disabled (Azure Speech SDK not installed)")
    elif filename.endswith(('.ppt', '.pptx')):
        return "pptx", ppt.process(file)
    elif filename.endswith(('.xls', '.xlsx')):
        return "xlsx", xlsx.process(file)
    else:
        raise ValueError("Unsupported file type")
