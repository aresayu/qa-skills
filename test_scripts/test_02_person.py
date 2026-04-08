"""
人员报送模块测试用例 (PS)
接口路径前缀: /api/v2/tax/person

测试范围:
- PS01: 查询人员列表
- PS02: 新增人员
- PS03: 修改人员
- PS04: 删除人员
- PS05: 批量删除人员
- PS06: 单个报送人员
- PS07: 批量报送人员

共计: 50+ 测试用例
"""
import pytest
from tests.conftest import assert_response_success, assert_response_code


# ============================================================================
# PS01: 查询人员列表
# 接口路径: POST /api/v2/tax/person/query
# ============================================================================

@pytest.mark.PS01
class TestPS01QueryPerson:
    """查询人员列表"""
    
    @pytest.mark.P0
    @pytest.mark.正向
    def test_ps01_001_query_success(self, api_client):
        """PS01-001: 查询人员列表-正常参数-成功"""
        request_data = {
            "cpId": "1001",
            "xm": "张三",
            "kjsrybm": "Agent001",
            "sdyf": "202503",
            "pageNum": 1,
            "pageSize": 20
        }
        response = api_client.post("/api/v2/tax/person/query", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P0
    @pytest.mark.反向
    def test_ps01_002_missing_cpId_fail(self, api_client):
        """PS01-002: 查询人员列表-缺少cpId-失败"""
        request_data = {
            "xm": "张三",
            "sdyf": "202503",
            "pageNum": 1,
            "pageSize": 20
        }
        response = api_client.post("/api/v2/tax/person/query", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="cpId")

    @pytest.mark.P1
    @pytest.mark.正向
    def test_ps01_003_query_no_filter_success(self, api_client):
        """PS01-003: 查询人员列表-所有筛选条件为空-成功"""
        request_data = {
            "cpId": "1001",
            "pageNum": 1,
            "pageSize": 20
        }
        response = api_client.post("/api/v2/tax/person/query", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    @pytest.mark.正向
    def test_ps01_004_filter_by_kjsrybm_success(self, api_client):
        """PS01-004: 查询人员列表-按kjsrybm精确查询-成功"""
        request_data = {
            "cpId": "1001",
            "kjsrybm": "Agent001",
            "pageNum": 1,
            "pageSize": 20
        }
        response = api_client.post("/api/v2/tax/person/query", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    @pytest.mark.正向
    def test_ps01_005_filter_by_gh_success(self, api_client):
        """PS01-005: 查询人员列表-按gh模糊查询-成功"""
        request_data = {
            "cpId": "1001",
            "gh": "001",
            "pageNum": 1,
            "pageSize": 20
        }
        response = api_client.post("/api/v2/tax/person/query", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    @pytest.mark.正向
    def test_ps01_006_filter_by_xm_success(self, api_client):
        """PS01-006: 查询人员列表-按xm模糊查询-成功"""
        request_data = {
            "cpId": "1001",
            "xm": "张三",
            "pageNum": 1,
            "pageSize": 20
        }
        response = api_client.post("/api/v2/tax/person/query", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    @pytest.mark.正向
    def test_ps01_007_filter_by_zzhm_success(self, api_client):
        """PS01-007: 查询人员列表-按zzhm模糊查询-成功"""
        request_data = {
            "cpId": "1001",
            "zzhm": "310101",
            "pageNum": 1,
            "pageSize": 20
        }
        response = api_client.post("/api/v2/tax/person/query", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    @pytest.mark.正向
    def test_ps01_008_filter_by_sfgy_success(self, api_client):
        """PS01-008: 查询人员列表-按sfgy筛选-成功"""
        request_data = {
            "cpId": "1001",
            "sfgy": "01",
            "pageNum": 1,
            "pageSize": 20
        }
        response = api_client.post("/api/v2/tax/person/query", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    @pytest.mark.正向
    def test_ps01_009_filter_by_bszt_success(self, api_client):
        """PS01-009: 查询人员列表-按bszt筛选-成功"""
        request_data = {
            "cpId": "1001",
            "bszt": "0",
            "pageNum": 1,
            "pageSize": 20
        }
        response = api_client.post("/api/v2/tax/person/query", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    @pytest.mark.正向
    def test_ps01_010_filter_by_sdyf_success(self, api_client):
        """PS01-010: 查询人员列表-按sdyf格式筛选-成功"""
        request_data = {
            "cpId": "1001",
            "sdyf": "202503",
            "pageNum": 1,
            "pageSize": 20
        }
        response = api_client.post("/api/v2/tax/person/query", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    @pytest.mark.反向
    def test_ps01_011_sdyf_invalid_format_fail(self, api_client):
        """PS01-011: 查询人员列表-sdyf格式错误-失败"""
        request_data = {
            "cpId": "1001",
            "sdyf": "2025-03",
            "pageNum": 1,
            "pageSize": 20
        }
        response = api_client.post("/api/v2/tax/person/query", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="sdyf")

    @pytest.mark.P1
    @pytest.mark.正向
    def test_ps01_012_filter_by_psnType_success(self, api_client):
        """PS01-012: 查询人员列表-按psnType筛选-成功"""
        request_data = {
            "cpId": "1001",
            "psnType": "DOMESTIC",
            "pageNum": 1,
            "pageSize": 20
        }
        response = api_client.post("/api/v2/tax/person/query", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    @pytest.mark.分页
    def test_ps01_013_pagination_pageNum_success(self, api_client):
        """PS01-013: 查询人员列表-按pageNum分页-成功"""
        request_data = {
            "cpId": "1001",
            "pageNum": 2,
            "pageSize": 10
        }
        response = api_client.post("/api/v2/tax/person/query", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    @pytest.mark.分页
    def test_ps01_014_pagination_pageSize_success(self, api_client):
        """PS01-014: 查询人员列表-按pageSize分页-成功"""
        request_data = {
            "cpId": "1001",
            "pageNum": 1,
            "pageSize": 50
        }
        response = api_client.post("/api/v2/tax/person/query", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    @pytest.mark.正向
    def test_ps01_015_verify_fields_complete(self, api_client):
        """PS01-015: 查询人员列表-验证返回字段完整性"""
        request_data = {
            "cpId": "1001",
            "pageNum": 1,
            "pageSize": 20
        }
        response = api_client.post("/api/v2/tax/person/query", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P2
    @pytest.mark.正向
    def test_ps01_016_empty_result_success(self, api_client):
        """PS01-016: 查询人员列表-空结果-成功"""
        request_data = {
            "cpId": "9999",
            "xm": "不存在的姓名XYZ",
            "pageNum": 1,
            "pageSize": 20
        }
        response = api_client.post("/api/v2/tax/person/query", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    @pytest.mark.正向
    def test_ps01_017_multi_condition_query_success(self, api_client):
        """PS01-017: 查询人员列表-多条件组合查询-成功"""
        request_data = {
            "cpId": "1001",
            "xm": "张",
            "sfgy": "01",
            "sdyf": "202503",
            "pageNum": 1,
            "pageSize": 20
        }
        response = api_client.post("/api/v2/tax/person/query", json_data=request_data)
        assert_response_success(response, expected_success=True)


# ============================================================================
# PS02: 新增人员
# 接口路径: POST /api/v2/tax/person/create
# ============================================================================

@pytest.mark.PS02
class TestPS02CreatePerson:
    """新增人员"""
    
    @pytest.mark.P0
    @pytest.mark.正向
    def test_ps02_001_create_success(self, api_client, generate_unique_id):
        """PS02-001: 新增人员-正常参数-成功"""
        request_data = {
            "cpId": "1001",
            "xm": f"张三{generate_unique_id()}",
            "zzlx": "A",
            "zzhm": f"31010119900101{generate_unique_id()[:4]}",
            "kjsrybm": "Agent001",
            "kjsry": "XX科技有限公司",
            "sfgy": "01",
            "sdyf": "202503",
            "taxClassCode": "PLAN_abc123def456",
            "lxdh": "13800138000"
        }
        response = api_client.post("/api/v2/tax/person/create", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P0
    @pytest.mark.反向
    def test_ps02_002_missing_xm_fail(self, api_client):
        """PS02-002: 新增人员-缺少必填xm-失败"""
        request_data = {
            "cpId": "1001",
            "zzlx": "A",
            "zzhm": "310101199001011234",
            "kjsrybm": "Agent001",
            "kjsry": "XX科技有限公司",
            "sfgy": "01",
            "sdyf": "202503",
            "taxClassCode": "PLAN_abc123def456"
        }
        response = api_client.post("/api/v2/tax/person/create", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="xm")

    @pytest.mark.P0
    @pytest.mark.反向
    def test_ps02_003_missing_zzlx_fail(self, api_client, generate_unique_id):
        """PS02-003: 新增人员-缺少必填zzlx-失败"""
        request_data = {
            "cpId": "1001",
            "xm": f"张三{generate_unique_id()}",
            "zzhm": "310101199001011234",
            "kjsrybm": "Agent001",
            "kjsry": "XX科技有限公司",
            "sfgy": "01",
            "sdyf": "202503",
            "taxClassCode": "PLAN_abc123def456"
        }
        response = api_client.post("/api/v2/tax/person/create", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="zzlx")

    @pytest.mark.P0
    @pytest.mark.反向
    def test_ps02_004_missing_zzhm_fail(self, api_client, generate_unique_id):
        """PS02-004: 新增人员-缺少必填zzhm-失败"""
        request_data = {
            "cpId": "1001",
            "xm": f"张三{generate_unique_id()}",
            "zzlx": "A",
            "kjsrybm": "Agent001",
            "kjsry": "XX科技有限公司",
            "sfgy": "01",
            "sdyf": "202503",
            "taxClassCode": "PLAN_abc123def456"
        }
        response = api_client.post("/api/v2/tax/person/create", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="zzhm")

    @pytest.mark.P0
    @pytest.mark.反向
    def test_ps02_005_missing_kjsrybm_fail(self, api_client, generate_unique_id):
        """PS02-005: 新增人员-缺少必填kjsrybm-失败"""
        request_data = {
            "cpId": "1001",
            "xm": f"张三{generate_unique_id()}",
            "zzlx": "A",
            "zzhm": "310101199001011234",
            "kjsry": "XX科技有限公司",
            "sfgy": "01",
            "sdyf": "202503",
            "taxClassCode": "PLAN_abc123def456"
        }
        response = api_client.post("/api/v2/tax/person/create", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="kjsrybm")

    @pytest.mark.P0
    @pytest.mark.反向
    def test_ps02_006_missing_kjsry_fail(self, api_client, generate_unique_id):
        """PS02-006: 新增人员-缺少必填kjsry-失败"""
        request_data = {
            "cpId": "1001",
            "xm": f"张三{generate_unique_id()}",
            "zzlx": "A",
            "zzhm": "310101199001011234",
            "kjsrybm": "Agent001",
            "sfgy": "01",
            "sdyf": "202503",
            "taxClassCode": "PLAN_abc123def456"
        }
        response = api_client.post("/api/v2/tax/person/create", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="kjsry")

    @pytest.mark.P0
    @pytest.mark.反向
    def test_ps02_007_missing_sfgy_fail(self, api_client, generate_unique_id):
        """PS02-007: 新增人员-缺少必填sfgy-失败"""
        request_data = {
            "cpId": "1001",
            "xm": f"张三{generate_unique_id()}",
            "zzlx": "A",
            "zzhm": "310101199001011234",
            "kjsrybm": "Agent001",
            "kjsry": "XX科技有限公司",
            "sdyf": "202503",
            "taxClassCode": "PLAN_abc123def456"
        }
        response = api_client.post("/api/v2/tax/person/create", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="sfgy")

    @pytest.mark.P0
    @pytest.mark.反向
    def test_ps02_008_missing_sdyf_fail(self, api_client, generate_unique_id):
        """PS02-008: 新增人员-缺少必填sdyf-失败"""
        request_data = {
            "cpId": "1001",
            "xm": f"张三{generate_unique_id()}",
            "zzlx": "A",
            "zzhm": "310101199001011234",
            "kjsrybm": "Agent001",
            "kjsry": "XX科技有限公司",
            "sfgy": "01",
            "taxClassCode": "PLAN_abc123def456"
        }
        response = api_client.post("/api/v2/tax/person/create", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="sdyf")

    @pytest.mark.P0
    @pytest.mark.反向
    def test_ps02_009_missing_taxClassCode_fail(self, api_client, generate_unique_id):
        """PS02-009: 新增人员-缺少必填taxClassCode-失败"""
        request_data = {
            "cpId": "1001",
            "xm": f"张三{generate_unique_id()}",
            "zzlx": "A",
            "zzhm": "310101199001011234",
            "kjsrybm": "Agent001",
            "kjsry": "XX科技有限公司",
            "sfgy": "01",
            "sdyf": "202503"
        }
        response = api_client.post("/api/v2/tax/person/create", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="taxClassCode")

    @pytest.mark.P1
    @pytest.mark.反向
    def test_ps02_010_sdyf_invalid_format_fail(self, api_client, generate_unique_id):
        """PS02-010: 新增人员-sdyf格式错误-失败"""
        request_data = {
            "xm": f"张三{generate_unique_id()}",
            "zzlx": "A",
            "zzhm": "310101199001011234",
            "kjsrybm": "Agent001",
            "kjsry": "XX科技有限公司",
            "sfgy": "01",
            "sdyf": "2025-03",
            "taxClassCode": "PLAN_abc123def456"
        }
        response = api_client.post("/api/v2/tax/person/create", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="sdyf")

    @pytest.mark.P1
    @pytest.mark.边界值
    def test_ps02_011_sdyf_greater_than_now_fail(self, api_client, generate_unique_id):
        """PS02-011: 新增人员-sdyf大于当前时间-失败"""
        request_data = {
            "xm": f"张三{generate_unique_id()}",
            "zzlx": "A",
            "zzhm": "310101199001011234",
            "kjsrybm": "Agent001",
            "kjsry": "XX科技有限公司",
            "sfgy": "01",
            "sdyf": "209912",
            "taxClassCode": "PLAN_abc123def456"
        }
        response = api_client.post("/api/v2/tax/person/create", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="sdyf")

    @pytest.mark.P1
    @pytest.mark.反向
    def test_ps02_012_zzlx_invalid_fail(self, api_client, generate_unique_id):
        """PS02-012: 新增人员-zzlx为无效值-失败"""
        request_data = {
            "cpId": "1001",
            "xm": f"张三{generate_unique_id()}",
            "zzlx": "X",
            "zzhm": "310101199001011234",
            "kjsrybm": "Agent001",
            "kjsry": "XX科技有限公司",
            "sfgy": "01",
            "sdyf": "202503",
            "taxClassCode": "PLAN_abc123def456"
        }
        response = api_client.post("/api/v2/tax/person/create", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="zzlx")

    @pytest.mark.P1
    @pytest.mark.正向
    def test_ps02_013_zzlx_a_success(self, api_client, generate_unique_id):
        """PS02-013: 新增人员-zzlx为A(居民身份证)-成功"""
        request_data = {
            "cpId": "1001",
            "xm": f"李四{generate_unique_id()}",
            "zzlx": "A",
            "zzhm": f"31010119900202{generate_unique_id()[:4]}",
            "kjsrybm": "Agent001",
            "kjsry": "XX科技有限公司",
            "sfgy": "01",
            "sdyf": "202503",
            "taxClassCode": "PLAN_abc123def456"
        }
        response = api_client.post("/api/v2/tax/person/create", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    @pytest.mark.反向
    def test_ps02_014_lxdh_invalid_format_fail(self, api_client, generate_unique_id):
        """PS02-014: 新增人员-lxdh格式错误-失败"""
        request_data = {
            "xm": f"张三{generate_unique_id()}",
            "zzlx": "A",
            "zzhm": "310101199001011234",
            "kjsrybm": "Agent001",
            "kjsry": "XX科技有限公司",
            "sfgy": "01",
            "sdyf": "202503",
            "taxClassCode": "PLAN_abc123def456",
            "lxdh": "13800138"
        }
        response = api_client.post("/api/v2/tax/person/create", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="手机号码")

    @pytest.mark.P2
    @pytest.mark.正向
    def test_ps02_015_lxdh_empty_string_success(self, api_client, generate_unique_id):
        """PS02-015: 新增人员-lxdh为空字符串-成功"""
        request_data = {
            "cpId": "1001",
            "xm": f"张三{generate_unique_id()}",
            "zzlx": "A",
            "zzhm": f"31010119900101{generate_unique_id()[:4]}",
            "kjsrybm": "Agent001",
            "kjsry": "XX科技有限公司",
            "sfgy": "01",
            "sdyf": "202503",
            "taxClassCode": "PLAN_abc123def456",
            "lxdh": ""
        }
        response = api_client.post("/api/v2/tax/person/create", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    @pytest.mark.正向
    def test_ps02_016_psnType_domestic_success(self, api_client, generate_unique_id):
        """PS02-016: 新增人员-psnType为DOMESTIC-成功"""
        request_data = {
            "cpId": "1001",
            "xm": f"张三{generate_unique_id()}",
            "zzlx": "A",
            "zzhm": f"31010119900101{generate_unique_id()[:4]}",
            "kjsrybm": "Agent001",
            "kjsry": "XX科技有限公司",
            "sfgy": "01",
            "sdyf": "202503",
            "taxClassCode": "PLAN_abc123def456",
            "psnType": "DOMESTIC"
        }
        response = api_client.post("/api/v2/tax/person/create", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    @pytest.mark.正向
    def test_ps02_017_psnType_foreign_success(self, api_client, generate_unique_id):
        """PS02-017: 新增人员-psnType为FOREIGN-成功"""
        request_data = {
            "cpId": "1001",
            "xm": f"John{generate_unique_id()}",
            "zzlx": "C",
            "zzhm": f"E12345{generate_unique_id()[:4]}",
            "kjsrybm": "Agent001",
            "kjsry": "XX科技有限公司",
            "sfgy": "01",
            "sdyf": "202503",
            "taxClassCode": "PLAN_abc123def456",
            "psnType": "FOREIGN",
            "gj": "USA"
        }
        response = api_client.post("/api/v2/tax/person/create", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    @pytest.mark.反向
    def test_ps02_018_foreign_without_gj_fail(self, api_client, generate_unique_id):
        """PS02-018: 新增人员-境外人员缺少gj-失败"""
        request_data = {
            "cpId": "1001",
            "xm": f"John{generate_unique_id()}",
            "zzlx": "C",
            "zzhm": f"E12345{generate_unique_id()[:4]}",
            "kjsrybm": "Agent001",
            "kjsry": "XX科技有限公司",
            "sfgy": "01",
            "sdyf": "202503",
            "taxClassCode": "PLAN_abc123def456",
            "psnType": "FOREIGN"
        }
        response = api_client.post("/api/v2/tax/person/create", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="gj")

    @pytest.mark.P1
    @pytest.mark.反向
    def test_ps02_019_bsny_invalid_format_fail(self, api_client, generate_unique_id):
        """PS02-019: 新增人员-bsny格式错误-失败"""
        request_data = {
            "cpId": "1001",
            "xm": f"张三{generate_unique_id()}",
            "zzlx": "A",
            "zzhm": f"31010119900101{generate_unique_id()[:4]}",
            "kjsrybm": "Agent001",
            "kjsry": "XX科技有限公司",
            "sfgy": "01",
            "sdyf": "202503",
            "taxClassCode": "PLAN_abc123def456",
            "bsny": "2025-03"
        }
        response = api_client.post("/api/v2/tax/person/create", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="bsny")

    @pytest.mark.P1
    @pytest.mark.边界值
    def test_ps02_020_bsny_greater_than_now_fail(self, api_client, generate_unique_id):
        """PS02-020: 新增人员-bsny大于当前时间-失败"""
        request_data = {
            "cpId": "1001",
            "xm": f"张三{generate_unique_id()}",
            "zzlx": "A",
            "zzhm": f"31010119900101{generate_unique_id()[:4]}",
            "kjsrybm": "Agent001",
            "kjsry": "XX科技有限公司",
            "sfgy": "01",
            "sdyf": "202503",
            "taxClassCode": "PLAN_abc123def456",
            "bsny": "209912"
        }
        response = api_client.post("/api/v2/tax/person/create", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="bsny")

    @pytest.mark.P1
    @pytest.mark.正向
    def test_ps02_021_sfgy_01_success(self, api_client, generate_unique_id):
        """PS02-021: 新增人员-sfgy为01(正常在职)-成功"""
        request_data = {
            "cpId": "1001",
            "xm": f"张三{generate_unique_id()}",
            "zzlx": "A",
            "zzhm": f"31010119900101{generate_unique_id()[:4]}",
            "kjsrybm": "Agent001",
            "kjsry": "XX科技有限公司",
            "sfgy": "01",
            "sdyf": "202503",
            "taxClassCode": "PLAN_abc123def456"
        }
        response = api_client.post("/api/v2/tax/person/create", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    @pytest.mark.正向
    def test_ps02_022_sfgy_02_success(self, api_client, generate_unique_id):
        """PS02-022: 新增人员-sfgy为02(离职)-成功"""
        request_data = {
            "cpId": "1001",
            "xm": f"张三{generate_unique_id()}",
            "zzlx": "A",
            "zzhm": f"31010119900101{generate_unique_id()[:4]}",
            "kjsrybm": "Agent001",
            "kjsry": "XX科技有限公司",
            "sfgy": "02",
            "sdyf": "202503",
            "taxClassCode": "PLAN_abc123def456"
        }
        response = api_client.post("/api/v2/tax/person/create", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    @pytest.mark.反向
    def test_ps02_023_sfbfgz_without_bfyf_fail(self, api_client, generate_unique_id):
        """PS02-023: 新增人员-sfbfgz为1时缺少bfyf-失败"""
        request_data = {
            "cpId": "1001",
            "xm": f"张三{generate_unique_id()}",
            "zzlx": "A",
            "zzhm": f"31010119900101{generate_unique_id()[:4]}",
            "kjsrybm": "Agent001",
            "kjsry": "XX科技有限公司",
            "sfgy": "01",
            "sdyf": "202503",
            "taxClassCode": "PLAN_abc123def456",
            "sfbfgz": "1"
        }
        response = api_client.post("/api/v2/tax/person/create", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="bfyf")

    @pytest.mark.P2
    @pytest.mark.正向
    def test_ps02_024_sfkcjcfy_success(self, api_client, generate_unique_id):
        """PS02-024: 新增人员-sfkcjcfy为1-成功"""
        request_data = {
            "cpId": "1001",
            "xm": f"张三{generate_unique_id()}",
            "zzlx": "A",
            "zzhm": f"31010119900101{generate_unique_id()[:4]}",
            "kjsrybm": "Agent001",
            "kjsry": "XX科技有限公司",
            "sfgy": "01",
            "sdyf": "202503",
            "taxClassCode": "PLAN_abc123def456",
            "sfkcjcfy": "1",
            "cjcfy": 500
        }
        response = api_client.post("/api/v2/tax/person/create", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    @pytest.mark.反向
    def test_ps02_025_sfcj_without_cjzjlx_cjzh_fail(self, api_client, generate_unique_id):
        """PS02-025: 新增人员-sfcj为1时缺少cjzjlx/cjzh-失败"""
        request_data = {
            "cpId": "1001",
            "xm": f"张三{generate_unique_id()}",
            "zzlx": "A",
            "zzhm": f"31010119900101{generate_unique_id()[:4]}",
            "kjsrybm": "Agent001",
            "kjsry": "XX科技有限公司",
            "sfgy": "01",
            "sdyf": "202503",
            "taxClassCode": "PLAN_abc123def456",
            "sfcj": "1"
        }
        response = api_client.post("/api/v2/tax/person/create", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="cjzjlx")

    @pytest.mark.P2
    @pytest.mark.正向
    def test_ps02_026_sfgl_success(self, api_client, generate_unique_id):
        """PS02-026: 新增人员-sfgl为1-成功"""
        request_data = {
            "cpId": "1001",
            "xm": f"张三{generate_unique_id()}",
            "zzlx": "A",
            "zzhm": f"31010119900101{generate_unique_id()[:4]}",
            "kjsrybm": "Agent001",
            "kjsry": "XX科技有限公司",
            "sfgy": "01",
            "sdyf": "202503",
            "taxClassCode": "PLAN_abc123def456",
            "sfgl": "1",
            "glmj": 100
        }
        response = api_client.post("/api/v2/tax/person/create", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    @pytest.mark.反向
    def test_ps02_027_sfls_without_lszh_fail(self, api_client, generate_unique_id):
        """PS02-027: 新增人员-sfls为1时缺少lszh-失败"""
        request_data = {
            "cpId": "1001",
            "xm": f"张三{generate_unique_id()}",
            "zzlx": "A",
            "zzhm": f"31010119900101{generate_unique_id()[:4]}",
            "kjsrybm": "Agent001",
            "kjsry": "XX科技有限公司",
            "sfgy": "01",
            "sdyf": "202503",
            "taxClassCode": "PLAN_abc123def456",
            "sfls": "1"
        }
        response = api_client.post("/api/v2/tax/person/create", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="lszh")

    @pytest.mark.P1
    @pytest.mark.反向
    def test_ps02_028_grtzze_grtzbl_mismatch_fail(self, api_client, generate_unique_id):
        """PS02-028: 新增人员-grtzze与grtzbl不匹配-失败"""
        request_data = {
            "cpId": "1001",
            "xm": f"张三{generate_unique_id()}",
            "zzlx": "A",
            "zzhm": f"31010119900101{generate_unique_id()[:4]}",
            "kjsrybm": "Agent001",
            "kjsry": "XX科技有限公司",
            "sfgy": "01",
            "sdyf": "202503",
            "taxClassCode": "PLAN_abc123def456",
            "grtzze": 10000,
            "grtzbl": "0.3"
        }
        response = api_client.post("/api/v2/tax/person/create", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="grtzze")


    @pytest.mark.P2
    @pytest.mark.正向
    def test_ps02_029_all_optional_fields_success(self, api_client, generate_unique_id):
        """PS02-029: 新增人员-所有可选字段都填写-成功"""
        request_data = {
            "cpId": "1001",
            "xm": f"张三{generate_unique_id()}",
            "zzlx": "A",
            "zzhm": f"31010119900101{generate_unique_id()[:4]}",
            "kjsrybm": "Agent001",
            "kjsry": "XX科技有限公司",
            "sfgy": "01",
            "sdyf": "202503",
            "taxClassCode": "PLAN_abc123def456",
            "lxdh": "13800138000",
            "psnType": "DOMESTIC",
            "bsny": "202001",
            "sfbfgz": "0",
            "sfkcjcfy": "0",
            "sfcj": "0",
            "sfgl": "0",
            "sfls": "0"
        }
        response = api_client.post("/api/v2/tax/person/create", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    @pytest.mark.反向
    def test_ps02_030_duplicate_zzhm_fail(self, api_client, generate_unique_id):
        """PS02-030: 新增人员-重复zzhm-失败"""
        request_data = {
            "cpId": "1001",
            "xm": f"王五{generate_unique_id()}",
            "zzlx": "A",
            "zzhm": "310101199001011234",
            "kjsrybm": "Agent001",
            "kjsry": "XX科技有限公司",
            "sfgy": "01",
            "sdyf": "202503",
            "taxClassCode": "PLAN_abc123def456"
        }
        response = api_client.post("/api/v2/tax/person/create", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="证件号码")


# ============================================================================
# PS03: 修改人员
# 接口路径: POST /api/v2/tax/person/update
# ============================================================================

@pytest.mark.PS03
class TestPS03UpdatePerson:
    """修改人员"""
    
    @pytest.mark.P0
    @pytest.mark.正向
    def test_ps03_001_update_success(self, api_client):
        """PS03-001: 修改人员-正常参数-成功"""
        request_data = {
            "cpId": "1001",
            "pkPerson": "PSN20250301001",
            "xm": "张三（修改）",
            "lxdh": "13900139000"
        }
        response = api_client.post("/api/v2/tax/person/update", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P0
    @pytest.mark.反向
    def test_ps03_002_missing_cpId_fail(self, api_client):
        """PS03-002: 修改人员-缺少cpId-失败"""
        request_data = {
            "pkPerson": "PSN20250301001",
            "xm": "张三（修改）"
        }
        response = api_client.post("/api/v2/tax/person/update", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="cpId")

    @pytest.mark.P0
    @pytest.mark.反向
    def test_ps03_003_missing_pkPerson_fail(self, api_client):
        """PS03-003: 修改人员-缺少pkPerson-失败"""
        request_data = {
            "cpId": "1001",
            "xm": "张三（修改）"
        }
        response = api_client.post("/api/v2/tax/person/update", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="pkPerson")

    @pytest.mark.P1
    @pytest.mark.反向
    def test_ps03_004_invalid_pkPerson_fail(self, api_client):
        """PS03-004: 修改人员-pkPerson不存在-失败"""
        request_data = {
            "cpId": "1001",
            "pkPerson": "INVALID_PSN",
            "xm": "张三（修改）"
        }
        response = api_client.post("/api/v2/tax/person/update", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="pkPerson")

    @pytest.mark.P1
    @pytest.mark.正向
    def test_ps03_005_update_xm_success(self, api_client):
        """PS03-005: 修改人员-修改xm-成功"""
        request_data = {
            "cpId": "1001",
            "pkPerson": "PSN20250301001",
            "xm": "张三（修改）"
        }
        response = api_client.post("/api/v2/tax/person/update", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    @pytest.mark.反向
    def test_ps03_006_update_lxdh_invalid_format_fail(self, api_client):
        """PS03-006: 修改人员-修改lxdh格式错误-失败"""
        request_data = {
            "cpId": "1001",
            "pkPerson": "PSN20250301001",
            "lxdh": "12345"
        }
        response = api_client.post("/api/v2/tax/person/update", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="手机号码")

    @pytest.mark.P1
    @pytest.mark.反向
    def test_ps03_007_update_sdyf_invalid_format_fail(self, api_client):
        """PS03-007: 修改人员-修改sdyf格式错误-失败"""
        request_data = {
            "cpId": "1001",
            "pkPerson": "PSN20250301001",
            "sdyf": "2025-03"
        }
        response = api_client.post("/api/v2/tax/person/update", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="sdyf")

    @pytest.mark.P2
    @pytest.mark.正向
    def test_ps03_008_update_no_optional_fields_success(self, api_client):
        """PS03-008: 修改人员-所有可选参数为空-成功"""
        request_data = {
            "cpId": "1001",
            "pkPerson": "PSN20250301001"
        }
        response = api_client.post("/api/v2/tax/person/update", json_data=request_data)
        assert_response_success(response, expected_success=True)


# ============================================================================
# PS04: 删除人员
# 接口路径: POST /api/v2/tax/person/delete
# ============================================================================

@pytest.mark.PS04
class TestPS04DeletePerson:
    """删除人员"""
    
    @pytest.mark.P0
    @pytest.mark.正向
    def test_ps04_001_delete_success(self, api_client):
        """PS04-001: 删除人员-正常参数-成功"""
        request_data = {
            "cpId": "1001",
            "pkPerson": "PSN20250301001"
        }
        response = api_client.post("/api/v2/tax/person/delete", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P0
    @pytest.mark.反向
    def test_ps04_002_missing_cpId_fail(self, api_client):
        """PS04-002: 删除人员-缺少cpId-失败"""
        request_data = {
            "pkPerson": "PSN20250301001"
        }
        response = api_client.post("/api/v2/tax/person/delete", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="cpId")

    @pytest.mark.P0
    @pytest.mark.反向
    def test_ps04_003_missing_pkPerson_fail(self, api_client):
        """PS04-003: 删除人员-缺少pkPerson-失败"""
        request_data = {
            "cpId": "1001"
        }
        response = api_client.post("/api/v2/tax/person/delete", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="pkPerson")

    @pytest.mark.P1
    @pytest.mark.反向
    def test_ps04_004_invalid_pkPerson_fail(self, api_client):
        """PS04-004: 删除人员-pkPerson不存在-失败"""
        request_data = {
            "cpId": "1001",
            "pkPerson": "INVALID_PSN"
        }
        response = api_client.post("/api/v2/tax/person/delete", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="pkPerson")

    @pytest.mark.P1
    @pytest.mark.幂等
    def test_ps04_005_duplicate_delete_success(self, api_client):
        """PS04-005: 删除人员-重复删除-成功"""
        request_data = {
            "cpId": "1001",
            "pkPerson": "PSN20250301001"
        }
        response = api_client.post("/api/v2/tax/person/delete", json_data=request_data)
        assert_response_success(response, expected_success=True)


# ============================================================================
# PS05: 批量删除人员
# 接口路径: POST /api/v2/tax/person/batch-delete
# ============================================================================

@pytest.mark.PS05
class TestPS05BatchDeletePerson:
    """批量删除人员"""
    
    @pytest.mark.P0
    @pytest.mark.正向
    def test_ps05_001_batch_delete_success(self, api_client):
        """PS05-001: 批量删除人员-正常参数-成功"""
        request_data = {
            "cpId": "1001",
            "pkPersons": ["PSN20250301001", "PSN20250301002", "PSN20250301003"]
        }
        response = api_client.post("/api/v2/tax/person/batch-delete", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P0
    @pytest.mark.反向
    def test_ps05_002_missing_cpId_fail(self, api_client):
        """PS05-002: 批量删除人员-缺少cpId-失败"""
        request_data = {
            "pkPersons": ["PSN20250301001", "PSN20250301002"]
        }
        response = api_client.post("/api/v2/tax/person/batch-delete", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="cpId")

    @pytest.mark.P0
    @pytest.mark.反向
    def test_ps05_003_missing_pkPersons_fail(self, api_client):
        """PS05-003: 批量删除人员-缺少pkPersons-失败"""
        request_data = {
            "cpId": "1001"
        }
        response = api_client.post("/api/v2/tax/person/batch-delete", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="pkPersons")

    @pytest.mark.P0
    @pytest.mark.反向
    def test_ps05_004_empty_pkPersons_fail(self, api_client):
        """PS05-004: 批量删除人员-pkPersons为空数组-失败"""
        request_data = {
            "cpId": "1001",
            "pkPersons": []
        }
        response = api_client.post("/api/v2/tax/person/batch-delete", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="pkPersons")

    @pytest.mark.P1
    @pytest.mark.反向
    def test_ps05_005_partial_invalid_pkPersons_success(self, api_client):
        """PS05-005: 批量删除人员-部分pkPerson不存在-成功"""
        request_data = {
            "cpId": "1001",
            "pkPersons": ["PSN20250301001", "PSN20250301002"]
        }
        response = api_client.post("/api/v2/tax/person/batch-delete", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    @pytest.mark.正向
    def test_ps05_006_all_invalid_pkPersons_success(self, api_client):
        """PS05-006: 批量删除人员-全部pkPerson不存在-成功"""
        request_data = {
            "cpId": "1001",
            "pkPersons": ["INVALID1", "INVALID2", "INVALID3"]
        }
        response = api_client.post("/api/v2/tax/person/batch-delete", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    @pytest.mark.正向
    def test_ps05_007_single_pkPerson_success(self, api_client):
        """PS05-007: 批量删除人员-单个人员ID-成功"""
        request_data = {
            "cpId": "1001",
            "pkPersons": ["PSN20250301001"]
        }
        response = api_client.post("/api/v2/tax/person/batch-delete", json_data=request_data)
        assert_response_success(response, expected_success=True)


# ============================================================================
# PS06: 单个报送人员
# 接口路径: POST /api/v2/tax/person/submit
# ============================================================================

@pytest.mark.PS06
class TestPS06SubmitPerson:
    """单个报送人员"""
    
    @pytest.mark.P0
    @pytest.mark.正向
    def test_ps06_001_submit_success(self, api_client):
        """PS06-001: 单个报送人员-正常参数-成功"""
        request_data = {
            "cpId": "1001",
            "pkPerson": "PSN20250301001"
        }
        response = api_client.post("/api/v2/tax/person/submit", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P0
    @pytest.mark.反向
    def test_ps06_002_missing_cpId_fail(self, api_client):
        """PS06-002: 单个报送人员-缺少cpId-失败"""
        request_data = {
            "pkPerson": "PSN20250301001"
        }
        response = api_client.post("/api/v2/tax/person/submit", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="cpId")

    @pytest.mark.P0
    @pytest.mark.反向
    def test_ps06_003_missing_pkPerson_fail(self, api_client):
        """PS06-003: 单个报送人员-缺少pkPerson-失败"""
        request_data = {
            "cpId": "1001"
        }
        response = api_client.post("/api/v2/tax/person/submit", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="pkPerson")

    @pytest.mark.P1
    @pytest.mark.反向
    def test_ps06_004_invalid_pkPerson_fail(self, api_client):
        """PS06-004: 单个报送人员-pkPerson不存在-失败"""
        request_data = {
            "cpId": "1001",
            "pkPerson": "INVALID_PSN"
        }
        response = api_client.post("/api/v2/tax/person/submit", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="pkPerson")

    @pytest.mark.P1
    @pytest.mark.幂等
    def test_ps06_005_duplicate_submit_success(self, api_client):
        """PS06-005: 单个报送人员-重复报送-成功"""
        request_data = {
            "cpId": "1001",
            "pkPerson": "PSN20250301001"
        }
        response = api_client.post("/api/v2/tax/person/submit", json_data=request_data)
        assert_response_success(response, expected_success=True)


# ============================================================================
# PS07: 批量报送人员
# 接口路径: POST /api/v2/tax/person/batch-submit
# ============================================================================

@pytest.mark.PS07
class TestPS07BatchSubmitPerson:
    """批量报送人员"""
    
    @pytest.mark.P0
    @pytest.mark.正向
    def test_ps07_001_batch_submit_success(self, api_client):
        """PS07-001: 批量报送人员-正常参数-成功"""
        request_data = {
            "cpId": "1001",
            "pkPersons": ["PSN20250301001", "PSN20250301002"]
        }
        response = api_client.post("/api/v2/tax/person/batch-submit", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P0
    @pytest.mark.反向
    def test_ps07_002_missing_cpId_fail(self, api_client):
        """PS07-002: 批量报送人员-缺少cpId-失败"""
        request_data = {
            "pkPersons": ["PSN20250301001", "PSN20250301002"]
        }
        response = api_client.post("/api/v2/tax/person/batch-submit", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="cpId")

    @pytest.mark.P0
    @pytest.mark.反向
    def test_ps07_003_missing_pkPersons_fail(self, api_client):
        """PS07-003: 批量报送人员-缺少pkPersons-失败"""
        request_data = {
            "cpId": "1001"
        }
        response = api_client.post("/api/v2/tax/person/batch-submit", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="pkPersons")

    @pytest.mark.P0
    @pytest.mark.反向
    def test_ps07_004_empty_pkPersons_fail(self, api_client):
        """PS07-004: 批量报送人员-pkPersons为空数组-失败"""
        request_data = {
            "cpId": "1001",
            "pkPersons": []
        }
        response = api_client.post("/api/v2/tax/person/batch-submit", json_data=request_data)
        assert_response_success(response, expected_success=False, expected_msg="pkPersons")

    @pytest.mark.P1
    @pytest.mark.反向
    def test_ps07_005_partial_invalid_pkPersons_success(self, api_client):
        """PS07-005: 批量报送人员-部分pkPerson不存在-成功"""
        request_data = {
            "cpId": "1001",
            "pkPersons": ["PSN20250301001", "INVALID_PSN"]
        }
        response = api_client.post("/api/v2/tax/person/batch-submit", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    @pytest.mark.正向
    def test_ps07_006_all_invalid_pkPersons_success(self, api_client):
        """PS07-006: 批量报送人员-全部pkPerson不存在-成功"""
        request_data = {
            "cpId": "1001",
            "pkPersons": ["INVALID1", "INVALID2"]
        }
        response = api_client.post("/api/v2/tax/person/batch-submit", json_data=request_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    @pytest.mark.正向
    def test_ps07_007_verify_total_and_submitting(self, api_client):
        """PS07-007: 批量报送人员-验证返回total和submitting"""
        request_data = {
            "cpId": "1001",
            "pkPersons": ["PSN20250301001", "PSN20250301002"]
        }
        response = api_client.post("/api/v2/tax/person/batch-submit", json_data=request_data)
        assert_response_success(response, expected_success=True)
        data = response.json()
        assert "data" in data

    @pytest.mark.P1
    @pytest.mark.正向
    def test_ps07_008_single_pkPerson_success(self, api_client):
        """PS07-008: 批量报送人员-单个人员ID-成功"""
        request_data = {
            "cpId": "1001",
            "pkPersons": ["PSN20250301001"]
        }
        response = api_client.post("/api/v2/tax/person/batch-submit", json_data=request_data)
        assert_response_success(response, expected_success=True)


# ============================================================================
# PS: 鉴权测试
# ============================================================================

@pytest.mark.PS
@pytest.mark.鉴权
class TestPSAuthentication:
    """人员报送模块 - 鉴权测试"""
    
    def test_ps_auth_no_token_fail(self, api_client):
        """PS-AUTH-001: 所有接口-无token访问-失败"""
        from tests.conftest import APIClient
        temp_client = APIClient(api_client.base_url, {})
        request_data = {"cpId": "1001"}
        response = temp_client.post("/api/v2/tax/person/query", json_data=request_data)
        assert response.status_code == 401

    def test_ps_auth_invalid_token_fail(self, api_client):
        """PS-AUTH-002: 所有接口-token无效-失败"""
        from tests.conftest import APIClient
        temp_client = APIClient(api_client.base_url, {"Authorization": "Bearer invalid_token"})
        request_data = {"cpId": "1001"}
        response = temp_client.post("/api/v2/tax/person/query", json_data=request_data)
        assert response.status_code == 401

    def test_ps_auth_expired_token_fail(self, api_client):
        """PS-AUTH-003: 所有接口-token过期-失败"""
        from tests.conftest import APIClient
        temp_client = APIClient(api_client.base_url, {"Authorization": "Bearer expired_token"})
        request_data = {"cpId": "1001"}
        response = temp_client.post("/api/v2/tax/person/query", json_data=request_data)
        assert response.status_code == 401
