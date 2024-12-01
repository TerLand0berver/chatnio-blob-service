from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from handlers.processor import process_file
from config import *
from handlers.ocr import create_ocr_task, deprecated_could_enable_ocr
from handlers.config_handler import router as config_router
from handlers.response_format import format_success_response, format_error_response
from config_manager import config_manager

async def read_file_size(file: UploadFile) -> float:
    """读取文件大小（以MB为单位）"""
    size = 0
    while chunk := await file.read(8192):
        size += len(chunk)
    await file.seek(0)  # 重置文件指针到开始
    return size / (1024 * 1024)  # 转换为MB

app = FastAPI()

# 初始化配置管理器
config_manager.initialize(app)

# 挂载静态文件
app.mount("/static", StaticFiles(directory="static"), name="static")

# 注册路由
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


@app.options("/upload")
async def options_upload():
    """处理上传接口的 OPTIONS 请求"""
    origins = config_manager._get_cors_origins()
    return JSONResponse(
        content="",
        headers={
            "Access-Control-Allow-Origin": origins[0] if origins and origins[0] != "*" else "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Credentials": "true" if origins and origins[0] != "*" else "false",
            "Access-Control-Max-Age": "600",
        }
    )
