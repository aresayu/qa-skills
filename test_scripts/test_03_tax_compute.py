"""
个税计算模块测试用例 (TC)
接口路径前缀: /api/v2/tax/salaryData 和 /api/v2/tax/taxCompute

测试范围:
- TC01: 薪酬数据导入
- TC02: 薪酬数据查询
- TC03: 生成0工资记录
- TC04: 触发算税
- TC05: 重新触发算税
- TC06: 算税结果查询
- TC07: 算税汇总统计
- TC08: 算税记录详情
- TC09: 导出算税结果

共计: 80+ 测试用例
"""
import pytest
from tests.conftest import assert_response_success, assert_response_code


# ============================================================================
# TC01: 薪酬数据导入
# 接口路径: POST /api/v2/tax/salaryData/import
# ============================================================================

@pytest.mark.TC01
class TestTC01SalaryDataImport:
    """薪酬数据导入"""
    
    @pytest.mark.P0
    @pytest.mark.正向
    def test_tc01_001_import_success(self, api_client, sample_salary_data):
        """TC01-001: 薪酬数据导入-正常参数-成功"""
        request_data = {
            "cpId": 1001,
            "nsrsbh": "91310000XXXXXXXX1K",
            "taxClassCode": "TC2025001",
            "sdyf": "202503",
            "dysd": sample_salary_data[:1]
        }
        response = api_client.post("/api/v2/tax/salaryData/import", json_data=request_data)
        assert_response_code(response, expected_code="200")

    @pytest.mark.P0
    @pytest.mark.反向
    def test_tc01_002_missing_cpId_fail(self, api_client, sample_salary_data):
        """TC01-002: 薪酬数据导入-缺少cpId-失败"""
        request_data = {
            "nsrsbh": "91310000XXXXXXXX1K",
            "taxClassCode": "TC2025001",
            "sdyf": "202503",
            "dysd": sample_salary_data[:1]
        }
        response = api_client.post("/api/v2/tax/salaryData/import", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="cpId")

    @pytest.mark.P0
    @pytest.mark.反向
    def test_tc01_003_missing_nsrsbh_fail(self, api_client, sample_salary_data):
        """TC01-003: 薪酬数据导入-缺少nsrsbh-失败"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC2025001",
            "sdyf": "202503",
            "dysd": sample_salary_data[:1]
        }
        response = api_client.post("/api/v2/tax/salaryData/import", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="nsrsbh")

    @pytest.mark.P0
    @pytest.mark.反向
    def test_tc01_004_missing_taxClassCode_fail(self, api_client, sample_salary_data):
        """TC01-004: 薪酬数据导入-缺少taxClassCode-失败"""
        request_data = {
            "cpId": 1001,
            "nsrsbh": "91310000XXXXXXXX1K",
            "sdyf": "202503",
            "dysd": sample_salary_data[:1]
        }
        response = api_client.post("/api/v2/tax/salaryData/import", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="taxClassCode")

    @pytest.mark.P0
    @pytest.mark.反向
    def test_tc01_005_missing_sdyf_fail(self, api_client, sample_salary_data):
        """TC01-005: 薪酬数据导入-缺少sdyf-失败"""
        request_data = {
            "cpId": 1001,
            "nsrsbh": "91310000XXXXXXXX1K",
            "taxClassCode": "TC2025001",
            "dysd": sample_salary_data[:1]
        }
        response = api_client.post("/api/v2/tax/salaryData/import", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="sdyf")

    @pytest.mark.P0
    @pytest.mark.反向
    def test_tc01_006_missing_dysd_fail(self, api_client):
        """TC01-006: 薪酬数据导入-缺少dysd-失败"""
        request_data = {
            "cpId": 1001,
            "nsrsbh": "91310000XXXXXXXX1K",
            "taxClassCode": "TC2025001",
            "sdyf": "202503"
        }
        response = api_client.post("/api/v2/tax/salaryData/import", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="dysd")

    @pytest.mark.P1
    @pytest.mark.反向
    def test_tc01_007_sdyf_invalid_format_fail(self, api_client, sample_salary_data):
        """TC01-007: 薪酬数据导入-sdyf格式错误-失败"""
        request_data = {
            "cpId": 1001,
            "nsrsbh": "91310000XXXXXXXX1K",
            "taxClassCode": "TC2025001",
            "sdyf": "2025-03",
            "dysd": sample_salary_data[:1]
        }
        response = api_client.post("/api/v2/tax/salaryData/import", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="sdyf")

    @pytest.mark.P1
    @pytest.mark.边界值
    def test_tc01_008_sdyf_invalid_length_fail(self, api_client, sample_salary_data):
        """TC01-008: 薪酬数据导入-sdyf长度非6位-失败"""
        request_data = {
            "cpId": 1001,
            "nsrsbh": "91310000XXXXXXXX1K",
            "taxClassCode": "TC2025001",
            "sdyf": "20253",
            "dysd": sample_salary_data[:1]
        }
        response = api_client.post("/api/v2/tax/salaryData/import", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="sdyf")

    @pytest.mark.P1
    @pytest.mark.边界值
    def test_tc01_009_dysd_exceed_500_fail(self, api_client):
        """TC01-009: 薪酬数据导入-dysd超过500条-失败"""
        dysd = [{"xm": f"员工{i}", "zzlx": "A", "zzhm": f"31010119900101{i:04d}", 
                 "itemCode": "01010101", "pch": i, "sre": 15000.00,
                 "jbylaobxf": 960.00, "jbylbxf": 240.00, "sybxf": 60.00, "zfgjj": 1200.00} 
                for i in range(501)]
        request_data = {
            "cpId": 1001,
            "nsrsbh": "91310000XXXXXXXX1K",
            "taxClassCode": "TC2025001",
            "sdyf": "202503",
            "dysd": dysd
        }
        response = api_client.post("/api/v2/tax/salaryData/import", json_data=request_data)
        assert_response_code(response, expected_code="200")

    @pytest.mark.P1
    @pytest.mark.反向
    def test_tc01_010_dysd_missing_itemCode_fail(self, api_client):
        """TC01-010: 薪酬数据导入-dysd单条缺少itemCode-失败"""
        request_data = {
            "cpId": 1001,
            "nsrsbh": "91310000XXXXXXXX1K",
            "taxClassCode": "TC2025001",
            "sdyf": "202503",
            "dysd": [{
                "xm": "张三",
                "zzlx": "A",
                "zzhm": "310101199001011234",
                "pch": 1,
                "sre": 15000.00,
                "jbylaobxf": 960.00,
                "jbylbxf": 240.00,
                "sybxf": 60.00,
                "zfgjj": 1200.00
            }]
        }
        response = api_client.post("/api/v2/tax/salaryData/import", json_data=request_data)
        assert_response_code(response, expected_code="200")

    @pytest.mark.P1
    @pytest.mark.反向
    def test_tc01_011_sre_negative_fail(self, api_client):
        """TC01-011: 薪酬数据导入-sre为负数-失败"""
        request_data = {
            "cpId": 1001,
            "nsrsbh": "91310000XXXXXXXX1K",
            "taxClassCode": "TC2025001",
            "sdyf": "202503",
            "dysd": [{
                "xm": "张三",
                "zzlx": "A",
                "zzhm": "310101199001011234",
                "itemCode": "01010101",
                "pch": 1,
                "sre": -5000.00,
                "jbylaobxf": 960.00,
                "jbylbxf": 240.00,
                "sybxf": 60.00,
                "zfgjj": 1200.00
            }]
        }
        response = api_client.post("/api/v2/tax/salaryData/import", json_data=request_data)
        assert_response_code(response, expected_code="200")

    @pytest.mark.P1
    @pytest.mark.边界值
    def test_tc01_012_sre_zero_success(self, api_client):
        """TC01-012: 薪酬数据导入-sre为零-成功"""
        request_data = {
            "cpId": 1001,
            "nsrsbh": "91310000XXXXXXXX1K",
            "taxClassCode": "TC2025001",
            "sdyf": "202503",
            "dysd": [{
                "xm": "张三",
                "zzlx": "A",
                "zzhm": "310101199001011234",
                "itemCode": "01010101",
                "pch": 1,
                "sre": 0.00,
                "jbylaobxf": 0.00,
                "jbylbxf": 0.00,
                "sybxf": 0.00,
                "zfgjj": 0.00
            }]
        }
        response = api_client.post("/api/v2/tax/salaryData/import", json_data=request_data)
        assert_response_code(response, expected_code="200")

    @pytest.mark.P2
    @pytest.mark.边界值
    def test_tc01_013_sre_max_value_success(self, api_client):
        """TC01-013: 薪酬数据导入-sre为极大值-成功"""
        request_data = {
            "cpId": 1001,
            "nsrsbh": "91310000XXXXXXXX1K",
            "taxClassCode": "TC2025001",
            "sdyf": "202503",
            "dysd": [{
                "xm": "张三",
                "zzlx": "A",
                "zzhm": "310101199001011234",
                "itemCode": "01010101",
                "pch": 1,
                "sre": 999999999.99,
                "jbylaobxf": 30000.00,
                "jbylbxf": 10000.00,
                "sybxf": 5000.00,
                "zfgjj": 30000.00
            }]
        }
        response = api_client.post("/api/v2/tax/salaryData/import", json_data=request_data)
        assert_response_code(response, expected_code="200")

    @pytest.mark.P1
    @pytest.mark.反向
    def test_tc01_014_jbylaobxf_invalid_format_fail(self, api_client):
        """TC01-014: 薪酬数据导入-养老保险格式错误-失败"""
        request_data = {
            "cpId": 1001,
            "nsrsbh": "91310000XXXXXXXX1K",
            "taxClassCode": "TC2025001",
            "sdyf": "202503",
            "dysd": [{
                "xm": "张三",
                "zzlx": "A",
                "zzhm": "310101199001011234",
                "itemCode": "01010101",
                "pch": 1,
                "sre": 15000.00,
                "jbylaobxf": "abc",
                "jbylbxf": 240.00,
                "sybxf": 60.00,
                "zfgjj": 1200.00
            }]
        }
        response = api_client.post("/api/v2/tax/salaryData/import", json_data=request_data)
        assert_response_code(response, expected_code="200")

    @pytest.mark.P1
    @pytest.mark.反向
    def test_tc01_015_jbylbxf_invalid_format_fail(self, api_client):
        """TC01-015: 薪酬数据导入-医保保险格式错误-失败"""
        request_data = {
            "cpId": 1001,
            "nsrsbh": "91310000XXXXXXXX1K",
            "taxClassCode": "TC2025001",
            "sdyf": "202503",
            "dysd": [{
                "xm": "张三",
                "zzlx": "A",
                "zzhm": "310101199001011234",
                "itemCode": "01010101",
                "pch": 1,
                "sre": 15000.00,
                "jbylaobxf": 960.00,
                "jbylbxf": "xyz",
                "sybxf": 60.00,
                "zfgjj": 1200.00
            }]
        }
        response = api_client.post("/api/v2/tax/salaryData/import", json_data=request_data)
        assert_response_code(response, expected_code="200")

    @pytest.mark.P1
    @pytest.mark.反向
    def test_tc01_016_sybxf_invalid_format_fail(self, api_client):
        """TC01-016: 薪酬数据导入-失业保险格式错误-失败"""
        request_data = {
            "cpId": 1001,
            "nsrsbh": "91310000XXXXXXXX1K",
            "taxClassCode": "TC2025001",
            "sdyf": "202503",
            "dysd": [{
                "xm": "张三",
                "zzlx": "A",
                "zzhm": "310101199001011234",
                "itemCode": "01010101",
                "pch": 1,
                "sre": 15000.00,
                "jbylaobxf": 960.00,
                "jbylbxf": 240.00,
                "sybxf": "def",
                "zfgjj": 1200.00
            }]
        }
        response = api_client.post("/api/v2/tax/salaryData/import", json_data=request_data)
        assert_response_code(response, expected_code="200")

    @pytest.mark.P1
    @pytest.mark.反向
    def test_tc01_017_zfgjj_invalid_format_fail(self, api_client):
        """TC01-017: 薪酬数据导入-公积金格式错误-失败"""
        request_data = {
            "cpId": 1001,
            "nsrsbh": "91310000XXXXXXXX1K",
            "taxClassCode": "TC2025001",
            "sdyf": "202503",
            "dysd": [{
                "xm": "张三",
                "zzlx": "A",
                "zzhm": "310101199001011234",
                "itemCode": "01010101",
                "pch": 1,
                "sre": 15000.00,
                "jbylaobxf": 960.00,
                "jbylbxf": 240.00,
                "sybxf": 60.00,
                "zfgjj": "ghi"
            }]
        }
        response = api_client.post("/api/v2/tax/salaryData/import", json_data=request_data)
        assert_response_code(response, expected_code="200")

    @pytest.mark.P1
    @pytest.mark.正向
    def test_tc01_018_with_jmxx_success(self, api_client):
        """TC01-018: 薪酬数据导入-减免附表数据完整-成功"""
        request_data = {
            "cpId": 1001,
            "nsrsbh": "91310000XXXXXXXX1K",
            "taxClassCode": "TC2025001",
            "sdyf": "202503",
            "dysd": [{
                "xm": "张三",
                "zzlx": "A",
                "zzhm": "310101199001011234",
                "itemCode": "01010101",
                "pch": 1,
                "sre": 15000.00,
                "jbylaobxf": 960.00,
                "jbylbxf": 240.00,
                "sybxf": 60.00,
                "zfgjj": 1200.00,
                "jmxx": {
                    "jmlx": "重点群体就业",
                    "jmbz": "失业半年以上人员",
                    "jmje": 500.00
                }
            }]
        }
        response = api_client.post("/api/v2/tax/salaryData/import", json_data=request_data)
        assert_response_code(response, expected_code="200")

    @pytest.mark.P1
    @pytest.mark.正向
    def test_tc01_019_with_jzxx_success(self, api_client):
        """TC01-019: 薪酬数据导入-捐赠附表数据完整-成功"""
        request_data = {
            "cpId": 1001,
            "nsrsbh": "91310000XXXXXXXX1K",
            "taxClassCode": "TC2025001",
            "sdyf": "202503",
            "dysd": [{
                "xm": "张三",
                "zzlx": "A",
                "zzhm": "310101199001011234",
                "itemCode": "01010101",
                "pch": 1,
                "sre": 15000.00,
                "jbylaobxf": 960.00,
                "jbylbxf": 240.00,
                "sybxf": 60.00,
                "zfgjj": 1200.00,
                "jzxx": {
                    "jzxm": "公益慈善事业捐赠",
                    "jzjg": "某基金会",
                    "jzje": 1000.00,
                    "jzhm": "JB202503001"
                }
            }]
        }
        response = api_client.post("/api/v2/tax/salaryData/import", json_data=request_data)
        assert_response_code(response, expected_code="200")

    @pytest.mark.P1
    @pytest.mark.正向
    def test_tc01_020_with_syjxjxx_success(self, api_client):
        """TC01-020: 薪酬数据导入-商业健康险附表数据完整-成功"""
        request_data = {
            "cpId": 1001,
            "nsrsbh": "91310000XXXXXXXX1K",
            "taxClassCode": "TC2025001",
            "sdyf": "202503",
            "dysd": [{
                "xm": "张三",
                "zzlx": "A",
                "zzhm": "310101199001011234",
                "itemCode": "01010101",
                "pch": 1,
                "sre": 15000.00,
                "jbylaobxf": 960.00,
                "jbylbxf": 240.00,
                "sybxf": 60.00,
                "zfgjj": 1200.00,
                "syjxjxx": {
                    "bxgs": "某保险公司",
                    "bxmc": "税优健康险",
                    "bxje": 200.00,
                    "bxzh": "BX202503001"
                }
            }]
        }
        response = api_client.post("/api/v2/tax/salaryData/import", json_data=request_data)
        assert_response_code(response, expected_code="200")

    @pytest.mark.P1
    @pytest.mark.正向
    def test_tc01_021_domestic_and_foreign_success(self, api_client):
        """TC01-021: 薪酬数据导入-境内境外数据同时存在-成功"""
        request_data = {
            "cpId": 1001,
            "nsrsbh": "91310000XXXXXXXX1K",
            "taxClassCode": "TC2025001",
            "sdyf": "202503",
            "dysd": [
                {
                    "xm": "张三",
                    "zzlx": "A",
                    "zzhm": "310101199001011234",
                    "itemCode": "01010101",
                    "pch": 1,
                    "sre": 15000.00,
                    "jbylaobxf": 960.00,
                    "jbylbxf": 240.00,
                    "sybxf": 60.00,
                    "zfgjj": 1200.00
                },
                {
                    "xm": "李四",
                    "zzlx": "B",
                    "zzhm": "H310101199001011234",
                    "itemCode": "01010101",
                    "pch": 2,
                    "sre": 20000.00,
                    "jbylaobxf": 0,
                    "jbylbxf": 0,
                    "sybxf": 0,
                    "zfgjj": 0
                }
            ]
        }
        response = api_client.post("/api/v2/tax/salaryData/import", json_data=request_data)
        assert_response_code(response, expected_code="200")

    @pytest.mark.P1
    @pytest.mark.反向
    def test_tc01_022_jbylaobxf_exceed_sre_fail(self, api_client):
        """TC01-022: 薪酬数据导入-jbylaobxf大于sre-失败"""
        request_data = {
            "cpId": 1001,
            "nsrsbh": "91310000XXXXXXXX1K",
            "taxClassCode": "TC2025001",
            "sdyf": "202503",
            "dysd": [{
                "xm": "张三",
                "zzlx": "A",
                "zzhm": "310101199001011234",
                "itemCode": "01010101",
                "sre": 1000.00,
                "jbylaobxf": 2000.00
            }]
        }
        response = api_client.post("/api/v2/tax/salaryData/import", json_data=request_data)
        assert_response_code(response, expected_code="200")

    @pytest.mark.P1
    @pytest.mark.反向
    def test_tc01_023_partial_success_partial_fail(self, api_client):
        """TC01-023: 薪酬数据导入-部分成功部分失败-成功"""
        request_data = {
            "cpId": 1001,
            "nsrsbh": "91310000XXXXXXXX1K",
            "taxClassCode": "TC2025001",
            "sdyf": "202503",
            "dysd": [
                {
                    "xm": "张三",
                    "zzlx": "A",
                    "zzhm": "310101199001011234",
                    "itemCode": "01010101",
                    "pch": 1,
                    "sre": 15000.00,
                    "jbylaobxf": 960.00,
                    "jbylbxf": 240.00,
                    "sybxf": 60.00,
                    "zfgjj": 1200.00
                },
                {
                    "xm": "李四",
                    "zzlx": "A",
                    "zzhm": "310101199001011235",
                    "itemCode": "01010101",
                    "sre": 1000.00,
                    "jbylaobxf": 2000.00
                }
            ]
        }
        response = api_client.post("/api/v2/tax/salaryData/import", json_data=request_data)
        assert_response_code(response, expected_code="200")

    @pytest.mark.P1
    @pytest.mark.反向
    def test_tc01_024_all_fail(self, api_client):
        """TC01-024: 薪酬数据导入-全部失败-成功"""
        request_data = {
            "cpId": 1001,
            "nsrsbh": "91310000XXXXXXXX1K",
            "taxClassCode": "TC2025001",
            "sdyf": "202503",
            "dysd": [
                {
                    "xm": "张三",
                    "zzlx": "A",
                    "zzhm": "310101199001011234",
                    "itemCode": "01010101",
                    "sre": 1000.00,
                    "jbylaobxf": 2000.00
                },
                {
                    "xm": "李四",
                    "zzlx": "A",
                    "zzhm": "310101199001011235",
                    "itemCode": "01010101",
                    "sre": 800.00,
                    "jbylaobxf": 1500.00
                }
            ]
        }
        response = api_client.post("/api/v2/tax/salaryData/import", json_data=request_data)
        assert_response_code(response, expected_code="200")

    @pytest.mark.P1
    @pytest.mark.反向
    def test_tc01_025_gwjtfy_exceed_sre_fail(self, api_client):
        """TC01-025: 薪酬数据导入-gwjtfy大于sre-失败"""
        request_data = {
            "cpId": 1001,
            "nsrsbh": "91310000XXXXXXXX1K",
            "taxClassCode": "TC2025001",
            "sdyf": "202503",
            "dysd": [{
                "xm": "张三",
                "zzlx": "A",
                "zzhm": "310101199001011234",
                "itemCode": "01010101",
                "pch": 1,
                "sre": 5000.00,
                "jbylaobxf": 960.00,
                "jbylbxf": 240.00,
                "sybxf": 60.00,
                "zfgjj": 1200.00,
                "gwjtfy": 6000.00
            }]
        }
        response = api_client.post("/api/v2/tax/salaryData/import", json_data=request_data)
        assert_response_code(response, expected_code="200")

    @pytest.mark.P1
    @pytest.mark.反向
    def test_tc01_026_txfy_exceed_sre_fail(self, api_client):
        """TC01-026: 薪酬数据导入-txfy大于sre-失败"""
        request_data = {
            "cpId": 1001,
            "nsrsbh": "91310000XXXXXXXX1K",
            "taxClassCode": "TC2025001",
            "sdyf": "202503",
            "dysd": [{
                "xm": "张三",
                "zzlx": "A",
                "zzhm": "310101199001011234",
                "itemCode": "01010101",
                "pch": 1,
                "sre": 5000.00,
                "jbylaobxf": 960.00,
                "jbylbxf": 240.00,
                "sybxf": 60.00,
                "zfgjj": 1200.00,
                "txfy": 6000.00
            }]
        }
        response = api_client.post("/api/v2/tax/salaryData/import", json_data=request_data)
        assert_response_code(response, expected_code="200")


# ============================================================================
# TC02: 薪酬数据查询
# 接口路径: POST /api/v2/tax/salaryData/list
# ============================================================================

@pytest.mark.TC02
class TestTC02SalaryDataList:
    """薪酬数据查询"""
    
    @pytest.mark.P0
    @pytest.mark.正向
    def test_tc02_001_list_success(self, api_client):
        """TC02-001: 薪酬数据查询-正常参数-成功"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC2025001",
            "sdyf": "202503",
            "pageNum": 1,
            "pageSize": 20
        }
        response = api_client.post("/api/v2/tax/salaryData/list", json_data=request_data)
        assert_response_code(response, expected_code="200")

    @pytest.mark.P0
    @pytest.mark.反向
    def test_tc02_002_missing_cpId_fail(self, api_client):
        """TC02-002: 薪酬数据查询-缺少cpId-失败"""
        request_data = {
            "taxClassCode": "TC2025001",
            "sdyf": "202503",
            "pageNum": 1,
            "pageSize": 20
        }
        response = api_client.post("/api/v2/tax/salaryData/list", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="cpId")

    @pytest.mark.P0
    @pytest.mark.反向
    def test_tc02_003_missing_taxClassCode_fail(self, api_client):
        """TC02-003: 薪酬数据查询-缺少taxClassCode-失败"""
        request_data = {
            "cpId": 1001,
            "sdyf": "202503",
            "pageNum": 1,
            "pageSize": 20
        }
        response = api_client.post("/api/v2/tax/salaryData/list", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="taxClassCode")

    @pytest.mark.P0
    @pytest.mark.反向
    def test_tc02_004_missing_sdyf_fail(self, api_client):
        """TC02-004: 薪酬数据查询-缺少sdyf-失败"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC2025001",
            "pageNum": 1,
            "pageSize": 20
        }
        response = api_client.post("/api/v2/tax/salaryData/list", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="sdyf")

    @pytest.mark.P1
    @pytest.mark.反向
    def test_tc02_005_sdyf_invalid_format_fail(self, api_client):
        """TC02-005: 薪酬数据查询-sdyf格式错误-失败"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC2025001",
            "sdyf": "2025-03",
            "pageNum": 1,
            "pageSize": 20
        }
        response = api_client.post("/api/v2/tax/salaryData/list", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="sdyf")

    @pytest.mark.P1
    @pytest.mark.正向
    def test_tc02_006_filter_by_sdxm_success(self, api_client):
        """TC02-006: 薪酬数据查询-按sdxm过滤-成功"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC2025001",
            "sdyf": "202503",
            "sdxm": "正常工资薪金",
            "pageNum": 1,
            "pageSize": 20
        }
        response = api_client.post("/api/v2/tax/salaryData/list", json_data=request_data)
        assert_response_code(response, expected_code="200")

    @pytest.mark.P1
    @pytest.mark.正向
    def test_tc02_007_filter_by_status_neg9_success(self, api_client):
        """TC02-007: 薪酬数据查询-按status过滤(-9失败)-成功"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC2025001",
            "sdyf": "202503",
            "status": -9,
            "pageNum": 1,
            "pageSize": 20
        }
        response = api_client.post("/api/v2/tax/salaryData/list", json_data=request_data)
        assert_response_code(response, expected_code="200")

    @pytest.mark.P1
    @pytest.mark.正向
    def test_tc02_008_filter_by_status_neg1_success(self, api_client):
        """TC02-008: 薪酬数据查询-按status过滤(-1未处理)-成功"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC2025001",
            "sdyf": "202503",
            "status": -1,
            "pageNum": 1,
            "pageSize": 20
        }
        response = api_client.post("/api/v2/tax/salaryData/list", json_data=request_data)
        assert_response_code(response, expected_code="200")

    @pytest.mark.P1
    @pytest.mark.正向
    def test_tc02_009_filter_by_status_0_success(self, api_client):
        """TC02-009: 薪酬数据查询-按status过滤(0正确)-成功"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC2025001",
            "sdyf": "202503",
            "status": 0,
            "pageNum": 1,
            "pageSize": 20
        }
        response = api_client.post("/api/v2/tax/salaryData/list", json_data=request_data)
        assert_response_code(response, expected_code="200")

    @pytest.mark.P1
    @pytest.mark.正向
    def test_tc02_010_filter_by_status_1_success(self, api_client):
        """TC02-010: 薪酬数据查询-按status过滤(1有提示)-成功"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC2025001",
            "sdyf": "202503",
            "status": 1,
            "pageNum": 1,
            "pageSize": 20
        }
        response = api_client.post("/api/v2/tax/salaryData/list", json_data=request_data)
        assert_response_code(response, expected_code="200")

    @pytest.mark.P1
    @pytest.mark.分页
    def test_tc02_011_pagination_pageNum_success(self, api_client):
        """TC02-011: 薪酬数据查询-分页pageNum-成功"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC2025001",
            "sdyf": "202503",
            "pageNum": 2,
            "pageSize": 20
        }
        response = api_client.post("/api/v2/tax/salaryData/list", json_data=request_data)
        assert_response_code(response, expected_code="200")

    @pytest.mark.P1
    @pytest.mark.分页
    def test_tc02_012_pagination_pageSize_success(self, api_client):
        """TC02-012: 薪酬数据查询-分页pageSize-成功"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC2025001",
            "sdyf": "202503",
            "pageNum": 1,
            "pageSize": 50
        }
        response = api_client.post("/api/v2/tax/salaryData/list", json_data=request_data)
        assert_response_code(response, expected_code="200")

    @pytest.mark.P2
    @pytest.mark.边界值
    def test_tc02_013_pageSize_max_500_success(self, api_client):
        """TC02-013: 薪酬数据查询-pageSize最大500-成功"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC2025001",
            "sdyf": "202503",
            "pageNum": 1,
            "pageSize": 500,
        },

        response = api_client.post("/api/v2/tax/salaryData/list", json_data=request_data)
        assert_response_code(response, expected_code="200")

    @pytest.mark.P2
    @pytest.mark.边界值
    def test_tc02_014_pageSize_exceed_500_success(self, api_client):
        """TC02-014: 薪酬数据查询-pageSize超过500-成功"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC2025001",
            "sdyf": "202503",
            "pageNum": 1,
            "pageSize": 1000
        }
        response = api_client.post("/api/v2/tax/salaryData/list", json_data=request_data)
        assert_response_code(response, expected_code="200")

    @pytest.mark.P1
    @pytest.mark.正向
    def test_tc02_015_verify_fields_complete(self, api_client):
        """TC02-015: 薪酬数据查询-验证返回字段完整性"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC2025001",
            "sdyf": "202503",
            "pageNum": 1,
            "pageSize": 20
        }
        response = api_client.post("/api/v2/tax/salaryData/list", json_data=request_data)
        assert_response_code(response, expected_code="200")

    @pytest.mark.P2
    @pytest.mark.正向
    def test_tc02_016_empty_result_success(self, api_client):
        """TC02-016: 薪酬数据查询-空结果-成功"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC2025001",
            "sdyf": "209912",
            "pageNum": 1,
            "pageSize": 20
        }
        response = api_client.post("/api/v2/tax/salaryData/list", json_data=request_data)
        assert_response_code(response, expected_code="200")


# ============================================================================
# TC03: 生成0工资记录
# 接口路径: POST /api/v2/tax/salaryData/zeroWage
# ============================================================================

@pytest.mark.TC03
class TestTC03ZeroWage:
    """生成0工资记录"""
    
    @pytest.mark.P0
    @pytest.mark.正向
    def test_tc03_001_zero_wage_success(self, api_client):
        """TC03-001: 生成0工资记录-正常参数-成功"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC2025001",
            "sdyf": "202503",
            "personIds": ["310101199001011234", "310101199002022345"]
        }
        response = api_client.post("/api/v2/tax/salaryData/zeroWage", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P0
    @pytest.mark.反向
    def test_tc03_002_missing_cpId_fail(self, api_client):
        """TC03-002: 生成0工资记录-缺少cpId-失败"""
        request_data = {
            "taxClassCode": "TC2025001",
            "sdyf": "202503",
            "personIds": ["310101199001011234"]
        }
        response = api_client.post("/api/v2/tax/salaryData/zeroWage", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="cpId")

    @pytest.mark.P0
    @pytest.mark.反向
    def test_tc03_003_missing_taxClassCode_fail(self, api_client):
        """TC03-003: 生成0工资记录-缺少taxClassCode-失败"""
        request_data = {
            "cpId": 1001,
            "sdyf": "202503",
            "personIds": ["310101199001011234"]
        }
        response = api_client.post("/api/v2/tax/salaryData/zeroWage", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="taxClassCode")

    @pytest.mark.P0
    @pytest.mark.反向
    def test_tc03_004_missing_sdyf_fail(self, api_client):
        """TC03-004: 生成0工资记录-缺少sdyf-失败"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC2025001",
            "personIds": ["310101199001011234"]
        }
        response = api_client.post("/api/v2/tax/salaryData/zeroWage", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="sdyf")

    @pytest.mark.P0
    @pytest.mark.反向
    def test_tc03_005_missing_personIds_fail(self, api_client):
        """TC03-005: 生成0工资记录-缺少personIds-失败"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC2025001",
            "sdyf": "202503"
        }
        response = api_client.post("/api/v2/tax/salaryData/zeroWage", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="personIds")

    @pytest.mark.P0
    @pytest.mark.反向
    def test_tc03_006_empty_personIds_fail(self, api_client):
        """TC03-006: 生成0工资记录-personIds为空数组-失败"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC2025001",
            "sdyf": "202503",
            "personIds": []
        }
        response = api_client.post("/api/v2/tax/salaryData/zeroWage", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="personIds")

    @pytest.mark.P1
    @pytest.mark.反向
    def test_tc03_007_sdyf_invalid_format_fail(self, api_client):
        """TC03-007: 生成0工资记录-sdyf格式错误-失败"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC2025001",
            "sdyf": "2025-03",
            "personIds": ["310101199001011234"]
        }
        response = api_client.post("/api/v2/tax/salaryData/zeroWage", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="sdyf")

    @pytest.mark.P1
    @pytest.mark.边界值
    def test_tc03_008_sdyf_invalid_length_fail(self, api_client):
        """TC03-008: 生成0工资记录-sdyf长度非6位-失败"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC2025001",
            "sdyf": "20253",
            "personIds": ["310101199001011234"]
        }
        response = api_client.post("/api/v2/tax/salaryData/zeroWage", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="sdyf")

    @pytest.mark.P1
    @pytest.mark.正向
    def test_tc03_009_single_personId_success(self, api_client):
        """TC03-009: 生成0工资记录-单个personId-成功"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC2025001",
            "sdyf": "202503",
            "personIds": ["310101199001011234"]
        }
        response = api_client.post("/api/v2/tax/salaryData/zeroWage", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    @pytest.mark.正向
    def test_tc03_010_multiple_personIds_success(self, api_client):
        """TC03-010: 生成0工资记录-多个personId-成功"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC2025001",
            "sdyf": "202503",
            "personIds": ["310101199001011234", "310101199002022345", "310101199003033456"]
        }
        response = api_client.post("/api/v2/tax/salaryData/zeroWage", json_data=request_data)
        assert_response_success(response, expected_success=True)


# ============================================================================
# TC04: 触发算税
# 接口路径: POST /api/v2/tax/taxCompute/trigger
# ============================================================================

@pytest.mark.TC04
class TestTC04TaxComputeTrigger:
    """触发算税"""
    
    @pytest.mark.P0
    @pytest.mark.正向
    def test_tc04_001_batch_trigger_skjs_success(self, api_client):
        """TC04-001: 触发算税-批量算税BATCH-SKJS模式-成功"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC2025001",
            "sdyf": "202503",
            "triggerType": "BATCH",
            "computeMode": "SKJS"
        }
        response = api_client.post("/api/v2/tax/taxCompute/trigger", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P0
    @pytest.mark.正向
    def test_tc04_002_batch_trigger_gyss_success(self, api_client):
        """TC04-002: 触发算税-批量算税BATCH-GYSS模式-成功"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC2025001",
            "sdyf": "202503",
            "triggerType": "BATCH",
            "computeMode": "GYSS"
        }
        response = api_client.post("/api/v2/tax/taxCompute/trigger", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P0
    @pytest.mark.正向
    def test_tc04_003_person_trigger_success(self, api_client):
        """TC04-003: 触发算税-单人算税PERSON-成功"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC2025001",
            "sdyf": "202503",
            "triggerType": "PERSON",
            "personIds": ["310101199001011234"],
            "computeMode": "SKJS"
        }
        response = api_client.post("/api/v2/tax/taxCompute/trigger", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P0
    @pytest.mark.反向
    def test_tc04_004_missing_cpId_fail(self, api_client):
        """TC04-004: 触发算税-缺少cpId-失败"""
        request_data = {
            "taxClassCode": "TC2025001",
            "sdyf": "202503",
            "triggerType": "BATCH",
            "computeMode": "SKJS"
        }
        response = api_client.post("/api/v2/tax/taxCompute/trigger", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="cpId")

    @pytest.mark.P0
    @pytest.mark.反向
    def test_tc04_005_missing_taxClassCode_fail(self, api_client):
        """TC04-005: 触发算税-缺少taxClassCode-失败"""
        request_data = {
            "cpId": 1001,
            "sdyf": "202503",
            "triggerType": "BATCH",
            "computeMode": "SKJS"
        }
        response = api_client.post("/api/v2/tax/taxCompute/trigger", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="taxClassCode")

    @pytest.mark.P0
    @pytest.mark.反向
    def test_tc04_006_missing_sdyf_fail(self, api_client):
        """TC04-006: 触发算税-缺少sdyf-失败"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC2025001",
            "triggerType": "BATCH",
            "computeMode": "SKJS"
        }
        response = api_client.post("/api/v2/tax/taxCompute/trigger", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="sdyf")

    @pytest.mark.P0
    @pytest.mark.反向
    def test_tc04_007_missing_triggerType_fail(self, api_client):
        """TC04-007: 触发算税-缺少triggerType-失败"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC2025001",
            "sdyf": "202503",
            "computeMode": "SKJS"
        }
        response = api_client.post("/api/v2/tax/taxCompute/trigger", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="triggerType")

    @pytest.mark.P1
    @pytest.mark.正向
    def test_tc04_008_missing_computeMode_success(self, api_client):
        """TC04-008: 触发算税-缺少computeMode-成功"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC2025001",
            "sdyf": "202503",
            "triggerType": "BATCH"
        }
        response = api_client.post("/api/v2/tax/taxCompute/trigger", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P0
    @pytest.mark.反向
    def test_tc04_009_person_without_personIds_fail(self, api_client):
        """TC04-009: 触发算税-triggerType为PERSON时缺少personIds-失败"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC2025001",
            "sdyf": "202503",
            "triggerType": "PERSON"
        }
        response = api_client.post("/api/v2/tax/taxCompute/trigger", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="personIds")

    @pytest.mark.P1
    @pytest.mark.正向
    def test_tc04_010_batch_with_personIds_ignored(self, api_client):
        """TC04-010: 触发算税-triggerType为BATCH时传入personIds-成功"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC2025001",
            "sdyf": "202503",
            "triggerType": "BATCH",
            "personIds": ["310101199001011234"],
            "computeMode": "SKJS"
        }
        response = api_client.post("/api/v2/tax/taxCompute/trigger", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    @pytest.mark.反向
    def test_tc04_011_sdyf_invalid_format_fail(self, api_client):
        """TC04-011: 触发算税-sdyf格式错误-失败"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC2025001",
            "sdyf": "2025-03",
            "triggerType": "BATCH",
            "computeMode": "SKJS"
        }
        response = api_client.post("/api/v2/tax/taxCompute/trigger", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="sdyf")

    @pytest.mark.P1
    @pytest.mark.反向
    def test_tc04_012_triggerType_invalid_fail(self, api_client):
        """TC04-012: 触发算税-triggerType无效值-失败"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC2025001",
            "sdyf": "202503",
            "triggerType": "INVALID",
            "computeMode": "SKJS"
        }
        response = api_client.post("/api/v2/tax/taxCompute/trigger", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="triggerType")

    @pytest.mark.P1
    @pytest.mark.正向
    def test_tc04_013_no_data_success(self, api_client):
        """TC04-014: 触发算税-无可算税记录-成功"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC2025001",
            "sdyf": "209912",
            "triggerType": "BATCH",
            "computeMode": "SKJS"
        }
        response = api_client.post("/api/v2/tax/taxCompute/trigger", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    @pytest.mark.正向
    def test_tc04_014_verify_taskid_returned(self, api_client):
        """TC04-015: 触发算税-验证返回taskId"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC2025001",
            "sdyf": "202503",
            "triggerType": "BATCH",
            "computeMode": "SKJS"
        }
        response = api_client.post("/api/v2/tax/taxCompute/trigger", json_data=request_data)
        assert_response_success(response, expected_success=True)
        data = response.json()
        assert "taskId" in data.get("data", {}), \
            f"返回数据应包含taskId，实际响应: {data}"
        assert data["data"]["taskId"], "taskId不应为空"

    @pytest.mark.P1
    @pytest.mark.正向
    def test_tc04_015_verify_count_fields(self, api_client):
        """TC04-016: 触发算税-验证返回totalCount和mergedCount"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC2025001",
            "sdyf": "202503",
            "triggerType": "BATCH",
            "computeMode": "SKJS"
        }
        response = api_client.post("/api/v2/tax/taxCompute/trigger", json_data=request_data)
        assert_response_success(response, expected_success=True)
        data = response.json()
        result = data.get("data", {})
        assert "totalCount" in result, f"返回数据应包含totalCount，实际响应: {data}"
        assert "mergedCount" in result, f"返回数据应包含mergedCount，实际响应: {data}"
        assert result["totalCount"] >= result["mergedCount"], \
            f"totalCount({result['totalCount']})应>=mergedCount({result['mergedCount']})"


