import json
import os
from typing import Dict, Any, List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

class ConfigManager:
    _instance = None
    _app: FastAPI = None
    _config: Dict[str, Any] = {}
    _cors_middleware = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
        return cls._instance

    @classmethod
    def initialize(cls, app: FastAPI):
        cls._app = app
        cls._load_config()
        # 初始化时添加 CORS 中间件
        cls._setup_cors()

    @classmethod
    def _setup_cors(cls):
        """设置 CORS 中间件"""
        origins = cls._get_cors_origins()
        
        # 如果已经存在 CORS 中间件，先移除它
        if cls._cors_middleware is not None:
            cls._app.middleware_stack = None
            cls._app.middleware_stack = cls._app.build_middleware_stack()
        
        # 添加新的 CORS 中间件
        cls._cors_middleware = CORSMiddleware(
            app=cls._app,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
            allow_origin_regex=None,
            expose_headers=["*"],
            max_age=600,
        )
        
        # 重建中间件栈
        if cls._app.middleware_stack is None:
            cls._app.middleware_stack = cls._app.build_middleware_stack()

    @classmethod
    def _get_cors_origins(cls) -> List[str]:
        """获取 CORS origins 配置
        
        配置优先级：
        1. 环境变量 CORS_ALLOW_ORIGINS
        2. 配置文件中的 cors_allow_origins
        3. 默认值 "*"
        
        支持的格式：
        - "*" 表示允许所有源
        - 单个域名
        - 逗号分隔的多个域名
        """
        # 从环境变量或配置文件获取origins
        origins = os.getenv('CORS_ALLOW_ORIGINS') or cls._config.get('cors_allow_origins', '*')

        # 处理字符串格式的origins
        if isinstance(origins, str):
            # 如果是通配符，直接返回
            if origins.strip() == '*':
                return ['*']
            # 分割并清理域名列表
            origins = [origin.strip() for origin in origins.split(',') if origin.strip()]

        # 如果origins是空列表或None，使用默认值
        if not origins:
            return ['*']

        # 验证域名格式
        valid_origins = []
        for origin in origins:
            # 跳过通配符
            if origin == '*':
                return ['*']
            # 验证域名格式（简单验证，确保包含协议和域名）
            if '://' in origin and '.' in origin:
                valid_origins.append(origin)

        # 如果没有有效的域名，返回默认值
        return valid_origins or ['*']

    @classmethod
    def _load_config(cls):
        """从文件和环境变量加载配置"""
        config_file = "config.json"
        config = {}
        
        # 1. 从文件加载配置
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
            except json.JSONDecodeError:
                pass

        # 2. 从环境变量加载配置
        env_cors = os.getenv('CORS_ALLOW_ORIGINS')
        if env_cors:
            config['cors_allow_origins'] = env_cors

        # 3. 确保配置文件存在
        if not os.path.exists(config_file):
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)

        cls._config = config

    @classmethod
    def save_config(cls, config: Dict[str, Any]) -> None:
        """保存配置到文件并更新运行时配置"""
        with open("config.json", 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        cls._config = config
        cls._update_runtime_config()

    @classmethod
    def get_config(cls) -> Dict[str, Any]:
        """获取当前配置"""
        return cls._config

    @classmethod
    def _update_runtime_config(cls):
        """更新运行时配置"""
        config = cls._config

        # 更新 CORS 配置
        if 'cors_allow_origins' in config:
            cls._setup_cors()

        # 更新环境变量
        cls._update_env_vars(config)

    @classmethod
    def _update_env_vars(cls, config: Dict[str, Any]):
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
                if isinstance(api_format['content_wrapper'], str):
                    api_format['content_wrapper'] = json.loads(api_format['content_wrapper'])
            except json.JSONDecodeError:
                api_format['content_wrapper'] = None
                api_format['wrap_content'] = False
        
        os.environ['API_RESPONSE_FORMAT'] = json.dumps(api_format)

        # 基础配置
        env_mappings = {
            'pdf_max_images': 'PDF_MAX_IMAGES',
            'max_file_size': 'MAX_FILE_SIZE',
            'cors_allow_origins': 'CORS_ALLOW_ORIGINS',
            'storage_type': 'STORAGE_TYPE',
            'local_storage_domain': 'LOCAL_STORAGE_DOMAIN',
            's3_access_key': 'S3_ACCESS_KEY',
            's3_secret_key': 'S3_SECRET_KEY',
            's3_bucket': 'S3_BUCKET',
            's3_region': 'S3_REGION',
            's3_domain': 'S3_DOMAIN',
            'tg_endpoint': 'TG_ENDPOINT',
            'tg_password': 'TG_PASSWORD',
            'azure_speech_key': 'AZURE_SPEECH_KEY',
            'azure_speech_region': 'AZURE_SPEECH_REGION',
            'ocr_endpoint': 'OCR_ENDPOINT',
        }

        for config_key, env_key in env_mappings.items():
            if config_key in config:
                os.environ[env_key] = str(config[config_key])

        # 特殊处理存储配置
        if config.get('storage_type') == 'alist':
            alist_vars = ['alist_endpoint', 'alist_username', 'alist_password', 'alist_path']
            for var in alist_vars:
                if var in config:
                    os.environ[var.upper()] = str(config[var])

config_manager = ConfigManager()
