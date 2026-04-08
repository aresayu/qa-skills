"""
扣缴义务人模块测试用例 (WA)
接口路径前缀: /api/v2/tax/withholding-agent

测试范围:
- WA01: 新增扣缴义务人
- WA02: 更新扣缴义务人
- WA03: 获取扣缴义务人详情
- WA04: 查询扣缴义务人列表
- WA05: 搜索扣缴义务人
- WA06: 删除扣缴义务人
- WA07: 获取报税地区列表
- WA08: 预获取税局任务ID
- WA09: 根据任务ID查询税务机关

共计: 60+ 测试用例
"""
import pytest
import requests
from tests.conftest import assert_response_success, assert_response_code


# ============================================================================
# WA01: 新增扣缴义务人
# 接口路径: POST /api/v2/tax/withholding-agent/create
# ============================================================================

@pytest.mark.WA01
class TestWA01CreateWithholdingAgent:
    """新增扣缴义务人"""
    
    @pytest.mark.P0
    @pytest.mark.正向
    def test_wa01_001_create_with_all_required_params_success(self, api_client, generate_unique_id):
        """WA01-001: 新增扣缴义务人-正常参数-成功"""
        unique_id = generate_unique_id("WA01")
        request_data = {
            "cpId": 1001,
            "agentCode": f"A{unique_id[-12:]}",
            "agentName": "XX科技有限公司",
            "nsrsbh": "91310000XXXXXXXX1K",
            "sbmm": "12345678",
            "passwordVerificationType": "01",
            "areaid": "310000",
            "djxhid": "DJXH20250301001",
            "zgswjg": "国家税务总局上海市税务局",
            "bmbh": "BM001"
        }
        response = api_client.post("/api/v2/tax/withholding-agent/create", json_data=request_data)
        assert_response_success(response, expected_success=True)
        data = response.json()
        assert "data" in data

    @pytest.mark.P0
    @pytest.mark.反向
    def test_wa01_002_missing_cpId_fail(self, api_client):
        """WA01-002: 新增扣缴义务人-缺少cpId-失败"""
        request_data = {
            "agentCode": "Agent001",
            "agentName": "XX科技有限公司",
            "nsrsbh": "91310000XXXXXXXX1K",
            "sbmm": "12345678",
            "passwordVerificationType": "01",
            "areaid": "310000",
            "djxhid": "DJXH20250301001",
            "zgswjg": "国家税务总局上海市税务局"
        }
        response = api_client.post("/api/v2/tax/withholding-agent/create", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="cpId")

    @pytest.mark.P0
    @pytest.mark.反向
    def test_wa01_003_missing_agentCode_fail(self, api_client):
        """WA01-003: 新增扣缴义务人-缺少agentCode-失败"""
        request_data = {
            "cpId": 1001,
            "agentName": "XX科技有限公司",
            "nsrsbh": "91310000XXXXXXXX1K",
            "sbmm": "12345678",
            "passwordVerificationType": "01",
            "areaid": "310000",
            "djxhid": "DJXH20250301001",
            "zgswjg": "国家税务总局上海市税务局"
        }
        response = api_client.post("/api/v2/tax/withholding-agent/create", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="agentCode")

    @pytest.mark.P0
    @pytest.mark.反向
    def test_wa01_004_missing_agentName_fail(self, api_client):
        """WA01-004: 新增扣缴义务人-缺少agentName-失败"""
        request_data = {
            "cpId": 1001,
            "agentCode": "Agent001",
            "nsrsbh": "91310000XXXXXXXX1K",
            "sbmm": "12345678",
            "passwordVerificationType": "01",
            "areaid": "310000",
            "djxhid": "DJXH20250301001",
            "zgswjg": "国家税务总局上海市税务局"
        }
        response = api_client.post("/api/v2/tax/withholding-agent/create", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="agentName")

    @pytest.mark.P0
    @pytest.mark.反向
    def test_wa01_005_missing_nsrsbh_fail(self, api_client):
        """WA01-005: 新增扣缴义务人-缺少nsrsbh-失败"""
        request_data = {
            "cpId": 1001,
            "agentCode": "Agent001",
            "agentName": "XX科技有限公司",
            "sbmm": "12345678",
            "passwordVerificationType": "01",
            "areaid": "310000",
            "djxhid": "DJXH20250301001",
            "zgswjg": "国家税务总局上海市税务局"
        }
        response = api_client.post("/api/v2/tax/withholding-agent/create", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="nsrsbh")

    @pytest.mark.P0
    @pytest.mark.反向
    def test_wa01_006_missing_sbmm_fail(self, api_client):
        """WA01-006: 新增扣缴义务人-缺少sbmm-失败"""
        request_data = {
            "cpId": 1001,
            "agentCode": "Agent001",
            "agentName": "XX科技有限公司",
            "nsrsbh": "91310000XXXXXXXX1K",
            "passwordVerificationType": "01",
            "areaid": "310000",
            "djxhid": "DJXH20250301001",
            "zgswjg": "国家税务总局上海市税务局"
        }
        response = api_client.post("/api/v2/tax/withholding-agent/create", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="sbmm")

    @pytest.mark.P0
    @pytest.mark.反向
    def test_wa01_007_missing_passwordVerificationType_fail(self, api_client):
        """WA01-007: 新增扣缴义务人-缺少passwordVerificationType-失败"""
        request_data = {
            "cpId": 1001,
            "agentCode": "Agent001",
            "agentName": "XX科技有限公司",
            "nsrsbh": "91310000XXXXXXXX1K",
            "sbmm": "12345678",
            "areaid": "310000",
            "djxhid": "DJXH20250301001",
            "zgswjg": "国家税务总局上海市税务局"
        }
        response = api_client.post("/api/v2/tax/withholding-agent/create", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="passwordVerificationType")

    @pytest.mark.P0
    @pytest.mark.反向
    def test_wa01_008_missing_areaid_fail(self, api_client):
        """WA01-008: 新增扣缴义务人-缺少areaid-失败"""
        request_data = {
            "cpId": 1001,
            "agentCode": "Agent001",
            "agentName": "XX科技有限公司",
            "nsrsbh": "91310000XXXXXXXX1K",
            "sbmm": "12345678",
            "passwordVerificationType": "01",
            "djxhid": "DJXH20250301001",
            "zgswjg": "国家税务总局上海市税务局"
        }
        response = api_client.post("/api/v2/tax/withholding-agent/create", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="areaid")

    @pytest.mark.P0
    @pytest.mark.反向
    def test_wa01_009_missing_djxhid_fail(self, api_client):
        """WA01-009: 新增扣缴义务人-缺少djxhid-失败"""
        request_data = {
            "cpId": 1001,
            "agentCode": "Agent001",
            "agentName": "XX科技有限公司",
            "nsrsbh": "91310000XXXXXXXX1K",
            "sbmm": "12345678",
            "passwordVerificationType": "01",
            "areaid": "310000",
            "zgswjg": "国家税务总局上海市税务局"
        }
        response = api_client.post("/api/v2/tax/withholding-agent/create", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="djxhid")

    @pytest.mark.P0
    @pytest.mark.反向
    def test_wa01_010_missing_zgswjg_fail(self, api_client):
        """WA01-010: 新增扣缴义务人-缺少zgswjg-失败"""
        request_data = {
            "cpId": 1001,
            "agentCode": "Agent001",
            "agentName": "XX科技有限公司",
            "nsrsbh": "91310000XXXXXXXX1K",
            "sbmm": "12345678",
            "passwordVerificationType": "01",
            "areaid": "310000",
            "djxhid": "DJXH20250301001"
        }
        response = api_client.post("/api/v2/tax/withholding-agent/create", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="zgswjg")

    @pytest.mark.P1
    @pytest.mark.反向
    def test_wa01_011_agentCode_invalid_format_fail(self, api_client):
        """WA01-011: 新增扣缴义务人-agentCode格式错误-失败"""
        request_data = {
            "cpId": 1001,
            "agentCode": "Agent@001!",
            "agentName": "XX科技有限公司",
            "nsrsbh": "91310000XXXXXXXX1K",
            "sbmm": "12345678",
            "passwordVerificationType": "01",
            "areaid": "310000",
            "djxhid": "DJXH20250301001",
            "zgswjg": "国家税务总局上海市税务局"
        }
        response = api_client.post("/api/v2/tax/withholding-agent/create", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="agentCode")

    @pytest.mark.P1
    @pytest.mark.边界值
    def test_wa01_012_agentCode_too_short_fail(self, api_client):
        """WA01-012: 新增扣缴义务人-agentCode长度不足4位-失败"""
        request_data = {
            "cpId": 1001,
            "agentCode": "A01",
            "agentName": "XX科技有限公司",
            "nsrsbh": "91310000XXXXXXXX1K",
            "sbmm": "12345678",
            "passwordVerificationType": "01",
            "areaid": "310000",
            "djxhid": "DJXH20250301001",
            "zgswjg": "国家税务总局上海市税务局"
        }
        response = api_client.post("/api/v2/tax/withholding-agent/create", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="agentCode")

    @pytest.mark.P1
    @pytest.mark.边界值
    def test_wa01_013_agentCode_too_long_fail(self, api_client):
        """WA01-013: 新增扣缴义务人-agentCode长度超过16位-失败"""
        request_data = {
            "cpId": 1001,
            "agentCode": "AgentCode12345678901",
            "agentName": "XX科技有限公司",
            "nsrsbh": "91310000XXXXXXXX1K",
            "sbmm": "12345678",
            "passwordVerificationType": "01",
            "areaid": "310000",
            "djxhid": "DJXH20250301001",
            "zgswjg": "国家税务总局上海市税务局"
        }
        response = api_client.post("/api/v2/tax/withholding-agent/create", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="agentCode")

    @pytest.mark.P1
    @pytest.mark.反向
    def test_wa01_014_nsrsbh_invalid_format_fail(self, api_client):
        """WA01-014: 新增扣缴义务人-nsrsbh格式错误-失败"""
        request_data = {
            "cpId": 1001,
            "agentCode": "Agent001",
            "agentName": "XX科技有限公司",
            "nsrsbh": "ABCDEFG",
            "sbmm": "12345678",
            "passwordVerificationType": "01",
            "areaid": "310000",
            "djxhid": "DJXH20250301001",
            "zgswjg": "国家税务总局上海市税务局"
        }
        response = api_client.post("/api/v2/tax/withholding-agent/create", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="nsrsbh")

    @pytest.mark.P2
    @pytest.mark.边界值
    def test_wa01_015_nsrsbh_15_digits_success(self, api_client, generate_unique_id):
        """WA01-015: 新增扣缴义务人-nsrsbh长度15位-成功"""
        request_data = {
            "cpId": 1001,
            "agentCode": f"A{generate_unique_id()[-4:]}",
            "agentName": "XX科技有限公司",
            "nsrsbh": "91310000XXXXXK",
            "sbmm": "12345678",
            "passwordVerificationType": "01",
            "areaid": "310000",
            "djxhid": "DJXH20250301001",
            "zgswjg": "国家税务总局上海市税务局"
        }
        response = api_client.post("/api/v2/tax/withholding-agent/create", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P2
    @pytest.mark.边界值
    def test_wa01_016_nsrsbh_17_digits_success(self, api_client, generate_unique_id):
        """WA01-016: 新增扣缴义务人-nsrsbh长度17位-成功"""
        request_data = {
            "cpId": 1001,
            "agentCode": f"A{generate_unique_id()[-4:]}",
            "agentName": "YY科技有限公司",
            "nsrsbh": "9131000XXXXXXXK",
            "sbmm": "12345678",
            "passwordVerificationType": "01",
            "areaid": "310000",
            "djxhid": "DJXH20250301001",
            "zgswjg": "国家税务总局上海市税务局"
        }
        response = api_client.post("/api/v2/tax/withholding-agent/create", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P2
    @pytest.mark.边界值
    def test_wa01_017_nsrsbh_18_digits_success(self, api_client, generate_unique_id):
        """WA01-017: 新增扣缴义务人-nsrsbh长度18位-成功"""
        request_data = {
            "cpId": 1001,
            "agentCode": f"A{generate_unique_id()[-4:]}",
            "agentName": "ZZ科技有限公司",
            "nsrsbh": "91310000XXXXXXXX1K",
            "sbmm": "12345678",
            "passwordVerificationType": "01",
            "areaid": "310000",
            "djxhid": "DJXH20250301001",
            "zgswjg": "国家税务总局上海市税务局"
        }
        response = api_client.post("/api/v2/tax/withholding-agent/create", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P2
    @pytest.mark.边界值
    def test_wa01_018_nsrsbh_20_digits_success(self, api_client, generate_unique_id):
        """WA01-018: 新增扣缴义务人-nsrsbh长度20位-成功"""
        request_data = {
            "cpId": 1001,
            "agentCode": f"A{generate_unique_id()[-4:]}",
            "agentName": "AA科技有限公司",
            "nsrsbh": "91310000XXXXXXXXXXXK",
            "sbmm": "12345678",
            "passwordVerificationType": "01",
            "areaid": "310000",
            "djxhid": "DJXH20250301001",
            "zgswjg": "国家税务总局上海市税务局"
        }
        response = api_client.post("/api/v2/tax/withholding-agent/create", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    @pytest.mark.边界值
    def test_wa01_019_sbmm_too_short_fail(self, api_client):
        """WA01-019: 新增扣缴义务人-sbmm长度不足8位-失败"""
        request_data = {
            "cpId": 1001,
            "agentCode": "Agent001",
            "agentName": "XX科技有限公司",
            "nsrsbh": "91310000XXXXXXXX1K",
            "sbmm": "1234567",
            "passwordVerificationType": "01",
            "areaid": "310000",
            "djxhid": "DJXH20250301001",
            "zgswjg": "国家税务总局上海市税务局"
        }
        response = api_client.post("/api/v2/tax/withholding-agent/create", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="sbmm")

    @pytest.mark.P1
    @pytest.mark.边界值
    def test_wa01_020_sbmm_too_long_fail(self, api_client):
        """WA01-020: 新增扣缴义务人-sbmm长度超过20位-失败"""
        request_data = {
            "cpId": 1001,
            "agentCode": "Agent001",
            "agentName": "XX科技有限公司",
            "nsrsbh": "91310000XXXXXXXX1K",
            "sbmm": "123456789012345678901",
            "passwordVerificationType": "01",
            "areaid": "310000",
            "djxhid": "DJXH20250301001",
            "zgswjg": "国家税务总局上海市税务局"
        }
        response = api_client.post("/api/v2/tax/withholding-agent/create", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="sbmm")

    @pytest.mark.P1
    @pytest.mark.边界值
    def test_wa01_021_areaid_too_short_fail(self, api_client):
        """WA01-021: 新增扣缴义务人-areaid长度不足6位-失败"""
        request_data = {
            "cpId": 1001,
            "agentCode": "Agent001",
            "agentName": "XX科技有限公司",
            "nsrsbh": "91310000XXXXXXXX1K",
            "sbmm": "12345678",
            "passwordVerificationType": "01",
            "areaid": "31000",
            "djxhid": "DJXH20250301001",
            "zgswjg": "国家税务总局上海市税务局"
        }
        response = api_client.post("/api/v2/tax/withholding-agent/create", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="areaid")

    @pytest.mark.P1
    @pytest.mark.边界值
    def test_wa01_022_areaid_too_long_fail(self, api_client):
        """WA01-022: 新增扣缴义务人-areaid长度超过6位-失败"""
        request_data = {
            "cpId": 1001,
            "agentCode": "Agent001",
            "agentName": "XX科技有限公司",
            "nsrsbh": "91310000XXXXXXXX1K",
            "sbmm": "12345678",
            "passwordVerificationType": "01",
            "areaid": "3100000",
            "djxhid": "DJXH20250301001",
            "zgswjg": "国家税务总局上海市税务局"
        }
        response = api_client.post("/api/v2/tax/withholding-agent/create", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="areaid")

    @pytest.mark.P1
    @pytest.mark.反向
    def test_wa01_023_areaid_non_numeric_fail(self, api_client):
        """WA01-023: 新增扣缴义务人-areaid包含非数字字符-失败"""
        request_data = {
            "cpId": 1001,
            "agentCode": "Agent001",
            "agentName": "XX科技有限公司",
            "nsrsbh": "91310000XXXXXXXX1K",
            "sbmm": "12345678",
            "passwordVerificationType": "01",
            "areaid": "31000A",
            "djxhid": "DJXH20250301001",
            "zgswjg": "国家税务总局上海市税务局"
        }
        response = api_client.post("/api/v2/tax/withholding-agent/create", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="areaid")

    @pytest.mark.P1
    @pytest.mark.反向
    def test_wa01_024_duplicate_agentCode_fail(self, api_client):
        """WA01-024: 新增扣缴义务人-重复agentCode-失败"""
        request_data = {
            "cpId": 1001,
            "agentCode": "DUP001",
            "agentName": "XX科技有限公司2",
            "nsrsbh": "91310000XXXXXXXX2K",
            "sbmm": "12345678",
            "passwordVerificationType": "01",
            "areaid": "310000",
            "djxhid": "DJXH20250301001",
            "zgswjg": "国家税务总局上海市税务局"
        }
        response = api_client.post("/api/v2/tax/withholding-agent/create", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="agentCode")

    @pytest.mark.P1
    @pytest.mark.反向
    def test_wa01_025_duplicate_nsrsbh_fail(self, api_client):
        """WA01-025: 新增扣缴义务人-重复nsrsbh-失败"""
        request_data = {
            "cpId": 1001,
            "agentCode": "Agent005",
            "agentName": "BB科技有限公司",
            "nsrsbh": "EXISTING001",
            "sbmm": "12345678",
            "passwordVerificationType": "01",
            "areaid": "310000",
            "djxhid": "DJXH20250301001",
            "zgswjg": "国家税务总局上海市税务局"
        }
        response = api_client.post("/api/v2/tax/withholding-agent/create", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="nsrsbh")

    @pytest.mark.P1
    @pytest.mark.反向
    def test_wa01_026_invalid_djxhid_fail(self, api_client):
        """WA01-026: 新增扣缴义务人-不存在的djxhid-失败"""
        request_data = {
            "cpId": 1001,
            "agentCode": "Agent001",
            "agentName": "XX科技有限公司",
            "nsrsbh": "91310000XXXXXXXX1K",
            "sbmm": "12345678",
            "passwordVerificationType": "01",
            "areaid": "310000",
            "djxhid": "INVALID_DJXH",
            "zgswjg": "国家税务总局上海市税务局"
        }
        response = api_client.post("/api/v2/tax/withholding-agent/create", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="djxhid")

    @pytest.mark.P2
    @pytest.mark.正向
    def test_wa01_027_empty_pkGroup_success(self, api_client, generate_unique_id):
        """WA01-027: 新增扣缴义务人-可选参数pkGroup为空-成功"""
        request_data = {
            "cpId": 1001,
            "agentCode": f"A{generate_unique_id()[-12:]}",
            "agentName": "CC科技有限公司",
            "nsrsbh": f"91310000XXXXXXXX{generate_unique_id()[-4:]}K",
            "sbmm": "12345678",
            "passwordVerificationType": "01",
            "areaid": "310000",
            "djxhid": "DJXH20250301001",
            "zgswjg": "国家税务总局上海市税务局",
            "pkGroup": ""
        }
        response = api_client.post("/api/v2/tax/withholding-agent/create", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P2
    @pytest.mark.正向
    def test_wa01_028_all_optional_params_success(self, api_client, generate_unique_id):
        """WA01-028: 新增扣缴义务人-所有可选参数都填写-成功"""
        request_data = {
            "cpId": 1001,
            "agentCode": f"A{generate_unique_id()[-12:]}",
            "agentName": "DD科技有限公司",
            "nsrsbh": f"91310000XXXXXXXX{generate_unique_id()[-4:]}K",
            "sbmm": "12345678",
            "passwordVerificationType": "01",
            "areaid": "310000",
            "djxhid": "DJXH20250301001",
            "zgswjg": "国家税务总局上海市税务局",
            "pkGroup": "GROUP001",
            "pkTaxOrg": "ORG001",
            "bmbh": "BM001"
        }
        response = api_client.post("/api/v2/tax/withholding-agent/create", json_data=request_data)
        assert_response_success(response, expected_success=True)


# ============================================================================
# WA02: 更新扣缴义务人
# ============================================================================

@pytest.mark.WA02
class TestWA02UpdateWithholdingAgent:
    """更新扣缴义务人"""
    
    @pytest.mark.P0
    @pytest.mark.正向
    def test_wa02_001_update_success(self, api_client):
        """WA02-001: 更新扣缴义务人-正常参数-成功"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC001",
            "agentName": "XX科技有限公司（更名）",
            "sbmm": "654321"
        }
        response = api_client.post("/api/v2/tax/withholding-agent/update", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P0
    @pytest.mark.反向
    def test_wa02_002_missing_cpId_fail(self, api_client):
        """WA02-002: 更新扣缴义务人-缺少cpId-失败"""
        request_data = {
            "taxClassCode": "TC001",
            "agentName": "XX科技有限公司（更名）"
        }
        response = api_client.post("/api/v2/tax/withholding-agent/update", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="cpId")

    @pytest.mark.P0
    @pytest.mark.反向
    def test_wa02_003_missing_taxClassCode_fail(self, api_client):
        """WA02-003: 更新扣缴义务人-缺少taxClassCode-失败"""
        request_data = {
            "cpId": 1001,
            "agentName": "XX科技有限公司（更名）"
        }
        response = api_client.post("/api/v2/tax/withholding-agent/update", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="taxClassCode")

    @pytest.mark.P0
    @pytest.mark.反向
    def test_wa02_004_no_update_fields_fail(self, api_client):
        """WA02-004: 更新扣缴义务人-所有参数为空-失败"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC001"
        }
        response = api_client.post("/api/v2/tax/withholding-agent/update", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="没有可更新")

    @pytest.mark.P1
    @pytest.mark.正向
    def test_wa02_005_update_agentName_success(self, api_client):
        """WA02-005: 更新扣缴义务人-修改agentName-成功"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC001",
            "agentName": "XX科技有限公司（更名）"
        }
        response = api_client.post("/api/v2/tax/withholding-agent/update", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    @pytest.mark.正向
    def test_wa02_006_update_sbmm_success(self, api_client):
        """WA02-006: 更新扣缴义务人-修改sbmm-成功"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC001",
            "sbmm": "newPassword123"
        }
        response = api_client.post("/api/v2/tax/withholding-agent/update", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    @pytest.mark.正向
    def test_wa02_007_update_areaid_success(self, api_client):
        """WA02-007: 更新扣缴义务人-修改areaid-成功"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC001",
            "areaid": "320500"
        }
        response = api_client.post("/api/v2/tax/withholding-agent/update", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    @pytest.mark.边界值
    def test_wa02_008_sbmm_too_short_fail(self, api_client):
        """WA02-008: 更新扣缴义务人-sbmm长度不足8位-失败"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC001",
            "sbmm": "1234567"
        }
        response = api_client.post("/api/v2/tax/withholding-agent/update", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="sbmm")

    @pytest.mark.P1
    @pytest.mark.边界值
    def test_wa02_009_sbmm_too_long_fail(self, api_client):
        """WA02-009: 更新扣缴义务人-sbmm长度超过20位-失败"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC001",
            "sbmm": "123456789012345678901"
        }
        response = api_client.post("/api/v2/tax/withholding-agent/update", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="sbmm")

    @pytest.mark.P1
    @pytest.mark.反向
    def test_wa02_010_areaid_non_numeric_fail(self, api_client):
        """WA02-010: 更新扣缴义务人-areaid包含非数字-失败"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC001",
            "areaid": "31000A"
        }
        response = api_client.post("/api/v2/tax/withholding-agent/update", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="areaid")

    @pytest.mark.P1
    @pytest.mark.反向
    def test_wa02_011_nsrsbh_update_not_allowed_fail(self, api_client):
        """WA02-011: 更新扣缴义务人-nsrsbh尝试修改-失败"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC001",
            "nsrsbh": "91310000XXXXXXXX2K"
        }
        response = api_client.post("/api/v2/tax/withholding-agent/update", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="nsrsbh")

    @pytest.mark.P1
    @pytest.mark.反向
    def test_wa02_012_invalid_taxClassCode_fail(self, api_client):
        """WA02-012: 更新扣缴义务人-不存在的taxClassCode-失败"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "INVALID_TC",
            "agentName": "XX科技有限公司（更名）"
        }
        response = api_client.post("/api/v2/tax/withholding-agent/update", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="taxClassCode")


# ============================================================================
# WA03: 获取扣缴义务人详情
# ============================================================================

@pytest.mark.WA03
class TestWA03GetWithholdingAgentDetail:
    """获取扣缴义务人详情"""
    
    @pytest.mark.P0
    @pytest.mark.正向
    def test_wa03_001_get_detail_success(self, api_client):
        """WA03-001: 获取扣缴义务人详情-正常参数-成功"""
        request_data = {"cpId": 1001, "taxClassCode": "TC001"}
        response = api_client.post("/api/v2/tax/withholding-agent/detail", json_data=request_data)
        assert_response_success(response, expected_success=True)
        data = response.json()
        result = data.get("data", {})
        expected_fields = ["agentCode", "agentName", "nsrsbh", "areaid", "zgswjg"]
        for field in expected_fields:
            assert field in result

    @pytest.mark.P0
    @pytest.mark.反向
    def test_wa03_002_missing_cpId_fail(self, api_client):
        """WA03-002: 获取扣缴义务人详情-缺少cpId-失败"""
        request_data = {"taxClassCode": "TC001"}
        response = api_client.post("/api/v2/tax/withholding-agent/detail", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="cpId")

    @pytest.mark.P0
    @pytest.mark.反向
    def test_wa03_003_missing_taxClassCode_fail(self, api_client):
        """WA03-003: 获取扣缴义务人详情-缺少taxClassCode-失败"""
        request_data = {"cpId": 1001}
        response = api_client.post("/api/v2/tax/withholding-agent/detail", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="taxClassCode")

    @pytest.mark.P1
    @pytest.mark.反向
    def test_wa03_004_invalid_taxClassCode_fail(self, api_client):
        """WA03-004: 获取扣缴义务人详情-taxClassCode不存在-失败"""
        request_data = {"cpId": 1001, "taxClassCode": "INVALID_TC"}
        response = api_client.post("/api/v2/tax/withholding-agent/detail", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="不存在")

    @pytest.mark.P1
    @pytest.mark.正向
    def test_wa03_005_verify_complete_fields(self, api_client):
        """WA03-005: 获取扣缴义务人详情-验证返回完整字段-成功"""
        request_data = {"cpId": 1001, "taxClassCode": "TC001"}
        response = api_client.post("/api/v2/tax/withholding-agent/detail", json_data=request_data)
        assert_response_success(response, expected_success=True)
        data = response.json()
        result = data.get("data", {})
        expected_fields = ["agentCode", "agentName", "nsrsbh", "sbmm", "areaid", "djxhid", "zgswjg", "taxClassCode", "status"]
        for field in expected_fields:
            assert field in result


# ============================================================================
# WA04: 查询扣缴义务人列表
# ============================================================================

@pytest.mark.WA04
class TestWA04ListWithholdingAgent:
    """查询扣缴义务人列表"""
    
    @pytest.mark.P0
    @pytest.mark.正向
    def test_wa04_001_list_with_pagination_success(self, api_client):
        """WA04-001: 查询扣"""
        request_data = {
            "cpId": 1001,
            "pageNum": 1,
            "pageSize": 20
        }
        response = api_client.post("/api/v2/tax/withholding-agent/list", json_data=request_data)
        assert_response_success(response, expected_success=True)
        data = response.json()
        assert "data" in data

    @pytest.mark.P0
    @pytest.mark.反向
    def test_wa04_002_missing_cpId_fail(self, api_client):
        """WA04-002: 查询扣缴义务人列表-缺少cpId-失败"""
        request_data = {"pageNum": 1, "pageSize": 20}
        response = api_client.post("/api/v2/tax/withholding-agent/list", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="cpId")

    @pytest.mark.P1
    @pytest.mark.正向
    def test_wa04_003_list_no_filter_success(self, api_client):
        """WA04-003: 查询扣缴义务人列表-无筛选条件-成功"""
        request_data = {"cpId": 1001}
        response = api_client.post("/api/v2/tax/withholding-agent/list", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    @pytest.mark.正向
    def test_wa04_004_filter_by_nsrsbh_success(self, api_client):
        """WA04-004: 查询扣缴义务人列表-按nsrsbh精确查询-成功"""
        request_data = {"cpId": 1001, "nsrsbh": "91310000XXXXXXXX1K", "pageNum": 1, "pageSize": 20}
        response = api_client.post("/api/v2/tax/withholding-agent/list", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    @pytest.mark.正向
    def test_wa04_005_filter_by_agentName_success(self, api_client):
        """WA04-005: 查询扣缴义务人列表-按agentName模糊查询-成功"""
        request_data = {"cpId": 1001, "agentName": "科技", "pageNum": 1, "pageSize": 20}
        response = api_client.post("/api/v2/tax/withholding-agent/list", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    @pytest.mark.正向
    def test_wa04_006_filter_by_status_success(self, api_client):
        """WA04-006: 查询扣缴义务人列表-按status筛选-成功"""
        request_data = {"cpId": 1001, "status": "ACTIVE", "pageNum": 1, "pageSize": 20}
        response = api_client.post("/api/v2/tax/withholding-agent/list", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    @pytest.mark.分页
    def test_wa04_007_pagination_pageNum_success(self, api_client):
        """WA04-007: 查询扣缴义务人列表-分页pageNum-成功"""
        request_data = {"cpId": 1001, "pageNum": 2, "pageSize": 10}
        response = api_client.post("/api/v2/tax/withholding-agent/list", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    @pytest.mark.分页
    def test_wa04_008_pagination_pageSize_success(self, api_client):
        """WA04-008: 查询扣缴义务人列表-分页pageSize-成功"""
        request_data = {"cpId": 1001, "pageNum": 1, "pageSize": 50}
        response = api_client.post("/api/v2/tax/withholding-agent/list", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P2
    @pytest.mark.正向
    def test_wa04_009_empty_result_success(self, api_client):
        """WA04-009: 查询扣缴义务人列表-空结果-成功"""
        request_data = {"cpId": 9999, "pageNum": 1, "pageSize": 20}
        response = api_client.post("/api/v2/tax/withholding-agent/list", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    @pytest.mark.正向
    def test_wa04_010_verify_fields_complete(self, api_client):
        """WA04-010: 查询扣缴义务人列表-验证返回字段完整性-成功"""
        request_data = {"cpId": 1001, "pageNum": 1, "pageSize": 20}
        response = api_client.post("/api/v2/tax/withholding-agent/list", json_data=request_data)
        assert_response_success(response, expected_success=True)


# ============================================================================
# WA05: 搜索扣缴义务人
# ============================================================================

@pytest.mark.WA05
class TestWA05QueryWithholdingAgent:
    """搜索扣缴义务人"""
    
    @pytest.mark.P0
    @pytest.mark.正向
    def test_wa05_001_query_success(self, api_client):
        """WA05-001: 搜索扣缴义务人-正常参数-成功"""
        request_data = {"cpId": 1001, "keyword": "科技", "pageNum": 1, "pageSize": 20}
        response = api_client.post("/api/v2/tax/withholding-agent/query", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P0
    @pytest.mark.反向
    def test_wa05_002_missing_cpId_fail(self, api_client):
        """WA05-002: 搜索扣缴义务人-缺少cpId-失败"""
        request_data = {"keyword": "科技", "pageNum": 1, "pageSize": 20}
        response = api_client.post("/api/v2/tax/withholding-agent/query", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="cpId")

    @pytest.mark.P1
    @pytest.mark.正向
    def test_wa05_003_query_by_agentCode_success(self, api_client):
        """WA05-003: 搜索扣缴义务人-按agentCode模糊搜索-成功"""
        request_data = {"cpId": 1001, "keyword": "Agent", "pageNum": 1, "pageSize": 20}
        response = api_client.post("/api/v2/tax/withholding-agent/query", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    @pytest.mark.正向
    def test_wa05_004_query_by_agentName_success(self, api_client):
        """WA05-004: 搜索扣缴义务人-按agentName模糊搜索-成功"""
        request_data = {"cpId": 1001, "keyword": "有限", "pageNum": 1, "pageSize": 20}
        response = api_client.post("/api/v2/tax/withholding-agent/query", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    @pytest.mark.正向
    def test_wa05_005_query_by_nsrsbh_success(self, api_client):
        """WA05-005: 搜索扣缴义务人-按nsrsbh精确搜索-成功"""
        request_data = {"cpId": 1001, "keyword": "91310000XXXXXXXX1K", "pageNum": 1, "pageSize": 20}
        response = api_client.post("/api/v2/tax/withholding-agent/query", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    @pytest.mark.正向
    def test_wa05_006_query_multi_keywords_success(self, api_client):
        """WA05-006: 搜索扣缴义务人-多关键词搜索-成功"""
        request_data = {"cpId": 1001, "keyword": "Agent 科技", "pageNum": 1, "pageSize": 20}
        response = api_client.post("/api/v2/tax/withholding-agent/query", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    @pytest.mark.分页
    def test_wa05_007_query_pagination_success(self, api_client):
        """WA05-007: 搜索扣缴义务人-分页-成功"""
        request_data = {"cpId": 1001, "keyword": "科技", "pageNum": 1, "pageSize": 5}
        response = api_client.post("/api/v2/tax/withholding-agent/query", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P2
    @pytest.mark.正向
    def test_wa05_008_query_empty_result_success(self, api_client):
        """WA05-008: 搜索扣缴义务人-空结果-成功"""
        request_data = {"cpId": 1001, "keyword": "不存在的关键词XYZ", "pageNum": 1, "pageSize": 20}
        response = api_client.post("/api/v2/tax/withholding-agent/query", json_data=request_data)
        assert_response_success(response, expected_success=True)


# ============================================================================
# WA06: 删除扣缴义务人
# ============================================================================

@pytest.mark.WA06
class TestWA06DeleteWithholdingAgent:
    """删除扣缴义务人"""
    
    @pytest.mark.P0
    @pytest.mark.正向
    def test_wa06_001_delete_success(self, api_client):
        """WA06-001: 删除扣缴义务人-正常参数-成功"""
        request_data = {"cpId": 1001, "taxClassCode": "TC001"}
        response = api_client.post("/api/v2/tax/withholding-agent/delete", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P0
    @pytest.mark.反向
    def test_wa06_002_missing_cpId_fail(self, api_client):
        """WA06-002: 删除扣缴义务人-缺少cpId-失败"""
        request_data = {"taxClassCode": "TC001"}
        response = api_client.post("/api/v2/tax/withholding-agent/delete", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="cpId")

    @pytest.mark.P0
    @pytest.mark.反向
    def test_wa06_003_missing_taxClassCode_fail(self, api_client):
        """WA06-003: 删除扣缴义务人-缺少taxClassCode-失败"""
        request_data = {"cpId": 1001}
        response = api_client.post("/api/v2/tax/withholding-agent/delete", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="taxClassCode")

    @pytest.mark.P1
    @pytest.mark.反向
    def test_wa06_004_invalid_taxClassCode_fail(self, api_client):
        """WA06-004: 删除扣缴义务人-taxClassCode不存在-失败"""
        request_data = {"cpId": 1001, "taxClassCode": "INVALID_TC"}
        response = api_client.post("/api/v2/tax/withholding-agent/delete", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="不存在")

    @pytest.mark.P1
    @pytest.mark.幂等
    def test_wa06_005_duplicate_delete_success(self, api_client):
        """WA06-005: 删除扣缴义务人-重复删除-幂等"""
        request_data = {"cpId": 1001, "taxClassCode": "TC001"}
        response = api_client.post("/api/v2/tax/withholding-agent/delete", json_data=request_data)
        assert_response_success(response, expected_success=True)


# ============================================================================
# WA07: 获取报税地区列表
# ============================================================================

@pytest.mark.WA07
class TestWA07GetTaxRegions:
    """获取报税地区列表"""
    
    @pytest.mark.P0
    @pytest.mark.正向
    def test_wa07_001_get_regions_success(self, api_client):
        """WA07-001: 获取报税地区列表-正常参数-成功"""
        request_data = {"cpId": 1001}
        response = api_client.post("/api/v2/tax/withholding-agent/tax-regions", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P0
    @pytest.mark.反向
    def test_wa07_002_missing_cpId_fail(self, api_client):
        """WA07-002: 获取报税地区列表-缺少cpId-失败"""
        request_data = {}
        response = api_client.post("/api/v2/tax/withholding-agent/tax-regions", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="cpId")

    @pytest.mark.P1
    @pytest.mark.正向
    def test_wa07_003_verify_fields_success(self, api_client):
        """WA07-003: 获取报税地区列表-验证返回字段-成功"""
        request_data = {"cpId": 1001}
        response = api_client.post("/api/v2/tax/withholding-agent/tax-regions", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P2
    @pytest.mark.正向
    def test_wa07_004_empty_result_success(self, api_client):
        """WA07-004: 获取报税地区列表-空结果-成功"""
        request_data = {"cpId": 9999}
        response = api_client.post("/api/v2/tax/withholding-agent/tax-regions", json_data=request_data)
        assert_response_success(response, expected_success=True)


# ============================================================================
# WA08: 预获取税局任务ID
# ============================================================================

@pytest.mark.WA08
class TestWA08GetTaxAuthority:
    """预获取税局任务ID"""
    
    @pytest.mark.P0
    @pytest.mark.正向
    def test_wa08_001_get_authority_success(self, api_client):
        """WA08-001: 预获取税局任务ID-正常参数-成功"""
        request_data = {"cpId": 1001, "nsrsbh": "91310000XXXXXXXX1K", "sdyf": "202503"}
        response = api_client.post("/api/v2/tax/withholding-agent/tax-authority", json_data=request_data)
        assert_response_success(response, expected_success=True)
        data = response.json()
        assert "taxTaskId" in data.get("data", {})

    @pytest.mark.P0
    @pytest.mark.反向
    def test_wa08_002_missing_cpId_fail(self, api_client):
        """WA08-002: 预获取税局任务ID-缺少cpId-失败"""
        request_data = {"nsrsbh": "91310000XXXXXXXX1K", "sdyf": "202503"}
        response = api_client.post("/api/v2/tax/withholding-agent/tax-authority", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="cpId")

    @pytest.mark.P0
    @pytest.mark.反向
    def test_wa08_003_missing_nsrsbh_fail(self, api_client):
        """WA08-003: 预获取税局任务ID-缺少nsrsbh-失败"""
        request_data = {"cpId": 1001, "sdyf": "202503"}
        response = api_client.post("/api/v2/tax/withholding-agent/tax-authority", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="nsrsbh")

    @pytest.mark.P0
    @pytest.mark.反向
    def test_wa08_004_missing_sdyf_fail(self, api_client):
        """WA08-004: 预获取税局任务ID-缺少sdyf-失败"""
        request_data = {"cpId": 1001, "nsrsbh": "91310000XXXXXXXX1K"}
        response = api_client.post("/api/v2/tax/withholding-agent/tax-authority", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="sdyf")

    @pytest.mark.P1
    @pytest.mark.反向
    def test_wa08_005_sdyf_invalid_format_fail(self, api_client):
        """WA08-005: 预获取税局任务ID-sdyf格式错误-失败"""
        request_data = {"cpId": 1001, "nsrsbh": "91310000XXXXXXXX1K", "sdyf": "2025-03"}
        response = api_client.post("/api/v2/tax/withholding-agent/tax-authority", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="sdyf")

    @pytest.mark.P1
    @pytest.mark.正向
    def test_wa08_006_verify_taskId_success(self, api_client):
        """WA08-006: 预获取税局任务ID-验证返回taskId-成功"""
        request_data = {"cpId": 1001, "nsrsbh": "91310000XXXXXXXX1K", "sdyf": "202503"}
        response = api_client.post("/api/v2/tax/withholding-agent/tax-authority", json_data=request_data)
        assert_response_success(response, expected_success=True)
        data = response.json()
        assert data.get("data", {}).get("taxTaskId")


# ============================================================================
# WA09: 根据任务ID查询税务机关
# ============================================================================

@pytest.mark.WA09
class TestWA09GetTaxAuthorityByTaskId:
    """根据任务ID查询税务机关"""
    
    @pytest.mark.P0
    @pytest.mark.正向
    def test_wa09_001_get_authority_by_taskId_success(self, api_client):
        """WA09-001: 根据任务ID查询税务机关-正常参数-成功"""
        request_data = {"taxTaskId": "TASK20250301001"}
        response = api_client.post("/api/v2/tax/withholding-agent/tax-authority-by-taskId", json_data=request_data)
        assert_response_success(response, expected_success=True)
        data = response.json()
        result = data.get("data", {})
        assert "zgswjg" in result or "djxh" in result

    @pytest.mark.P0
    @pytest.mark.反向
    def test_wa09_002_missing_taxTaskId_fail(self, api_client):
        """WA09-002: 根据任务ID查询税务机关-缺少taxTaskId-失败"""
        request_data = {}
        response = api_client.post("/api/v2/tax/withholding-agent/tax-authority-by-taskId", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="taxTaskId")

    @pytest.mark.P1
    @pytest.mark.反向
    def test_wa09_003_invalid_taxTaskId_fail(self, api_client):
        """WA09-003: 根据任务ID查询税务机关-taxTaskId不存在-失败"""
        request_data = {"taxTaskId": "INVALID_TASK"}
        response = api_client.post("/api/v2/tax/withholding-agent/tax-authority-by-taskId", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="不存在")

    @pytest.mark.P1
    @pytest.mark.正向
    def test_wa09_004_verify_fields_success(self, api_client):
        """WA09-004: 根据任务ID查询税务机关-验证返回税务机关信息-成功"""
        request_data = {"taxTaskId": "TASK20250301001"}
        response = api_client.post("/api/v2/tax/withholding-agent/tax-authority-by-taskId", json_data=request_data)
        assert_response_success(response, expected_success=True)
        data = response.json()
        assert "zgswjg" in data.get("data", {})


# ============================================================================
# WA: 鉴权测试
# ============================================================================

@pytest.mark.WA
@pytest.mark.鉴权
class TestWAAuthentication:
    """扣缴义务人模块 - 鉴权测试"""
    
    def test_wa_auth_no_token_fail(self, api_client):
        """WA-AUTH-001: 所有接口-无token访问-失败"""
        from tests.conftest import APIClient
        temp_client = APIClient(api_client.base_url, {})
        request_data = {"cpId": 1001}
        response = temp_client.post("/api/v2/tax/withholding-agent/list", json_data=request_data)
        assert response.status_code == 401

    def test_wa_auth_invalid_token_fail(self, api_client):
        """WA-AUTH-002: 所有接口-token无效-失败"""
        from tests.conftest import APIClient
        temp_client = APIClient(api_client.base_url, {"Authorization": "Bearer invalid_token"})
        request_data = {"cpId": 1001}
        response = temp_client.post("/api/v2/tax/withholding-agent/list", json_data=request_data)
        assert response.status_code == 401

    def test_wa_auth_expired_token_fail(self, api_client):
        """WA-AUTH-003: 所有接口-token过期-失败"""
        from tests.conftest import APIClient
        temp_client = APIClient(api_client.base_url, {"Authorization": "Bearer expired_token"})
        request_data = {"cpId": 1001}
        response = temp_client.post("/api/v2/tax/withholding-agent/list", json_data=request_data)
        assert response.status_code == 401
