"""
飞书个税API接口测试 - pytest配置和共享fixture
测试范围: 扣缴义务人模块、人员报送模块、个税计算模块、个税申报模块
"""
import pytest
import requests
import json
import time
from typing import Dict, Any, Optional


# ============================================================================
# 全局配置
# ============================================================================
BASE_URL = "https://api.example.com"  # 实际环境替换
TIMEOUT = 30

# 默认请求头
DEFAULT_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer test_token_placeholder",  # 实际环境替换
}


# ============================================================================
# 工具函数
# ============================================================================
def decrypt_response(response_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    解密响应数据
    实际项目中根据加密方式实现，此处为占位实现
    """
    if isinstance(response_data, dict):
        # 如果响应被加密，通常会有加密字段
        if "encryptedData" in response_data:
            # TODO: 根据实际加密方式解密
            return response_data.get("decryptedData", response_data)
    return response_data


def assert_response_success(
    response: requests.Response,
    expected_success: bool = True,
    expected_msg: Optional[str] = None
):
    """
    通用响应断言
    
    Args:
        response: requests响应对象
        expected_success: 期望success字段值
        expected_msg: 期望的消息关键词（可选）
    """
    assert response.status_code == 200, f"HTTP状态码应为200，实际为{response.status_code}"
    
    data = response.json()
    
    # 解密处理
    if "data" in data and isinstance(data["data"], str) and data["data"].startswith("encrypted:"):
        data["data"] = decrypt_response(data)
    
    # 断言success字段
    actual_success = data.get("success")
    assert actual_success == expected_success, \
        f"success应为{expected_success}，实际为{actual_success}，完整响应: {data}"
    
    # 如果指定了期望消息关键词，进行模糊匹配
    if expected_msg and not (expected_msg in str(data.get("msg", "")) or expected_msg in str(data.get("message", ""))):
        # 对于包含错误的情况，也检查code
        if not expected_success:
            # 反向用例允许msg为空或包含错误信息
            pass
        else:
            pytest.fail(f"响应消息应包含'{expected_msg}'，实际消息: {data.get('msg', data.get('message', ''))}")


def assert_response_code(response: requests.Response, expected_code: str = "200"):
    """
    断言业务状态码
    
    Args:
        response: requests响应对象
        expected_code: 期望的业务状态码
    """
    assert response.status_code == 200, f"HTTP状态码应为200，实际为{response.status_code}"
    data = response.json()
    actual_code = data.get("code", data.get("success"))
    assert str(actual_code) == str(expected_code), \
        f"业务状态码应为{expected_code}，实际为{actual_code}，完整响应: {data}"


def assert_field_exists(data: Dict[str, Any], *fields: str, parent_key: str = "data"):
    """
    断言字段存在
    
    Args:
        data: 响应数据字典
        *fields: 要检查的字段名（支持嵌套，如"list", "0", "xm"）
        parent_key: 父级字段名
    """
    current = data.get(parent_key, data)
    for field in fields:
        if field.isdigit():
            index = int(field)
            assert isinstance(current, list) and len(current) > index, \
                f"{parent_key}应为非空列表，且索引{index}存在"
            current = current[index]
        else:
            assert field in current, \
                f"字段'{field}'不存在于{parent_key}中，可用字段: {list(current.keys()) if isinstance(current, dict) else type(current)}"
            current = current[field]


def assert_field_value(data: Dict[str, Any], field_path: str, expected_value: Any):
    """
    断言字段值
    
    Args:
        data: 响应数据字典
        field_path: 字段路径，用"."分隔，如"data.list.0.xm"
        expected_value: 期望值
    """
    parts = field_path.split(".")
    current = data
    for part in parts:
        if part.isdigit():
            current = current[int(part)]
        else:
            current = current[part]
    
    assert current == expected_value, \
        f"字段{field_path}应为{expected_value}，实际为{current}"


# ============================================================================
# API客户端
# ============================================================================
class APIClient:
    """API请求封装类"""
    
    def __init__(self, base_url: str = BASE_URL, headers: Dict[str, str] = None):
        self.base_url = base_url
        self.headers = headers or DEFAULT_HEADERS.copy()
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def post(self, path: str, json_data: Dict[str, Any], **kwargs) -> requests.Response:
        """POST请求"""
        url = f"{self.base_url}{path}"
        response = self.session.post(url, json=json_data, timeout=TIMEOUT, **kwargs)
        return response
    
    def get(self, path: str, **kwargs) -> requests.Response:
        """GET请求"""
        url = f"{self.base_url}{path}"
        response = self.session.get(url, timeout=TIMEOUT, **kwargs)
        return response
    
    def set_token(self, token: str):
        """设置认证token"""
        self.session.headers["Authorization"] = f"Bearer {token}"


# ============================================================================
# Pytest Fixtures
# ============================================================================
@pytest.fixture(scope="session")
def api_client():
    """全局API客户端"""
    client = APIClient()
    return client


@pytest.fixture(scope="session")
def base_url():
    """Base URL配置"""
    return BASE_URL


@pytest.fixture(scope="session")
def default_headers():
    """默认请求头"""
    return DEFAULT_HEADERS.copy()


@pytest.fixture
def withholding_agent_base_data():
    """
    扣缴义务人模块 - 基础测试数据
    
    包含所有接口共用的必填字段默认值
    """
    return {
        "cpId": 1001,
        "agentCode": "Agent001",
        "agentName": "XX科技有限公司",
        "nsrsbh": "91310000XXXXXXXX1K",
        "sbmm": "12345678",
        "passwordVerificationType": "01",
        "areaid": "310000",
        "djxhid": "DJXH20250301001",
        "zgswjg": "国家税务总局上海市税务局",
    }


@pytest.fixture
def person_base_data():
    """
    人员报送模块 - 基础测试数据
    
    包含人员接口共用的必填字段默认值
    """
    return {
        "cpId": "1001",
        "xm": "张三",
        "zzlx": "A",
        "zzhm": "310101199001011234",
        "kjsrybm": "Agent001",
        "kjsry": "XX科技有限公司",
        "sfgy": "01",
        "sdyf": "202503",
        "taxClassCode": "PLAN_abc123def456",
    }


@pytest.fixture
def salary_import_base_data():
    """
    个税计算模块 - 薪酬数据导入基础数据
    """
    return {
        "cpId": 1001,
        "nsrsbh": "91310000XXXXXXXX1K",
        "taxClassCode": "TC2025001",
        "sdyf": "202503",
    }


@pytest.fixture
def declaration_base_data():
    """
    个税申报模块 - 基础测试数据
    """
    return {
        "agentCode": "Agent001",
        "sdyf": "202503",
        "sdlx": "综合所得",
        "areaid": "310000",
        "djxhid": "DJXH20250301001",
        "sbmm": "12345678",
    }


@pytest.fixture
def declaration_rd_base_data():
    """
    个税申报模块(研发版) - 基础测试数据
    """
    return {
        "cpId": 1001,
        "taxClassCode": "TAX_CLASS_001",
        "sdyf": "2026-03",
        "categoryCode": "01",
    }


@pytest.fixture
def generate_unique_id():
    """
    生成唯一ID的工厂函数
    用于创建不重复的测试数据
    """
    counter = 0
    def _generate(prefix: str = "TEST") -> str:
        nonlocal counter
        counter += 1
        timestamp = int(time.time() * 1000) % 1000000
        return f"{prefix}{timestamp}{counter:03d}"
    return _generate


@pytest.fixture
def sample_person_list(generate_unique_id):
    """
    生成示例人员列表数据
    """
    unique_id = generate_unique_id()
    return [
        {
            "xm": f"员工{unique_id}A",
            "zzlx": "A",
            "zzhm": f"31010119900101{unique_id[:4]}",
            "kjsrybm": "Agent001",
            "kjsry": "XX科技有限公司",
            "sfgy": "01",
            "sdyf": "202503",
            "taxClassCode": "PLAN_abc123def456",
            "lxdh": "13800138000"
        },
        {
            "xm": f"员工{unique_id}B",
            "zzlx": "A",
            "zzhm": f"31010119900202{unique_id[:4]}",
            "kjsrybm": "Agent001",
            "kjsry": "XX科技有限公司",
            "sfgy": "01",
            "sdyf": "202503",
            "taxClassCode": "PLAN_abc123def456",
        }
    ]


@pytest.fixture
def sample_salary_data(generate_unique_id):
    """
    生成示例薪酬数据
    """
    unique_id = generate_unique_id()
    return [
        {
            "xm": f"张三{unique_id}",
            "zzlx": "A",
            "zzhm": f"31010119900101{unique_id[:4]}",
            "itemCode": "01010101",
            "pch": 1,
            "sre": 15000.00,
            "jbylaobxf": 960.00,
            "jbylbxf": 240.00,
            "sybxf": 60.00,
            "zfgjj": 1200.00
        },
        {
            "xm": f"李四{unique_id}",
            "zzlx": "A",
            "zzhm": f"31010119900202{unique_id[:4]}",
            "itemCode": "01010101",
            "pch": 2,
            "sre": 20000.00,
            "jbylaobxf": 1280.00,
            "jbylbxf": 320.00,
            "sybxf": 80.00,
            "zfgjj": 1600.00
        }
    ]


# ============================================================================
# Pytest配置
# ============================================================================
def pytest_configure(config):
    """pytest配置钩子"""
    config.addinivalue_line(
        "markers", "wa: 扣缴义务人模块测试用例"
    )
    config.addinivalue_line(
        "markers", "ps: 人员报送模块测试用例"
    )
    config.addinivalue_line(
        "markers", "tc: 个税计算模块测试用例"
    )
    config.addinivalue_line(
        "markers", "td: 个税申报模块测试用例(旧版)"
    )
    config.addinivalue_line(
        "markers", "rd: 个税申报模块测试用例(研发版)"
    )
    config.addinivalue_line(
        "markers", "p0: P0级别用例，核心功能"
    )
    config.addinivalue_line(
        "markers", "p1: P1级别用例，重要功能"
    )
    config.addinivalue_line(
        "markers", "p2: P2级别用例，边缘功能"
    )
    config.addinivalue_line(
        "markers", "正向: 正向测试用例"
    )
    config.addinivalue_line(
        "markers", "反向: 反向测试用例"
    )
    config.addinivalue_line(
        "markers", "边界值: 边界值测试用例"
    )
    config.addinivalue_line(
        "markers", "分页: 分页测试用例"
    )
    config.addinivalue_line(
        "markers", "幂等: 幂等性测试用例"
    )
    config.addinivalue_line(
        "markers", "鉴权: 鉴权测试用例"
    )
    config.addinivalue_line(
        "markers", "场景: 场景测试用例"
    )


def pytest_collection_modifyitems(config, items):
    """自动为测试用例添加标记"""
    for item in items:
        # 根据测试函数名自动添加模块标记
        if "wa" in item.nodeid.lower() or "withholding" in item.nodeid.lower():
            item.add_marker(pytest.mark.wa)
        elif "ps" in item.nodeid.lower() or "person" in item.nodeid.lower():
            item.add_marker(pytest.mark.ps)
        elif "tc" in item.nodeid.lower() or "taxcompute" in item.nodeid.lower() or "salary" in item.nodeid.lower():
            item.add_marker(pytest.mark.tc)
        elif "td" in item.nodeid.lower() and "rd" not in item.nodeid.lower():
            item.add_marker(pytest.mark.td)
        elif "rd" in item.nodeid.lower():
            item.add_marker(pytest.mark.rd)
        
        # 根据用例编号添加优先级标记
        for marker in item.iter_markers():
            if marker.name.startswith("p"):
                priority = marker.name.upper()
                if priority in ["P0", "P1", "P2"]:
                    if priority == "P0":
                        item.add_marker(pytest.mark.p0)
                    elif priority == "P1":
                        item.add_marker(pytest.mark.p1)
                    else:
                        item.add_marker(pytest.mark.p2)
