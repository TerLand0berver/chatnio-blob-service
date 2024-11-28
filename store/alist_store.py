import os
import requests
from typing import Optional, BinaryIO
from datetime import datetime
from .base import BaseStore

class AlistStore(BaseStore):
    def __init__(self):
        self.endpoint = os.getenv('ALIST_ENDPOINT', '').rstrip('/')
        self.username = os.getenv('ALIST_USERNAME', '')
        self.password = os.getenv('ALIST_PASSWORD', '')
        self.path = os.getenv('ALIST_PATH', '/blob').rstrip('/')
        self.token = None
        self._login()

    def _login(self):
        """登录获取token"""
        if not all([self.endpoint, self.username, self.password]):
            raise ValueError("Alist configuration is incomplete")
        
        try:
            response = requests.post(
                f"{self.endpoint}/api/auth/login",
                json={
                    "username": self.username,
                    "password": self.password
                }
            )
            response.raise_for_status()
            data = response.json()
            if data.get("code") == 200:
                self.token = data.get("data", {}).get("token")
            else:
                raise ValueError(f"Alist login failed: {data.get('message')}")
        except Exception as e:
            raise ValueError(f"Failed to login to Alist: {str(e)}")

    def _get_headers(self):
        """获取请求头"""
        if not self.token:
            self._login()
        return {
            "Authorization": self.token
        }

    def _upload_file(self, file_data: BinaryIO, filename: str) -> str:
        """上传文件到Alist"""
        try:
            # 构建完整的文件路径
            date_path = datetime.now().strftime('%Y%m')
            full_path = f"{self.path}/{date_path}/{filename}"
            
            # 创建目录
            requests.post(
                f"{self.endpoint}/api/fs/mkdir",
                headers=self._get_headers(),
                json={"path": f"{self.path}/{date_path}"}
            )

            # 上传文件
            files = {
                'file': (filename, file_data)
            }
            response = requests.put(
                f"{self.endpoint}/api/fs/form",
                headers=self._get_headers(),
                data={"path": f"{self.path}/{date_path}"},
                files=files
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get("code") == 200:
                return f"{self.endpoint}/d{full_path}"
            else:
                raise ValueError(f"Upload failed: {data.get('message')}")
                
        except Exception as e:
            raise ValueError(f"Failed to upload file to Alist: {str(e)}")

    def save(self, file_data: BinaryIO, filename: str) -> str:
        """保存文件并返回URL"""
        return self._upload_file(file_data, filename)

    def get(self, url: str) -> Optional[bytes]:
        """从URL获取文件内容"""
        try:
            response = requests.get(url, headers=self._get_headers())
            response.raise_for_status()
            return response.content
        except Exception:
            return None
