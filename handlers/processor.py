# from fastapi import UploadFile, File

# from config import ENABLE_AZURE_SPEECH, MAX_FILE_SIZE
# from handlers import (
#     pdf,
#     word,
#     ppt,
#     xlsx,
#     image,
#     speech,
# )


# async def read_file_size(file: UploadFile) -> float:
#     """Read file size and return it in MiB."""

#     # dont using file.read() directly because it will consume the file content
#     file_size = 0
#     while chunk := await file.read(20480):  # read chunk of 20KiB per iteration
#         file_size += len(chunk)
#     await file.seek(0)
#     return file_size / 1024 / 1024


# async def process_file(file: UploadFile = File(...), model: str = "") -> (str, str):
#     """Process file and return its contents."""

#     if MAX_FILE_SIZE > 0:
#         file_size = await read_file_size(file)
#         if file_size > MAX_FILE_SIZE:
#             raise ValueError(f"File size {file_size:.2f} MiB exceeds the limit of {MAX_FILE_SIZE} MiB.")

#     filename = file.filename.lower()
#     if pdf.is_pdf(filename):
#         return "pdf", await pdf.process(file, model)
#     elif word.is_docx(filename):
#         return "docx", word.process(file)
#     elif ppt.is_pptx(filename):
#         return "pptx", ppt.process(file)
#     elif xlsx.is_xlsx(filename):
#         return "xlsx", xlsx.process(file)
#     elif image.is_image(filename):
#         return "image", await image.process(file, model)
#     elif ENABLE_AZURE_SPEECH and speech.is_audio(filename):
#         return "audio", speech.process(file)

#     content = await file.read()
#     return "text", content.decode("utf-8")
from fastapi import FastAPI, UploadFile, File, HTTPException

# Assuming these constants are defined somewhere in your config file
MAX_FILE_SIZE = 15  # Maximum file size in MiB

app = FastAPI()

async def read_file_size(file: UploadFile) -> float:
    """Read file size and return it in MiB."""

    # Don't use file.read() directly because it will consume the file content
    file_size = 0
    while chunk := await file.read(20480):  # Read chunk of 20KiB per iteration
        file_size += len(chunk)
    await file.seek(0)
    return file_size / 1024 / 1024

@app.post("/uploadfile/")
async def process_file(file: UploadFile = File(...)) -> (str, bytes):
    """Upload file without processing it."""
    
    # Check the file size
    file_size = await read_file_size(file)
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail=f"File size {file_size:.2f} MiB exceeds the limit of {MAX_FILE_SIZE} MiB.")
    
    # Read and return file content
    return file.filename, await file.read()