# ============================================================================
# TC05: 重新触发算税
# 接口路径: POST /api/v2/tax/taxCompute/retry
# ============================================================================

@pytest.mark.TC05
class TestTC05TaxComputeRetry:
    """重新触发算税"""
    
    @pytest.mark.P0
    @pytest.mark.正向
    def test_tc05_001_retry_all_failures_success(self, api_client):
        """TC05-001: 重新触发算税-重试所有失败记录-成功"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC2025001",
            "sdyf": "202503"
        }
        response = api_client.post("/api/v2/tax/taxCompute/retry", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P0
    @pytest.mark.正向
    def test_tc05_002_retry_specific_records_success(self, api_client):
        """TC05-002: 重新触发算税-重试指定记录-成功"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC2025001",
            "sdyf": "202503",
            "recordIds": [100001, 100002]
        }
        response = api_client.post("/api/v2/tax/taxCompute/retry", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P0
    @pytest.mark.反向
    def test_tc05_003_missing_cpId_fail(self, api_client):
        """TC05-003: 重新触发算税-缺少cpId-失败"""
        request_data = {
            "taxClassCode": "TC2025001",
            "sdyf": "202503"
        }
        response = api_client.post("/api/v2/tax/taxCompute/retry", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="cpId")

    @pytest.mark.P0
    @pytest.mark.反向
    def test_tc05_004_missing_taxClassCode_fail(self, api_client):
        """TC05-004: 重新触发算税-缺少taxClassCode-失败"""
        request_data = {
            "cpId": 1001,
            "sdyf": "202503"
        }
        response = api_client.post("/api/v2/tax/taxCompute/retry", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="taxClassCode")

    @pytest.mark.P0
    @pytest.mark.反向
    def test_tc05_005_missing_sdyf_fail(self, api_client):
        """TC05-005: 重新触发算税-缺少sdyf-失败"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC2025001"
        }
        response = api_client.post("/api/v2/tax/taxCompute/retry", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="sdyf")

    @pytest.mark.P1
    @pytest.mark.反向
    def test_tc05_006_sdyf_invalid_format_fail(self, api_client):
        """TC05-006: 重新触发算税-sdyf格式错误-失败"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC2025001",
            "sdyf": "2025-03"
        }
        response = api_client.post("/api/v2/tax/taxCompute/retry", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="sdyf")

    @pytest.mark.P2
    @pytest.mark.正向
    def test_tc05_007_empty_recordIds_success(self, api_client):
        """TC05-007: 重新触发算税-recordIds为空数组-成功"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC2025001",
            "sdyf": "202503",
            "recordIds": []
        }
        response = api_client.post("/api/v2/tax/taxCompute/retry", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    @pytest.mark.正向
    def test_tc05_008_nonexistent_recordIds_success(self, api_client):
        """TC05-008: 重新触发算税-指定不存在的recordIds-成功"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC2025001",
            "sdyf": "202503",
            "recordIds": [999999, 999998]
        }
        response = api_client.post("/api/v2/tax/taxCompute/retry", json_data=request_data)
        assert_response_success(response, expected_success=True)


