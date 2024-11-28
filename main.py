from fastapi import FastAPI, File, UploadFile, Form
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from handlers.processor import process_file
from config import *
from handlers.ocr import create_ocr_task, deprecated_could_enable_ocr
from handlers.config_handler import router as config_router
from handlers.response_format import format_success_response, format_error_response

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOW_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(config_router)

@app.get("/")
def root():
    return FileResponse("index.html", media_type="text/html")


@app.get("/favicon.ico")
def favicon():
    return FileResponse("favicon.ico")


@app.post("/upload")
async def upload_file(
        file: UploadFile = File(...),
        enable_ocr: bool = Form(default=False),
        enable_vision: bool = Form(default=True),
        save_all: bool = Form(default=False),
        model: str = Form(default=""),  # deprecated
):
    """Accepts file and returns its contents."""

    if model and len(model) > 0:
        # compatibility with deprecated model parameter
        enable_ocr = deprecated_could_enable_ocr(model)
        enable_vision = not enable_ocr

    if len(OCR_ENDPOINT) == 0:
        enable_ocr = False

    try:
        # 检查文件大小
        if MAX_FILE_SIZE > 0:
            size = await read_file_size(file)
            if size > MAX_FILE_SIZE:
                return format_error_response(f"File size {size:.2f}MiB exceeds limit {MAX_FILE_SIZE}MiB")

        file_type, content = await process_file(file, enable_ocr, enable_vision, save_all)
        return format_success_response(file_type, content)
    except Exception as e:
        return format_error_response(str(e))
