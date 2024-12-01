import json
import os
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from config_manager import config_manager

router = APIRouter()
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates"))

CONFIG_FILE = "config.json"

def load_config() -> Dict[str, Any]:
    """加载配置文件"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_config(config: Dict[str, Any]) -> None:
    """保存配置到文件"""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def update_environment_variables(config: Dict[str, Any]) -> None:
    """更新环境变量"""
    # API响应格式配置
    api_format = {
        'status_field': config.get('status_field', 'status'),
        'type_field': config.get('type_field', 'type'),
        'content_field': config.get('content_field', 'content'),
        'error_field': config.get('error_field', 'error'),
        'success_value': config.get('success_value', True),
        'error_value': config.get('error_value', False),
        'include_type': config.get('include_type', True),
        'wrap_content': config.get('wrap_content', False),
        'content_wrapper': config.get('content_wrapper')
    }
    
    if api_format['content_wrapper']:
        try:
            # 确保content_wrapper是有效的JSON
            if isinstance(api_format['content_wrapper'], str):
                api_format['content_wrapper'] = json.loads(api_format['content_wrapper'])
        except json.JSONDecodeError:
            api_format['content_wrapper'] = None
            api_format['wrap_content'] = False
    
    os.environ['API_RESPONSE_FORMAT'] = json.dumps(api_format)

    # 基础配置
    if 'pdf_max_images' in config:
        os.environ['PDF_MAX_IMAGES'] = str(config['pdf_max_images'])
    if 'max_file_size' in config:
        os.environ['MAX_FILE_SIZE'] = str(config['max_file_size'])
    if 'cors_allow_origins' in config:
        os.environ['CORS_ALLOW_ORIGINS'] = str(config['cors_allow_origins'])

    # 存储配置
    if 'storage_type' in config:
        os.environ['STORAGE_TYPE'] = config['storage_type']
        
        if config['storage_type'] == 'local':
            if 'local_storage_domain' in config:
                os.environ['LOCAL_STORAGE_DOMAIN'] = config['local_storage_domain']
        
        elif config['storage_type'] == 's3':
            s3_vars = ['s3_access_key', 's3_secret_key', 's3_bucket', 's3_region', 's3_domain']
            for var in s3_vars:
                if var in config:
                    os.environ[var.upper()] = config[var]
        
        elif config['storage_type'] == 'tg':
            if 'tg_endpoint' in config:
                os.environ['TG_ENDPOINT'] = config['tg_endpoint']
            if 'tg_password' in config:
                os.environ['TG_PASSWORD'] = config['tg_password']
                
        elif config['storage_type'] == 'alist':
            alist_vars = ['alist_endpoint', 'alist_username', 'alist_password', 'alist_path']
            for var in alist_vars:
                if var in config:
                    os.environ[var.upper()] = config[var]

    # 功能配置
    if 'azure_speech_key' in config:
        os.environ['AZURE_SPEECH_KEY'] = config['azure_speech_key']
    if 'azure_speech_region' in config:
        os.environ['AZURE_SPEECH_REGION'] = config['azure_speech_region']
    if 'ocr_endpoint' in config:
        os.environ['OCR_ENDPOINT'] = config['ocr_endpoint']

@router.get("/config", response_class=HTMLResponse)
async def config_page(request: Request):
    """配置页面"""
    return templates.TemplateResponse("config.html", {"request": request})

@router.get("/api/config")
async def get_config():
    """获取当前配置"""
    return config_manager.get_config()

@router.post("/api/config")
async def update_config(config: Dict[str, Any]):
    """更新配置"""
    try:
        # 使用 config_manager 保存配置
        config_manager.save_config(config)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
