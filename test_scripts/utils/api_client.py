"""
API Client - 封装HTTP请求，支持加密响应自动解密
"""
import json
import base64
import requests
from typing import Dict, Any, Optional


class APIClient:
    """HTTP API 请求封装"""

    def __init__(self, base_url: str, headers: Optional[Dict[str, str]] = None, timeout: int = 30):
        """
        初始化API客户端

        Args:
            base_url: API基础URL
            headers: 默认请求头
            timeout: 请求超时时间(秒)
        """
        self.base_url = base_url.rstrip('/')
        self.default_headers = headers or {}
        self.timeout = timeout
        self.session = requests.Session()

    def _build_url(self, path: str) -> str:
        """构建完整URL"""
        return f"{self.base_url}/{path.lstrip('/')}"

    def _build_headers(self, headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """合并请求头"""
        merged = self.default_headers.copy()
        if headers:
            merged.update(headers)
        return merged

    def post(self, path: str, data: Optional[Dict[str, Any]] = None,
             headers: Optional[Dict[str, str]] = None, **kwargs) -> Dict[str, Any]:
        """
        POST请求

        Args:
            path: API路径
            data: 请求体数据(dict)
            headers: 额外请求头
            **kwargs: 其他requests参数

        Returns:
            解密后的响应数据(dict)
        """
        url = self._build_url(path)
        req_headers = self._build_headers(headers)

        response = self.session.post(
            url,
            json=data,
            headers=req_headers,
            timeout=kwargs.pop('timeout', self.timeout),
            **kwargs
        )

        return self._handle_response(response)

    def get(self, path: str, params: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None, **kwargs) -> Dict[str, Any]:
        """
        GET请求

        Args:
            path: API路径
            params: URL查询参数
            headers: 额外请求头
            **kwargs: 其他requests参数

        Returns:
            解密后的响应数据(dict)
        """
        url = self._build_url(path)
        req_headers = self._build_headers(headers)

        response = self.session.get(
            url,
            params=params,
            headers=req_headers,
            timeout=kwargs.pop('timeout', self.timeout),
            **kwargs
        )

        return self._handle_response(response)

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """
        处理HTTP响应，自动解密加密字段

        Args:
            response: requests.Response对象

        Returns:
            解析后的响应数据
        """
        # 尝试解析JSON
        try:
            result = response.json()
        except json.JSONDecodeError:
            return {
                'success': False,
                'code': response.status_code,
                'msg': f'JSON解析失败: {response.text[:200]}',
                'raw_text': response.text
            }

        # 处理加密响应: { "encrypted": true, "data": "base64编码的加密数据" }
        if isinstance(result, dict) and result.get('encrypted') is True:
            encrypted_data = result.get('data', '')
            if encrypted_data:
                decrypted = self._decrypt_response(encrypted_data)
                if decrypted:
                    try:
                        return json.loads(decrypted)
                    except json.JSONDecodeError:
                        return {
                            'success': False,
                            'code': result.get('code', 'ENCRYPT_ERROR'),
                            'msg': f'加密数据解密后JSON解析失败: {decrypted[:200]}',
                            'raw_decrypted': decrypted
                        }
            return {'success': False, 'code': 'ENCRYPT_ERROR', 'msg': '加密数据为空'}

        return result

    def _decrypt_response(self, encrypted_data: str) -> Optional[str]:
        """
        解密响应数据(简单Base64解码示例，实际项目中可能用AES/RSA)

        Args:
            encrypted_data: Base64编码的加密数据

        Returns:
            解密后的字符串
        """
        try:
            # 简单Base64解码(根据实际加密算法修改)
            decoded = base64.b64decode(encrypted_data)
            return decoded.decode('utf-8')
        except Exception:
            # 如果不是Base64编码，直接返回原数据
            return encrypted_data

    def set_auth_token(self, token: str):
        """设置认证Token"""
        self.default_headers['Authorization'] = f'Bearer {token}'

    def clear_auth_token(self):
        """清除认证Token"""
        self.default_headers.pop('Authorization', None)