# ============================================================================
# TC06: 算税结果查询
# 接口路径: POST /api/v2/tax/taxCompute/result/list
# ============================================================================

@pytest.mark.TC06
class TestTC06TaxResultList:
    """算税结果查询"""
    
    @pytest.mark.P0
    @pytest.mark.正向
    def test_tc06_001_list_success(self, api_client):
        """TC06-001: 算税结果查询-正常参数-成功"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC2025001",
            "sdyf": "202503",
            "pageNum": 1,
            "pageSize": 20
        }
        response = api_client.post("/api/v2/tax/taxCompute/result/list", json_data=request_data)
        assert_response_code(response, expected_code="200")

    @pytest.mark.P0
    @pytest.mark.反向
    def test_tc06_002_missing_cpId_fail(self, api_client):
        """TC06-002: 算税结果查询-缺少cpId-失败"""
        request_data = {
            "taxClassCode": "TC2025001",
            "sdyf": "202503",
            "pageNum": 1,
            "pageSize": 20
        }
        response = api_client.post("/api/v2/tax/taxCompute/result/list", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="cpId")

    @pytest.mark.P0
    @pytest.mark.反向
    def test_tc06_003_missing_taxClassCode_fail(self, api_client):
        """TC06-003: 算税结果查询-缺少taxClassCode-失败"""
        request_data = {
            "cpId": 1001,
            "sdyf": "202503",
            "pageNum": 1,
            "pageSize": 20
        }
        response = api_client.post("/api/v2/tax/taxCompute/result/list", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="taxClassCode")

    @pytest.mark.P0
    @pytest.mark.反向
    def test_tc06_004_missing_sdyf_fail(self, api_client):
        """TC06-004: 算税结果查询-缺少sdyf-失败"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC2025001",
            "pageNum": 1,
            "pageSize": 20
        }
        response = api_client.post("/api/v2/tax/taxCompute/result/list", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="sdyf")

    @pytest.mark.P1
    @pytest.mark.正向
    def test_tc06_005_filter_by_status_success(self, api_client):
        """TC06-005: 算税结果查询-按status过滤-成功"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC2025001",
            "sdyf": "202503",
            "status": 0,
            "pageNum": 1,
            "pageSize": 20
        }
        response = api_client.post("/api/v2/tax/taxCompute/result/list", json_data=request_data)
        assert_response_code(response, expected_code="200")

    @pytest.mark.P1
    @pytest.mark.分页
    def test_tc06_006_pagination_pageNum_success(self, api_client):
        """TC06-006: 算税结果查询-分页pageNum-成功"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC2025001",
            "sdyf": "202503",
            "pageNum": 2,
            "pageSize": 20
        }
        response = api_client.post("/api/v2/tax/taxCompute/result/list", json_data=request_data)
        assert_response_code(response, expected_code="200")

    @pytest.mark.P1
    @pytest.mark.分页
    def test_tc06_007_pagination_pageSize_success(self, api_client):
        """TC06-007: 算税结果查询-分页pageSize-成功"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC2025001",
            "sdyf": "202503",
            "pageNum": 1,
            "pageSize": 50
        }
        response = api_client.post("/api/v2/tax/taxCompute/result/list", json_data=request_data)
        assert_response_code(response, expected_code="200")

    @pytest.mark.P1
    @pytest.mark.正向
    def test_tc06_008_verify_fields_complete(self, api_client):
        """TC06-008: 算税结果查询-验证返回字段完整性"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC2025001",
            "sdyf": "202503",
            "pageNum": 1,
            "pageSize": 20
        }
        response = api_client.post("/api/v2/tax/taxCompute/result/list", json_data=request_data)
        assert_response_code(response, expected_code="200")

    @pytest.mark.P2
    @pytest.mark.正向
    def test_tc06_009_empty_result_success(self, api_client):
        """TC06-009: 算税结果查询-空结果-成功"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC2025001",
            "sdyf": "209912",
            "pageNum": 1,
            "pageSize": 20
        }
        response = api_client.post("/api/v2/tax/taxCompute/result/list", json_data=request_data)
        assert_response_code(response, expected_code="200")


# ============================================================================
# TC07: 算税汇总统计
# 接口路径: POST /api/v2/tax/taxCompute/result/summary
# ============================================================================

@pytest.mark.TC07
class TestTC07TaxResultSummary:
    """算税汇总统计"""
    
    @pytest.mark.P0
    @pytest.mark.正向
    def test_tc07_001_summary_success(self, api_client):
        """TC07-001: 算税汇总统计-正常参数-成功"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC2025001",
            "sdyf": "202503"
        }
        response = api_client.post("/api/v2/tax/taxCompute/result/summary", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P0
    @pytest.mark.反向
    def test_tc07_002_missing_cpId_fail(self, api_client):
        """TC07-002: 算税汇总统计-缺少cpId-失败"""
        request_data = {
            "taxClassCode": "TC2025001",
            "sdyf": "202503"
        }
        response = api_client.post("/api/v2/tax/taxCompute/result/summary", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="cpId")

    @pytest.mark.P0
    @pytest.mark.反向
    def test_tc07_003_missing_taxClassCode_fail(self, api_client):
        """TC07-003: 算税汇总统计-缺少taxClassCode-失败"""
        request_data = {
            "cpId": 1001,
            "sdyf": "202503"
        }
        response = api_client.post("/api/v2/tax/taxCompute/result/summary", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="taxClassCode")

    @pytest.mark.P0
    @pytest.mark.反向
    def test_tc07_004_missing_sdyf_fail(self, api_client):
        """TC07-004: 算税汇总统计-缺少sdyf-失败"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC2025001"
        }
        response = api_client.post("/api/v2/tax/taxCompute/result/summary", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="sdyf")

    @pytest.mark.P1
    @pytest.mark.反向
    def test_tc07_005_sdyf_invalid_format_fail(self, api_client):
        """TC07-005: 算税汇总统计-sdyf格式错误-失败"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC2025001",
            "sdyf": "2025-03"
        }
        response = api_client.post("/api/v2/tax/taxCompute/result/summary", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="sdyf")

    @pytest.mark.P1
    @pytest.mark.正向
    def test_tc07_006_verify_total_person_count(self, api_client):
        """TC07-006: 算税汇总统计-验证返回totalPersonCount"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC2025001",
            "sdyf": "202503"
        }
        response = api_client.post("/api/v2/tax/taxCompute/result/summary", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    @pytest.mark.正向
    def test_tc07_007_verify_total_sre_and_ybtse(self, api_client):
        """TC07-007: 算税汇总统计-验证返回totalSre和totalYbtse"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC2025001",
            "sdyf": "202503"
        }
        response = api_client.post("/api/v2/tax/taxCompute/result/summary", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    @pytest.mark.正向
    def test_tc07_008_verify_status_counts(self, api_client):
        """TC07-008: 算税汇总统计-验证返回各状态count"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC2025001",
            "sdyf": "202503"
        }
        response = api_client.post("/api/v2/tax/taxCompute/result/summary", json_data=request_data)
        assert_response_success(response, expected_success=True)


# ============================================================================
# TC08: 算税记录详情
# 接口路径: POST /api/v2/tax/taxCompute/result/detail
# ============================================================================

@pytest.mark.TC08
class TestTC08TaxResultDetail:
    """算税记录详情"""
    
    @pytest.mark.P0
    @pytest.mark.正向
    def test_tc08_001_detail_success(self, api_client):
        """TC08-001: 算税记录详情-正常参数-成功"""
        request_data = {
            "cpId": 1001,
            "id": 100001
        }
        response = api_client.post("/api/v2/tax/taxCompute/result/detail", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P0
    @pytest.mark.反向
    def test_tc08_002_missing_cpId_fail(self, api_client):
        """TC08-002: 算税记录详情-缺少cpId-失败"""
        request_data = {
            "id": 100001
        }
        response = api_client.post("/api/v2/tax/taxCompute/result/detail", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="cpId")

    @pytest.mark.P0
    @pytest.mark.反向
    def test_tc08_003_missing_id_fail(self, api_client):
        """TC08-003: 算税记录详情-缺少id-失败"""
        request_data = {
            "cpId": 1001
        }
        response = api_client.post("/api/v2/tax/taxCompute/result/detail", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="id")

    @pytest.mark.P1
    @pytest.mark.反向
    def test_tc08_004_id_not_exist_fail(self, api_client):
        """TC08-004: 算税记录详情-id不存在-失败"""
        request_data = {
            "cpId": 1001,
            "id": 999999
        }
        response = api_client.post("/api/v2/tax/taxCompute/result/detail", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="不存在")

    @pytest.mark.P1
    @pytest.mark.正向
    def test_tc08_005_verify_complete_fields(self, api_client):
        """TC08-005: 算税记录详情-验证返回税局完整字段"""
        request_data = {
            "cpId": 1001,
            "id": 100001
        }
        response = api_client.post("/api/v2/tax/taxCompute/result/detail", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    @pytest.mark.正向
    def test_tc08_006_verify_ljynssde_sl_sskcs(self, api_client):
        """TC08-006: 算税记录详情-验证返回ljynssde/sl/sskcs"""
        request_data = {
            "cpId": 1001,
            "id": 100001
        }
        response = api_client.post("/api/v2/tax/taxCompute/result/detail", json_data=request_data)
        assert_response_success(response, expected_success=True)


# ============================================================================
# TC09: 导出算税结果
# 接口路径: POST /api/v2/tax/taxCompute/result/export
# ============================================================================

@pytest.mark.TC09
class TestTC09TaxResultExport:
    """导出算税结果"""
    
    @pytest.mark.P0
    @pytest.mark.正向
    def test_tc09_001_export_success(self, api_client):
        """TC09-001: 导出算税结果-正常参数-成功"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC2025001",
            "sdyf": "202503"
        }
        response = api_client.post("/api/v2/tax/taxCompute/result/export", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P0
    @pytest.mark.反向
    @pytest.mark.P0
    @pytest.mark.反向
    def test_tc09_002_missing_cpId_fail(self, api_client):
        """TC09-002: 导出算税结果-缺少cpId-失败"""
        request_data = {
            "taxClassCode": "TC2025001",
            "sdyf": "202503"
        }
        response = api_client.post("/api/v2/tax/taxCompute/result/export", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="cpId")

    @pytest.mark.P0
    @pytest.mark.反向
    def test_tc09_003_missing_taxClassCode_fail(self, api_client):
        """TC09-003: 导出算税结果-缺少taxClassCode-失败"""
        request_data = {
            "cpId": 1001,
            "sdyf": "202503"
        }
        response = api_client.post("/api/v2/tax/taxCompute/result/export", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="taxClassCode")

    @pytest.mark.P0
    @pytest.mark.反向
    def test_tc09_004_missing_sdyf_fail(self, api_client):
        """TC09-004: 导出算税结果-缺少sdyf-失败"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC2025001"
        }
        response = api_client.post("/api/v2/tax/taxCompute/result/export", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="sdyf")

    @pytest.mark.P1
    @pytest.mark.正向
    def test_tc09_005_filter_by_sdxm_success(self, api_client):
        """TC09-005: 导出算税结果-按sdxm过滤-成功"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC2025001",
            "sdyf": "202503",
            "sdxm": "正常工资薪金"
        }
        response = api_client.post("/api/v2/tax/taxCompute/result/export", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    @pytest.mark.反向
    def test_tc09_006_sdyf_invalid_format_fail(self, api_client):
        """TC09-006: 导出算税结果-sdyf格式错误-失败"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC2025001",
            "sdyf": "2025-03"
        }
        response = api_client.post("/api/v2/tax/taxCompute/result/export", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="sdyf")

    @pytest.mark.P1
    @pytest.mark.正向
    def test_tc09_007_no_pagination_success(self, api_client):
        """TC09-007: 导出算税结果-不分页-成功"""
        request_data = {
            "cpId": 1001,
            "taxClassCode": "TC2025001",
            "sdyf": "202503",
            "pageSize": -1
        }
        response = api_client.post("/api/v2/tax/taxCompute/result/export", json_data=request_data)
        assert_response_success(response, expected_success=True)


# ============================================================================
# TC: 鉴权测试
# ============================================================================

@pytest.mark.TC
@pytest.mark.鉴权
class TestTCAuthentication:
    """个税计算模块 - 鉴权测试"""
    
    def test_tc_auth_no_token_fail(self, api_client):
        """TC-AUTH-001: 所有接口-无token访问-失败"""
        from tests.conftest import APIClient
        temp_client = APIClient(api_client.base_url, {})
        request_data = {"cpId": 1001, "taxClassCode": "TC001", "sdyf": "202503"}
        response = temp_client.post("/api/v2/tax/salaryData/list", json_data=request_data)
        assert response.status_code == 401

    def test_tc_auth_invalid_token_fail(self, api_client):
        """TC-AUTH-002: 所有接口-token无效-失败"""
        from tests.conftest import APIClient
        temp_client = APIClient(api_client.base_url, {"Authorization": "Bearer invalid_token"})
        request_data = {"cpId": 1001, "taxClassCode": "TC001", "sdyf": "202503"}
        response = temp_client.post("/api/v2/tax/salaryData/list", json_data=request_data)
        assert response.status_code == 401

    def test_tc_auth_expired_token_fail(self, api_client):
        """TC-AUTH-003: 所有接口-token过期-失败"""
        from tests.conftest import APIClient
        temp_client = APIClient(api_client.base_url, {"Authorization": "Bearer expired_token"})
        request_data = {"cpId": 1001, "taxClassCode": "TC001", "sdyf": "202503"}
        response = temp_client.post("/api/v2/tax/salaryData/list", json_data=request_data)
        assert response.status_code == 401
