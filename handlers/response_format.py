import json
import os
from typing import Any, Dict, Optional
from pydantic import BaseModel

class ResponseFormat(BaseModel):
    """响应格式配置"""
    status_field: str = "status"
    type_field: str = "type"
    content_field: str = "content"
    error_field: str = "error"
    success_value: Any = True
    error_value: Any = False
    include_type: bool = True
    wrap_content: bool = False
    content_wrapper: Optional[Dict[str, str]] = None

def get_response_format() -> ResponseFormat:
    """获取当前响应格式配置"""
    try:
        format_json = os.getenv('API_RESPONSE_FORMAT', '{}')
        format_dict = json.loads(format_json)
        return ResponseFormat(**format_dict)
    except Exception:
        return ResponseFormat()

def format_success_response(file_type: str, content: str) -> Dict[str, Any]:
    """格式化成功响应"""
    format_config = get_response_format()
    response = {
        format_config.status_field: format_config.success_value
    }
    
    if format_config.include_type:
        response[format_config.type_field] = file_type
    
    if format_config.wrap_content and format_config.content_wrapper:
        wrapped_content = format_config.content_wrapper.copy()
        for key, value in wrapped_content.items():
            if value == "${content}":
                wrapped_content[key] = content
        response[format_config.content_field] = wrapped_content
    else:
        response[format_config.content_field] = content
    
    response[format_config.error_field] = ""
    return response

def format_error_response(error_message: str) -> Dict[str, Any]:
    """格式化错误响应"""
    format_config = get_response_format()
    response = {
        format_config.status_field: format_config.error_value,
        format_config.type_field: "",
        format_config.content_field: "",
        format_config.error_field: error_message
    }
    return response
