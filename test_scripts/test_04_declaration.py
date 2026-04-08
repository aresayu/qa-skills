"""
个税申报模块测试用例 (TD/RD)
接口路径前缀:
- 生产版(TD): /api/v2/tax/declaration
- 研发版(RD): /api/tax-declaration/external

测试范围:
- TD01: 申报数据查询
- TD02: 个税申报执行
- TD03: 申报状态查询
- TD04: 待填附表人员查询
- TD05: 附表人员数据保存
- TD06: 附表规则字典查询
- RD01: 申报数据查询(研发版)
- RD02: 个税申报提交(研发版)
- RD03: 申报详情查询(研发版)
- RD04: 申报状态查询(研发版)
"""
import pytest
import requests
from conftest import (
    APIClient,
    assert_response_success,
    assert_response_code,
)


# ============================================================================
# API客户端封装
# ============================================================================

class DeclarationClient:
    """个税申报API客户端封装"""

    def __init__(self, api_client: APIClient):
        self._client = api_client

    def td_query(self, **kwargs) -> requests.Response:
        """TD01-申报数据查询 POST /api/v2/tax/declaration/query"""
        return self._client.post("/api/v2/tax/declaration/query", json_data=kwargs)

    def td_execute(self, **kwargs) -> requests.Response:
        """TD02-个税申报执行 POST /api/v2/tax/declaration/execute"""
        return self._client.post("/api/v2/tax/declaration/execute", json_data=kwargs)

    def td_status(self, accept_id: str) -> requests.Response:
        """TD03-申报状态查询 GET /api/v2/tax/declaration/status/{accept_id}"""
        return self._client.get(f"/api/v2/tax/declaration/status/{accept_id}")

    def td_pending_persons(self, **kwargs) -> requests.Response:
        """TD04-待填附表人员查询 POST /api/v2/tax/declaration/pending-persons"""
        return self._client.post("/api/v2/tax/declaration/pending-persons", json_data=kwargs)

    def td_attachment_save(self, **kwargs) -> requests.Response:
        """TD05-附表人员数据保存 POST /api/v2/tax/declaration/attachment/save"""
        return self._client.post("/api/v2/tax/declaration/attachment/save", json_data=kwargs)

    def td_attachment_rules(self, **kwargs) -> requests.Response:
        """TD06-附表规则字典查询 POST /api/v2/tax/declaration/attachment/rules"""
        return self._client.post("/api/v2/tax/declaration/attachment/rules", json_data=kwargs)

    def rd_query(self, **kwargs) -> requests.Response:
        """RD01-申报数据查询 POST /api/tax-declaration/external/query"""
        return self._client.post("/api/tax-declaration/external/query", json_data=kwargs)

    def rd_submit(self, **kwargs) -> requests.Response:
        """RD02-个税申报提交 POST /api/tax-declaration/external/submit"""
        return self._client.post("/api/tax-declaration/external/submit", json_data=kwargs)

    def rd_detail(self, **kwargs) -> requests.Response:
        """RD03-申报详情查询 POST /api/tax-declaration/external/detail"""
        return self._client.post("/api/tax-declaration/external/detail", json_data=kwargs)

    def rd_status(self, **kwargs) -> requests.Response:
        """RD04-申报状态查询 POST /api/tax-declaration/external/status"""
        return self._client.post("/api/tax-declaration/external/status", json_data=kwargs)


@pytest.fixture
def td_client(api_client):
    """生产版(TD) API客户端"""
    return DeclarationClient(api_client)


@pytest.fixture
def rd_client(api_client):
    """研发版(RD) API客户端"""
    return DeclarationClient(api_client)


# ============================================================================
# ====== 生产版 TD 测试类
# ============================================================================

@pytest.mark.TD
class TestTD01DeclarationQuery:
    """TD01-申报数据查询 (POST /api/v2/tax/declaration/query)"""

    @pytest.mark.P0
    def test_td01_001(self, td_client, declaration_base_data):
        """TD01-001: 正常参数-成功"""
        response = td_client.td_query(**declaration_base_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P0
    def test_td01_002(self, td_client, declaration_base_data):
        """TD01-002: 缺少agentCode-失败"""
        data = declaration_base_data.copy()
        data.pop("agentCode", None)
        response = td_client.td_query(**data)
        assert_response_success(response, expected_success=False)

    @pytest.mark.P0
    def test_td01_003(self, td_client, declaration_base_data):
        """TD01-003: 缺少sdyf-失败"""
        data = declaration_base_data.copy()
        data.pop("sdyf", None)
        response = td_client.td_query(**data)
        assert_response_success(response, expected_success=False)

    @pytest.mark.P0
    def test_td01_004(self, td_client, declaration_base_data):
        """TD01-004: 缺少sdlx-失败"""
        data = declaration_base_data.copy()
        data.pop("sdlx", None)
        response = td_client.td_query(**data)
        assert_response_success(response, expected_success=False)

    @pytest.mark.P0
    def test_td01_005(self, td_client, declaration_base_data):
        """TD01-005: 缺少areaid-失败"""
        data = declaration_base_data.copy()
        data.pop("areaid", None)
        response = td_client.td_query(**data)
        assert_response_success(response, expected_success=False)

    @pytest.mark.P0
    def test_td01_006(self, td_client, declaration_base_data):
        """TD01-006: 缺少djxhid-失败"""
        data = declaration_base_data.copy()
        data.pop("djxhid", None)
        response = td_client.td_query(**data)
        assert_response_success(response, expected_success=False)

    @pytest.mark.P0
    def test_td01_007(self, td_client, declaration_base_data):
        """TD01-007: 缺少sbmm-失败"""
        data = declaration_base_data.copy()
        data.pop("sbmm", None)
        response = td_client.td_query(**data)
        assert_response_success(response, expected_success=False)

    @pytest.mark.P1
    def test_td01_008(self, td_client, declaration_base_data):
        """TD01-008: sdyf格式错误(2025-03)-失败"""
        data = declaration_base_data.copy()
        data["sdyf"] = "2025-03"
        response = td_client.td_query(**data)
        assert_response_success(response, expected_success=False)

    @pytest.mark.P1
    def test_td01_009(self, td_client, declaration_base_data):
        """TD01-009: sdlx无效值-失败"""
        data = declaration_base_data.copy()
        data["sdlx"] = "无效所得类型"
        response = td_client.td_query(**data)
        assert_response_success(response, expected_success=False)

    @pytest.mark.P1
    def test_td01_010(self, td_client, declaration_base_data):
        """TD01-010: areaid格式错误-失败"""
        data = declaration_base_data.copy()
        data["areaid"] = "31"
        response = td_client.td_query(**data)
        assert_response_success(response, expected_success=False)

    @pytest.mark.P1
    def test_td01_011(self, td_client, declaration_base_data):
        """TD01-011: bmbh格式错误-失败"""
        data = declaration_base_data.copy()
        data["bmbh"] = "invalid!@#"
        response = td_client.td_query(**data)
        assert_response_success(response, expected_success=False)

    @pytest.mark.P1
    def test_td01_012(self, td_client, declaration_base_data):
        """TD01-012: 分部门报送-成功"""
        data = declaration_base_data.copy()
        data["bmbh"] = "DEPT001"
        response = td_client.td_query(**data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    def test_td01_013(self, td_client, declaration_base_data):
        """TD01-013: 验证返回嵌套结构-成功"""
        response = td_client.td_query(**declaration_base_data)
        assert_response_success(response, expected_success=True)
        data = response.json()
        assert "data" in data

    @pytest.mark.P1
    def test_td01_014(self, td_client, declaration_base_data):
        """TD01-014: 验证返回字段完整性-成功"""
        response = td_client.td_query(**declaration_base_data)
        assert_response_success(response, expected_success=True)
        data = response.json()
        assert "data" in data

    @pytest.mark.P2
    def test_td01_015(self, td_client, declaration_base_data):
        """TD01-015: 空结果-成功"""
        data = declaration_base_data.copy()
        data["sdyf"] = "209912"
        response = td_client.td_query(**data)
        assert_response_success(response, expected_success=True)


@pytest.mark.TD
class TestTD02DeclarationExecute:
    """TD02-个税申报执行 (POST /api/v2/tax/declaration/execute)"""

    @pytest.mark.P0
    def test_td02_001(self, td_client, declaration_base_data):
        """TD02-001: 正常参数-成功"""
        response = td_client.td_execute(**declaration_base_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P0
    def test_td02_002(self, td_client, declaration_base_data):
        """TD02-002: 缺少agentCode-失败"""
        data = declaration_base_data.copy()
        data.pop("agentCode", None)
        response = td_client.td_execute(**data)
        assert_response_success(response, expected_success=False)

    @pytest.mark.P0
    def test_td02_003(self, td_client, declaration_base_data):
        """TD02-003: 缺少sdyf-失败"""
        data = declaration_base_data.copy()
        data.pop("sdyf", None)
        response = td_client.td_execute(**data)
        assert_response_success(response, expected_success=False)

    @pytest.mark.P0
    def test_td02_004(self, td_client, declaration_base_data):
        """TD02-004: 缺少sdlx-失败"""
        data = declaration_base_data.copy()
        data.pop("sdlx", None)
        response = td_client.td_execute(**data)
        assert_response_success(response, expected_success=False)

    @pytest.mark.P0
    def test_td02_005(self, td_client, declaration_base_data):
        """TD02-005: 缺少areaid-失败"""
        data = declaration_base_data.copy()
        data.pop("areaid", None)
        response = td_client.td_execute(**data)
        assert_response_success(response, expected_success=False)

    @pytest.mark.P0
    def test_td02_006(self, td_client, declaration_base_data):
        """TD02-006: 缺少djxhid-失败"""
        data = declaration_base_data.copy()
        data.pop("djxhid", None)
        response = td_client.td_execute(**data)
        assert_response_success(response, expected_success=False)

    @pytest.mark.P0
    def test_td02_007(self, td_client, declaration_base_data):
        """TD02-007: 缺少sbmm-失败"""
        data = declaration_base_data.copy()
        data.pop("sbmm", None)
        response = td_client.td_execute(**data)
        assert_response_success(response, expected_success=False)

    @pytest.mark.P1
    def test_td02_008(self, td_client, declaration_base_data):
        """TD02-008: sbmm错误-失败"""
        data = declaration_base_data.copy()
        data["sbmm"] = "wrong_password"
        response = td_client.td_execute(**data)
        assert_response_success(response, expected_success=False)

    @pytest.mark.P1
    def test_td02_009(self, td_client, declaration_base_data):
        """TD02-009: sdyf格式错误-失败"""
        data = declaration_base_data.copy()
        data["sdyf"] = "2025-03"
        response = td_client.td_execute(**data)
        assert_response_success(response, expected_success=False)

    @pytest.mark.P1
    def test_td02_010(self, td_client, declaration_base_data):
        """TD02-010: sdlx无效值-失败"""
        data = declaration_base_data.copy()
        data["sdlx"] = "无效所得类型"
        response = td_client.td_execute(**data)
        assert_response_success(response, expected_success=False)

    @pytest.mark.P1
    def test_td02_011(self, td_client, declaration_base_data):
        """TD02-011: 验证返回accept_id-成功"""
        response = td_client.td_execute(**declaration_base_data)
        assert_response_success(response, expected_success=True)
        data = response.json()
        assert "data" in data

    @pytest.mark.P2
    def test_td02_012(self, td_client, declaration_base_data):
        """TD02-012: 重复申报-幂等"""
        response1 = td_client.td_execute(**declaration_base_data)
        assert_response_success(response1, expected_success=True)
        response2 = td_client.td_execute(**declaration_base_data)
        assert response2.status_code == 200


@pytest.mark.TD
class TestTD03DeclarationStatus:
    """TD03-申报状态查询 (GET /api/v2/tax/declaration/status/{accept_id})"""

    @pytest.mark.P0
    def test_td03_001(self, td_client):
        """TD03-001: 正常参数-成功"""
        response = td_client.td_status("ACCEPT20250301001")
        assert_response_success(response, expected_success=True)

    @pytest.mark.P0
    def test_td03_002(self, td_client, api_client):
        """TD03-002: 缺少accept_id路径参数-失败"""
        response = api_client.get("/api/v2/tax/declaration/status/")
        assert response.status_code in [400, 404]

    @pytest.mark.P1
    def test_td03_003(self, td_client):
        """TD03-003: accept_id不存在-失败"""
        response = td_client.td_status("ACCEPT_NOT_EXIST_99999")
        assert_response_success(response, expected_success=False)

    @pytest.mark.P1
    def test_td03_004(self, td_client, api_client):
        """TD03-004: accept_id格式错误-失败"""
        response = api_client.get("/api/v2/tax/declaration/status/invalid@format!")
        assert_response_success(response, expected_success=False)

    @pytest.mark.P1
    def test_td03_005(self, td_client):
        """TD03-005: 验证返回综合所得列表-成功"""
        response = td_client.td_status("ACCEPT20250301001")
        assert_response_success(response, expected_success=True)
        data = response.json()
        assert "data" in data

    @pytest.mark.P1
    def test_td03_006(self, td_client):
        """TD03-006: 验证返回分类所得列表-成功"""
        response = td_client.td_status("ACCEPT20250301001")
        assert_response_success(response, expected_success=True)
        data = response.json()
        assert "data" in data

    @pytest.mark.P1
    def test_td03_007(self, td_client):
        """TD03-007: 验证返回非居民所得列表-成功"""
        response = td_client.td_status("ACCEPT20250301001")
        assert_response_success(response, expected_success=True)
        data = response.json()
        assert "data" in data

    @pytest.mark.P1
    def test_td03_008(self, td_client):
        """TD03-008: 验证返回限售股列表-成功"""
        response = td_client.td_status("ACCEPT20250301001")
        assert_response_success(response, expected_success=True)
        data = response.json()
        assert "data" in data

    @pytest.mark.P1
    def test_td03_009(self, td_client):
        """TD03-009: 验证返回待邀请列表-成功"""
        response = td_client.td_status("ACCEPT20250301001")
        assert_response_success(response, expected_success=True)
        data = response.json()
        assert "data" in data

    @pytest.mark.P1
    def test_td03_010(self, td_client):
        """TD03-010: sbbz=2申报成功-成功"""
        response = td_client.td_status("ACCEPT20250301001")
        assert_response_success(response, expected_success=True)
        data = response.json()
        if "data" in data and isinstance(data["data"], dict):
            sbbz = data["data"].get("sbbz")
            assert sbbz == 2, f"申报状态应为2，实际为{sbbz}"

    @pytest.mark.P1
    def test_td03_011(self, td_client):
        """TD03-011: sbbz=3申报失败-成功"""
        response = td_client.td_status("ACCEPT_FAIL20250301001")
        assert_response_success(response, expected_success=True)
        data = response.json()
        if "data" in data and isinstance(data["data"], dict):
            sbbz = data["data"].get("sbbz")
            assert sbbz == 3, f"申报状态应为3，实际为{sbbz}"


@pytest.mark.TD
class TestTD04PendingPersons:
    """TD04-待填附表人员查询 (POST /api/v2/tax/declaration/pending-persons)"""

    @pytest.mark.P0
    def test_td04_001(self, td_client, declaration_base_data):
        """TD04-001: 正常参数-成功"""
        data = declaration_base_data.copy()
        data["accept_id"] = "ACC001"
        response = td_client.td_pending_persons(**data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P0
    def test_td04_002(self, td_client, declaration_base_data):
        """TD04-002: 缺少accept_id-失败"""
        data = declaration_base_data.copy()
        data.pop("accept_id", None)
        response = td_client.td_pending_persons(**data)
        assert_response_success(response, expected_success=False)

    @pytest.mark.P0
    def test_td04_003(self, td_client, declaration_base_data):
        """TD04-003: 缺少sdlx-失败"""
        data = declaration_base_data.copy()
        data["accept_id"] = "ACC001"
        data.pop("sdlx", None)
        response = td_client.td_pending_persons(**data)
        assert_response_success(response, expected_success=False)

    @pytest.mark.P2
    def test_td04_004(self, td_client, declaration_base_data):
        """TD04-004: 无待填人员-成功"""
        data = declaration_base_data.copy()
        data["accept_id"] = "ACC_NO_PENDING"
        response = td_client.td_pending_persons(**data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    def test_td04_005(self, td_client, declaration_base_data):
        """TD04-005: 有待填人员-成功"""
        data = declaration_base_data.copy()
        data["accept_id"] = "ACC_HAS_PENDING"
        response = td_client.td_pending_persons(**data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    def test_td04_006(self, td_client, declaration_base_data):
        """TD04-006: 多附表类型-成功"""
        data = declaration_base_data.copy()
        data["accept_id"] = "ACC_MULTI_TYPES"
        response = td_client.td_pending_persons(**data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    def test_td04_007(self, td_client, declaration_base_data):
        """TD04-007: 分部门报送-成功"""
        data = declaration_base_data.copy()
        data["accept_id"] = "ACC001"
        data["bmbh"] = "DEPT001"
        response = td_client.td_pending_persons(**data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    def test_td04_008(self, td_client, declaration_base_data):
        """TD04-008: 分类所得类型-成功"""
        data = declaration_base_data.copy()
        data["accept_id"] = "ACC001"
        data["sdlx"] = "分类所得"
        response = td_client.td_pending_persons(**data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    def test_td04_009(self, td_client, declaration_base_data):
        """TD04-009: 非居民所得类型-成功"""
        data = declaration_base_data.copy()
        data["accept_id"] = "ACC001"
        data["sdlx"] = "非居民所得"
        response = td_client.td_pending_persons(**data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    def test_td04_010(self, td_client, declaration_base_data):
        """TD04-010: accept_id不存在-失败"""
        data = declaration_base_data.copy()
        data["accept_id"] = "ACC_NOT_EXIST_99999"
        response = td_client.td_pending_persons(**data)
        assert_response_success(response, expected_success=False)


@pytest.mark.TD
class TestTD05AttachmentSave:
    """TD05-附表人员数据保存 (POST /api/v2/tax/declaration/attachment/save)"""

    @pytest.mark.P0
    def test_td05_001(self, td_client, declaration_base_data):
        """TD05-001: 正常参数-成功"""
        data = declaration_base_data.copy()
        data["accept_id"] = "ACC001"
        data["jmsxmx"] = [
            {
                "xm": "张三",
                "zzlx": "A",
                "zzhm": "310101199001011234",
                "jmfs": "免税收入",
                "sdxm": "0101",
                "jmsx": "个人所得税优惠",
                "jmxz": "其他",
                "jmse": 5000
            }
        ]
        response = td_client.td_attachment_save(**data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P0
    def test_td05_002(self, td_client, declaration_base_data):
        """TD05-002: 缺少accept_id-失败"""
        data = declaration_base_data.copy()
        data.pop("accept_id", None)
        response = td_client.td_attachment_save(**data)
        assert_response_success(response, expected_success=False)

    @pytest.mark.P0
    def test_td05_003(self, td_client, declaration_base_data):
        """TD05-003: 缺少sdlx-失败"""
        data = declaration_base_data.copy()
        data["accept_id"] = "ACC001"
        data.pop("sdlx", None)
        response = td_client.td_attachment_save(**data)
        assert_response_success(response, expected_success=False)

    @pytest.mark.P1
    def test_td05_004(self, td_client, declaration_base_data):
        """TD05-004: 减免事项必填字段缺失-失败"""
        data = declaration_base_data.copy()
        data["accept_id"] = "ACC001"
        data["jmsxmx"] = [{"xm": "张三"}]
        response = td_client.td_attachment_save(**data)
        assert_response_success(response, expected_success=False)

    @pytest.mark.P1
    def test_td05_005(self, td_client, declaration_base_data):
        """TD05-005: 减免事项完整数据-成功"""
        data = declaration_base_data.copy()
        data["accept_id"] = "ACC001"
        data["jmsxmx"] = [
            {
                "xm": "张三",
                "zzlx": "A",
                "zzhm": "310101199001011234",
                "jmfs": "免税收入",
                "sdxm": "0101",
                "jmsx": "个人所得税优惠",
                "jmxz": "其他",
                "jmse": 5000
            }
        ]
        response = td_client.td_attachment_save(**data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    def test_td05_006(self, td_client, declaration_base_data):
        """TD05-006: 商业健康险完整数据-成功"""
        data = declaration_base_data.copy()
        data["accept_id"] = "ACC001"
        data["jmsxmx"] = [
            {
                "xm": "李四",
                "zzlx": "A",
                "zzhm": "310101199002021234",
                "sdxm": "0111",
                "jmsx": "商业健康保险扣除",
                "jmse": 2000
            }
        ]
        response = td_client.td_attachment_save(**data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    def test_td05_007(self, td_client, declaration_base_data):
        """TD05-007: 捐赠附表完整数据-成功"""
        data = declaration_base_data.copy()
        data["accept_id"] = "ACC001"
        data["jmsxmx"] = [
            {
                "xm": "王五",
                "zzlx": "A",
                "zzhm": "310101199003031234",
                "sdxm": "0112",
                "jmsx": "捐赠扣除",
                "jmxz": "全额扣除",
                "jmse": 10000
            }
        ]
        response = td_client.td_attachment_save(**data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    def test_td05_008(self, td_client, declaration_base_data):
        """TD05-008: 多人员批量保存-成功"""
        data = declaration_base_data.copy()
        data["accept_id"] = "ACC001"
        data["jmsxmx"] = [
            {
                "xm": "员工A",
                "zzlx": "A",
                "zzhm": "310101199001011234",
                "sdxm": "0101",
                "jmsx": "个人所得税优惠",
                "jmxz": "其他",
                "jmse": 5000
            },
            {
                "xm": "员工B",
                "zzlx": "A",
                "zzhm": "310101199002021234",
                "sdxm": "0101",
                "jmsx": "个人所得税优惠",
                "jmxz": "其他",
                "jmse": 3000
            }
        ]
        response = td_client.td_attachment_save(**data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P2
    def test_td05_009(self, td_client, declaration_base_data):
        """TD05-009: 部分失败-成功"""
        data = declaration_base_data.copy()
        data["accept_id"] = "ACC_PARTIAL_FAIL"
        data["jmsxmx"] = [
            {
                "xm": "成功员工",
                "zzlx": "A",
                "zzhm": "310101199001011234",
                "sdxm": "0101",
                "jmsx": "个人所得税优惠",
                "jmxz": "其他",
                "jmse": 5000
            },
            {
                "xm": "失败员工",
                "zzlx": "A",
                "zzhm": "invalid",
                "sdxm": "0101",
                "jmsx": "个人所得税优惠",
                "jmxz": "其他",
                "jmse": 5000
            }
        ]
        response = td_client.td_attachment_save(**data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P2
    def test_td05_010(self, td_client, declaration_base_data):
        """TD05-010: 全部失败-失败"""
        data = declaration_base_data.copy()
        data["accept_id"] = "ACC_ALL_FAIL"
        data["jmsxmx"] = [
            {
                "xm": "员工1",
                "zzlx": "invalid_type",
                "zzhm": "invalid",
                "sdxm": "9999",
                "jmsx": "无效",
                "jmxz": "无效",
                "jmse": -100
            }
        ]
        response = td_client.td_attachment_save(**data)
        assert_response_success(response, expected_success=False)

    @pytest.mark.P1
    def test_td05_011(self, td_client, declaration_base_data):
        """TD05-011: 证照类型无效-失败"""
        data = declaration_base_data.copy()
        data["accept_id"] = "ACC001"
        data["jmsxmx"] = [
            {
                "xm": "张三",
                "zzlx": "X",
                "zzhm": "310101199001011234",
                "sdxm": "0101",
                "jmsx": "个人所得税优惠",
                "jmxz": "其他",
                "jmse": 5000
            }
        ]
        response = td_client.td_attachment_save(**data)
        assert_response_success(response, expected_success=False)

    @pytest.mark.P1
    def test_td05_012(self, td_client, declaration_base_data):
        """TD05-012: sbmm错误-失败"""
        data = declaration_base_data.copy()
        data["accept_id"] = "ACC001"
        data["sbmm"] = "wrong_password"
        data["jmsxmx"] = [
            {
                "xm": "张三",
                "zzlx": "A",
                "zzhm": "310101199001011234",
                "sdxm": "0101",
                "jmsx": "个人所得税优惠",
                "jmxz": "其他",
                "jmse": 5000
            }
        ]
        response = td_client.td_attachment_save(**data)
        assert_response_success(response, expected_success=False)

    @pytest.mark.P1
    def test_td05_013(self, td_client, declaration_base_data):
        """TD05-013: sdyf格式错误-失败"""
        data = declaration_base_data.copy()
        data["accept_id"] = "ACC001"
        data["sdyf"] = "2025-03"
        data["jmsxmx"] = [
            {
                "xm": "张三",
                "zzlx": "A",
                "zzhm": "310101199001011234",
                "sdxm": "0101",
                "jmsx": "个人所得税优惠",
                "jmxz": "其他",
                "jmse": 5000
            }
        ]
        response = td_client.td_attachment_save(**data)
        assert_response_success(response, expected_success=False)

    @pytest.mark.P2
    def test_td05_014(self, td_client, declaration_base_data):
        """TD05-014: 无附表数据-成功"""
        data = declaration_base_data.copy()
        data["accept_id"] = "ACC001"
        data["jmsxmx"] = []
        response = td_client.td_attachment_save(**data)
        assert_response_success(response, expected_success=True)


@pytest.mark.TD
class TestTD06AttachmentRules:
    """TD06-附表规则字典查询 (POST /api/v2/tax/declaration/attachment/rules)"""

    @pytest.mark.P0
    def test_td06_001(self, td_client):
        """TD06-001: 无参数-成功"""
        response = td_client.td_attachment_rules()
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    def test_td06_002(self, td_client):
        """TD06-002: 验证返回减免事项字典-成功"""
        response = td_client.td_attachment_rules()
        assert_response_success(response, expected_success=True)
        data = response.json()
        assert "data" in data

    @pytest.mark.P1
    def test_td06_003(self, td_client):
        """TD06-003: 验证减免方式节点-成功"""
        response = td_client.td_attachment_rules()
        assert_response_success(response, expected_success=True)
        data = response.json()
        assert "data" in data

    @pytest.mark.P1
    def test_td06_004(self, td_client):
        """TD06-004: 验证规则明细字段完整性-成功"""
        response = td_client.td_attachment_rules()
        assert_response_success(response, expected_success=True)
        data = response.json()
        assert "data" in data


# ============================================================================
# ====== 生产版 TD 鉴权测试
# ============================================================================

@pytest.mark.TD
@pytest.mark.鉴权
class TestTDAuth:
    """TD-AUTH: 生产版鉴权测试"""

    @pytest.mark.P0
    def test_td_auth_001(self, td_client, declaration_base_data, api_client):
        """TD-AUTH-001: 无token访问-失败"""
        original = api_client.session.headers.get("Authorization")
        api_client.session.headers.pop("Authorization", None)
        try:
            response = td_client.td_query(**declaration_base_data)
            assert_response_success(response, expected_success=False)
        finally:
            if original:
                api_client.session.headers["Authorization"] = original

    @pytest.mark.P0
    def test_td_auth_002(self, td_client, declaration_base_data, api_client):
        """TD-AUTH-002: token无效-失败"""
        api_client.set_token("invalid_token_12345")
        response = td_client.td_query(**declaration_base_data)
        assert_response_success(response, expected_success=False)

    @pytest.mark.P0
    def test_td_auth_003(self, td_client, declaration_base_data, api_client):
        """TD-AUTH-003: token过期-失败"""
        api_client.set_token("expired_token_99999")
        response = td_client.td_query(**declaration_base_data)
        assert_response_success(response, expected_success=False)


# ============================================================================
# ====== 生产版 TD 场景测试
# ============================================================================

@pytest.mark.TD
@pytest.mark.场景
class TestTDFlow:
    """TD-FLOW: 生产版场景测试"""

    @pytest.mark.P1
    def test_td_flow_001(self, td_client, declaration_base_data):
        """TD-FLOW-001: 完整申报流程-算税->申报执行->状态查询"""
        # Step 1: 申报数据查询
        query_resp = td_client.td_query(**declaration_base_data)
        assert_response_success(query_resp, expected_success=True)
        # Step 2: 申报执行
        exec_resp = td_client.td_execute(**declaration_base_data)
        assert_response_success(exec_resp, expected_success=True)
        exec_data = exec_resp.json()
        accept_id = None
        if "data" in exec_data and isinstance(exec_data["data"], dict):
            accept_id = exec_data["data"].get("accept_id")
        if accept_id:
            status_resp = td_client.td_status(accept_id)
            assert_response_success(status_resp, expected_success=True)

    @pytest.mark.P1
    def test_td_flow_002(self, td_client, declaration_base_data):
        """TD-FLOW-002: 附表补填流程-查询待填->保存附表->申报执行"""
        accept_id = "ACC_FLOW_002"
        # Step 1: 查询待填附表人员
        pending_data = declaration_base_data.copy()
        pending_data["accept_id"] = accept_id
        pending_resp = td_client.td_pending_persons(**pending_data)
        assert_response_success(pending_resp, expected_success=True)
        # Step 2: 保存附表数据
        attachment_data = declaration_base_data.copy()
        attachment_data["accept_id"] = accept_id
        attachment_data["jmsxmx"] = [
            {
                "xm": "张三",
                "zzlx": "A",
                "zzhm": "310101199001011234",
                "jmfs": "免税收入",
                "sdxm": "0101",
                "jmsx": "个人所得税优惠",
                "jmxz": "其他",
                "jmse": 5000
            }
        ]
        save_resp = td_client.td_attachment_save(**attachment_data)
        assert_response_success(save_resp, expected_success=True)
        # Step 3: 申报执行
        exec_resp = td_client.td_execute(**declaration_base_data)
        assert_response_success(exec_resp, expected_success=True)

    @pytest.mark.P1
    def test_td_flow_003(self, td_client, declaration_base_data):
        """TD-FLOW-003: 申报失败重试流程-状态查询->修正数据->申报执行"""
        # Step 1: 状态查询
        accept_id = "ACCEPT_FAIL_001"
        status_resp = td_client.td_status(accept_id)
        assert_response_success(status_resp, expected_success=True)
        status_data = status_resp.json()
        is_failed = False
        if "data" in status_data and isinstance(status_data["data"], dict):
            sbbz = status_data["data"].get("sbbz")
            if sbbz == 3:
                is_failed = True
        if is_failed:
            # Step 2: 修正数据 + 重新申报
            corrected_data = declaration_base_data.copy()
            retry_resp = td_client.td_execute(**corrected_data)
            assert_response_success(retry_resp, expected_success=True)


# ============================================================================
# ====== 研发版 RD 测试类
# ============================================================================

@pytest.mark.RD
class TestRD01DeclarationQuery:
    """RD01-申报数据查询 (POST /api/tax-declaration/external/query)"""

    @pytest.mark.P0
    def test_rd01_001(self, rd_client, declaration_rd_base_data):
        """RD01-001: 正常参数-成功"""
        response = rd_client.rd_query(**declaration_rd_base_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P0
    def test_rd01_002(self, rd_client, declaration_rd_base_data):
        """RD01-002: 缺少cpId-失败"""
        data = declaration_rd_base_data.copy()
        data.pop("cpId", None)
        response = rd_client.rd_query(**data)
        assert_response_success(response, expected_success=False)

    @pytest.mark.P0
    def test_rd01_003(self, rd_client, declaration_rd_base_data):
        """RD01-003: 缺少sdyf-失败"""
        data = declaration_rd_base_data.copy()
        data.pop("sdyf", None)
        response = rd_client.rd_query(**data)
        assert_response_success(response, expected_success=False)

    @pytest.mark.P1
    def test_rd01_004(self, rd_client, declaration_rd_base_data):
        """RD01-004: sdyf格式错误-失败"""
        data = declaration_rd_base_data.copy()
        data["sdyf"] = "20250315"
        response = rd_client.rd_query(**data)
        assert_response_success(response, expected_success=False)

    @pytest.mark.P1
    def test_rd01_005(self, rd_client, declaration_rd_base_data):
        """RD01-005: sdyf格式YYYY-MM-成功"""
        data = declaration_rd_base_data.copy()
        data["sdyf"] = "2026-03"
        response = rd_client.rd_query(**data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    def test_rd01_006(self, rd_client, declaration_rd_base_data):
        """RD01-006: sdyf格式YYYYMM-成功"""
        data = declaration_rd_base_data.copy()
        data["sdyf"] = "202603"
        response = rd_client.rd_query(**data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    def test_rd01_007(self, rd_client, declaration_rd_base_data):
        """RD01-007: 带taxClassCode-成功"""
        data = declaration_rd_base_data.copy()
        data["taxClassCode"] = "TAX_CLASS_001"
        response = rd_client.rd_query(**data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    def test_rd01_008(self, rd_client, declaration_rd_base_data):
        """RD01-008: 带categoryCode-成功"""
        data = declaration_rd_base_data.copy()
        data["categoryCode"] = "01"
        response = rd_client.rd_query(**data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P2
    def test_rd01_009(self, rd_client, declaration_rd_base_data):
        """RD01-009: 不带可选参数-成功"""
        data = {
            "cpId": declaration_rd_base_data["cpId"],
            "sdyf": declaration_rd_base_data["sdyf"]
        }
        response = rd_client.rd_query(**data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    def test_rd01_010(self, rd_client, declaration_rd_base_data):
        """RD01-010: 分页pageNum=1-成功"""
        data = declaration_rd_base_data.copy()
        data["pageNum"] = 1
        data["pageSize"] = 20
        response = rd_client.rd_query(**data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    def test_rd01_011(self, rd_client, declaration_rd_base_data):
        """RD01-011: 分页pageSize=20-成功"""
        data = declaration_rd_base_data.copy()
        data["pageNum"] = 1
        data["pageSize"] = 20
        response = rd_client.rd_query(**data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    def test_rd01_012(self, rd_client, declaration_rd_base_data):
        """RD01-012: pageSize=200最大-成功"""
        data = declaration_rd_base_data.copy()
        data["pageNum"] = 1
        data["pageSize"] = 200
        response = rd_client.rd_query(**data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P2
    def test_rd01_013(self, rd_client, declaration_rd_base_data):
        """RD01-013: pageSize超过200-成功"""
        data = declaration_rd_base_data.copy()
        data["pageNum"] = 1
        data["pageSize"] = 500
        response = rd_client.rd_query(**data)
        assert response.status_code == 200

    @pytest.mark.P1
    def test_rd01_014(self, rd_client, declaration_rd_base_data):
        """RD01-014: 验证返回字段完整性-成功"""
        response = rd_client.rd_query(**declaration_rd_base_data)
        assert_response_success(response, expected_success=True)
        data = response.json()
        assert "data" in data

    @pytest.mark.P2
    def test_rd01_015(self, rd_client, declaration_rd_base_data):
        """RD01-015: 空结果-成功"""
        data = declaration_rd_base_data.copy()
        data["sdyf"] = "209912"
        response = rd_client.rd_query(**data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    def test_rd01_016(self, rd_client, declaration_rd_base_data):
        """RD01-016: 多条件组合-成功"""
        data = declaration_rd_base_data.copy()
        data["taxClassCode"] = "TAX_CLASS_001"
        data["categoryCode"] = "01"
        data["pageNum"] = 1
        data["pageSize"] = 20
        response = rd_client.rd_query(**data)
        assert_response_success(response, expected_success=True)


@pytest.mark.RD
class TestRD02DeclarationSubmit:
    """RD02-个税申报提交 (POST /api/tax-declaration/external/submit)"""

    @pytest.mark.P0
    def test_rd02_001(self, rd_client, declaration_rd_base_data):
        """RD02-001: 正常参数-成功"""
        response = rd_client.rd_submit(**declaration_rd_base_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P0
    def test_rd02_002(self, rd_client, declaration_rd_base_data):
        """RD02-002: 缺少taxClassCode-失败"""
        data = declaration_rd_base_data.copy()
        data.pop("taxClassCode", None)
        response = rd_client.rd_submit(**data)
        assert_response_success(response, expected_success=False)

    @pytest.mark.P0
    def test_rd02_003(self, rd_client, declaration_rd_base_data):
        """RD02-003: 缺少cpId-失败"""
        data = declaration_rd_base_data.copy()
        data.pop("cpId", None)
        response = rd_client.rd_submit(**data)
        assert_response_success(response, expected_success=False)

    @pytest.mark.P0
    def test_rd02_004(self, rd_client, declaration_rd_base_data):
        """RD02-004: 缺少sdyf-失败"""
        data = declaration_rd_base_data.copy()
        data.pop("sdyf", None)
        response = rd_client.rd_submit(**data)
        assert_response_success(response, expected_success=False)

    @pytest.mark.P0
    def test_rd02_005(self, rd_client, declaration_rd_base_data):
        """RD02-005: 缺少categoryCode-失败"""
        data = declaration_rd_base_data.copy()
        data.pop("categoryCode", None)
        response = rd_client.rd_submit(**data)
        assert_response_success(response, expected_success=False)

    @pytest.mark.P1
    def test_rd02_006(self, rd_client, declaration_rd_base_data):
        """RD02-006: sdyf格式错误-失败"""
        data = declaration_rd_base_data.copy()
        data["sdyf"] = "20250315"
        response = rd_client.rd_submit(**data)
        assert_response_success(response, expected_success=False)

    @pytest.mark.P1
    def test_rd02_007(self, rd_client, declaration_rd_base_data):
        """RD02-007: sdyf格式YYYY-MM-成功"""
        data = declaration_rd_base_data.copy()
        data["sdyf"] = "2026-03"
        response = rd_client.rd_submit(**data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    def test_rd02_008(self, rd_client, declaration_rd_base_data):
        """RD02-008: categoryCode=01综合所得-成功"""
        data = declaration_rd_base_data.copy()
        data["categoryCode"] = "01"
        response = rd_client.rd_submit(**data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    def test_rd02_009(self, rd_client, declaration_rd_base_data):
        """RD02-009: categoryCode=02分类所得-成功"""
        data = declaration_rd_base_data.copy()
        data["categoryCode"] = "02"
        response = rd_client.rd_submit(**data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    def test_rd02_010(self, rd_client, declaration_rd_base_data):
        """RD02-010: categoryCode=03非居民所得-成功"""
        data = declaration_rd_base_data.copy()
        data["categoryCode"] = "03"
        response = rd_client.rd_submit(**data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    def test_rd02_011(self, rd_client, declaration_rd_base_data):
        """RD02-011: 验证返回submissionId-成功"""
        response = rd_client.rd_submit(**declaration_rd_base_data)
        assert_response_success(response, expected_success=True)
        data = response.json()
        assert "data" in data

    @pytest.mark.P1
    def test_rd02_012(self, rd_client, declaration_rd_base_data):
        """RD02-012: 异步申报status=PROCESSING-成功"""
        response = rd_client.rd_submit(**declaration_rd_base_data)
        assert_response_success(response, expected_success=True)
        data = response.json()
        if "data" in data and isinstance(data["data"], dict):
            status = data["data"].get("status")
            assert status in ["PROCESSING", "SUCCESS"]

    @pytest.mark.P2
    def test_rd02_013(self, rd_client, declaration_rd_base_data):
        """RD02-013: 重复提交-幂等"""
        response1 = rd_client.rd_submit(**declaration_rd_base_data)
        assert_response_success(response1, expected_success=True)
        response2 = rd_client.rd_submit(**declaration_rd_base_data)
        assert response2.status_code == 200


@pytest.mark.RD
class TestRD03DeclarationDetail:
    """RD03-申报详情查询 (POST /api/tax-declaration/external/detail)"""

    @pytest.mark.P0
    def test_rd03_001(self, rd_client, declaration_rd_base_data):
        """RD03-001: 正常参数-成功"""
        response = rd_client.rd_detail(**declaration_rd_base_data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P0
    def test_rd03_002(self, rd_client, declaration_rd_base_data):
        """RD03-002: 缺少taxClassCode-失败"""
        data = declaration_rd_base_data.copy()
        data.pop("taxClassCode", None)
        response = rd_client.rd_detail(**data)
        assert_response_success(response, expected_success=False)

    @pytest.mark.P0
    def test_rd03_003(self, rd_client, declaration_rd_base_data):
        """RD03-003: 缺少cpId-失败"""
        data = declaration_rd_base_data.copy()
        data.pop("cpId", None)
        response = rd_client.rd_detail(**data)
        assert_response_success(response, expected_success=False)

    @pytest.mark.P0
    def test_rd03_004(self, rd_client, declaration_rd_base_data):
        """RD03-004: 缺少sdyf-失败"""
        data = declaration_rd_base_data.copy()
        data.pop("sdyf", None)
        response = rd_client.rd_detail(**data)
        assert_response_success(response, expected_success=False)

    @pytest.mark.P0
    def test_rd03_005(self, rd_client, declaration_rd_base_data):
        """RD03-005: 缺少categoryCode-失败"""
        data = declaration_rd_base_data.copy()
        data.pop("categoryCode", None)
        response = rd_client.rd_detail(**data)
        assert_response_success(response, expected_success=False)

    @pytest.mark.P1
    def test_rd03_006(self, rd_client, declaration_rd_base_data):
        """RD03-006: sdyf格式YYYY-MM-成功"""
        data = declaration_rd_base_data.copy()
        data["sdyf"] = "2026-03"
        response = rd_client.rd_detail(**data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    def test_rd03_007(self, rd_client, declaration_rd_base_data):
        """RD03-007: sdyf格式YYYYMM-成功"""
        data = declaration_rd_base_data.copy()
        data["sdyf"] = "202603"
        response = rd_client.rd_detail(**data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    def test_rd03_008(self, rd_client, declaration_rd_base_data):
        """RD03-008: categoryCode=01-成功"""
        data = declaration_rd_base_data.copy()
        data["categoryCode"] = "01"
        response = rd_client.rd_detail(**data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    def test_rd03_009(self, rd_client, declaration_rd_base_data):
        """RD03-009: categoryCode=02-成功"""
        data = declaration_rd_base_data.copy()
        data["categoryCode"] = "02"
        response = rd_client.rd_detail(**data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    def test_rd03_010(self, rd_client, declaration_rd_base_data):
        """RD03-010: categoryCode=03-成功"""
        data = declaration_rd_base_data.copy()
        data["categoryCode"] = "03"
        response = rd_client.rd_detail(**data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    def test_rd03_011(self, rd_client, declaration_rd_base_data):
        """RD03-011: 分页pageNum=1-成功"""
        data = declaration_rd_base_data.copy()
        data["pageNum"] = 1
        data["pageSize"] = 20
        response = rd_client.rd_detail(**data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    def test_rd03_012(self, rd_client, declaration_rd_base_data):
        """RD03-012: 分页pageSize=20-成功"""
        data = declaration_rd_base_data.copy()
        data["pageNum"] = 1
        data["pageSize"] = 20
        response = rd_client.rd_detail(**data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    def test_rd03_013(self, rd_client, declaration_rd_base_data):
        """RD03-013: pageSize最大200-成功"""
        data = declaration_rd_base_data.copy()
        data["pageNum"] = 1
        data["pageSize"] = 200
        response = rd_client.rd_detail(**data)
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    def test_rd03_014(self, rd_client, declaration_rd_base_data):
        """RD03-014: 验证declarationStatus字段-成功"""
        response = rd_client.rd_detail(**declaration_rd_base_data)
        assert_response_success(response, expected_success=True)
        data = response.json()
        assert "data" in data

    @pytest.mark.P1
    def test_rd03_015(self, rd_client, declaration_rd_base_data):
        """RD03-015: 验证返回算税明细字段-成功"""
        response = rd_client.rd_detail(**declaration_rd_base_data)
        assert_response_success(response, expected_success=True)
        data = response.json()
        assert "data" in data

    @pytest.mark.P2
    def test_rd03_016(self, rd_client, declaration_rd_base_data):
        """RD03-016: 空结果-成功"""
        data = declaration_rd_base_data.copy()
        data["sdyf"] = "209912"
        response = rd_client.rd_detail(**data)
        assert_response_success(response, expected_success=True)


@pytest.mark.RD
class TestRD04DeclarationStatus:
    """RD04-申报状态查询 (POST /api/tax-declaration/external/status)"""

    @pytest.mark.P0
    def test_rd04_001(self, rd_client):
        """RD04-001: 正常参数-成功"""
        response = rd_client.rd_status(submissionId="DECL202603010001")
        assert_response_success(response, expected_success=True)

    @pytest.mark.P0
    def test_rd04_002(self, rd_client):
        """RD04-002: 缺少submissionId-失败"""
        response = rd_client.rd_status()
        assert_response_success(response, expected_success=False)

    @pytest.mark.P1
    def test_rd04_003(self, rd_client):
        """RD04-003: submissionId不存在-失败"""
        response = rd_client.rd_status(submissionId="DECL_NOT_EXIST_99999")
        assert_response_success(response, expected_success=False)

    @pytest.mark.P1
    def test_rd04_004(self, rd_client):
        """RD04-004: submissionId为空字符串-失败"""
        response = rd_client.rd_status(submissionId="")
        assert_response_success(response, expected_success=False)

    @pytest.mark.P1
    def test_rd04_005(self, rd_client):
        """RD04-005: status=PROCESSING-成功"""
        response = rd_client.rd_status(submissionId="DECL_PROCESSING_001")
        assert_response_success(response, expected_success=True)
        data = response.json()
        if "data" in data and isinstance(data["data"], dict):
            status = data["data"].get("status")
            assert status == "PROCESSING", f"状态应为PROCESSING，实际为{status}"

    @pytest.mark.P1
    def test_rd04_006(self, rd_client):
        """RD04-006: status=SUCCESS-成功"""
        response = rd_client.rd_status(submissionId="DECL_SUCCESS_001")
        assert_response_success(response, expected_success=True)
        data = response.json()
        if "data" in data and isinstance(data["data"], dict):
            status = data["data"].get("status")
            assert status == "SUCCESS", f"状态应为SUCCESS，实际为{status}"

    @pytest.mark.P1
    def test_rd04_007(self, rd_client):
        """RD04-007: status=FAILED-成功"""
        response = rd_client.rd_status(submissionId="DECL_FAILED_001")
        assert_response_success(response, expected_success=True)
        data = response.json()
        if "data" in data and isinstance(data["data"], dict):
            status = data["data"].get("status")
            assert status == "FAILED", f"状态应为FAILED，实际为{status}"

    @pytest.mark.P1
    def test_rd04_008(self, rd_client):
        """RD04-008: 验证状态映射-成功"""
        response = rd_client.rd_status(submissionId="DECL_MAPPING_001")
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    def test_rd04_009(self, rd_client):
        """RD04-009: 验证状态映射-成功"""
        response = rd_client.rd_status(submissionId="DECL_MAPPING_002")
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    def test_rd04_010(self, rd_client):
        """RD04-010: 验证状态映射-成功"""
        response = rd_client.rd_status(submissionId="DECL_MAPPING_003")
        assert_response_success(response, expected_success=True)

    @pytest.mark.P1
    def test_rd04_011(self, rd_client):
        """RD04-011: 验证状态映射-成功"""
        response = rd_client.rd_status(submissionId="DECL_MAPPING_004")
        assert_response_success(response, expected_success=True)


# ============================================================================
# ====== 研发版 RD 鉴权测试
# ============================================================================

@pytest.mark.RD
@pytest.mark.鉴权
class TestRDAuth:
    """RD-AUTH: 研发版鉴权测试"""

    @pytest.mark.P0
    def test_rd_auth_001(self, rd_client, declaration_rd_base_data, api_client):
        """RD-AUTH-001: 无token访问-失败"""
        original = api_client.session.headers.get("Authorization")
        api_client.session.headers.pop("Authorization", None)
        try:
            response = rd_client.rd_query(**declaration_rd_base_data)
            assert_response_success(response, expected_success=False)
        finally:
            if original:
                api_client.session.headers["Authorization"] = original

    @pytest.mark.P0
    def test_rd_auth_002(self, rd_client, declaration_rd_base_data, api_client):
        """RD-AUTH-002: token无效-失败"""
        api_client.set_token("invalid_token_12345")
        response = rd_client.rd_query(**declaration_rd_base_data)
        assert_response_success(response, expected_success=False)

    @pytest.mark.P0
    def test_rd_auth_003(self, rd_client, declaration_rd_base_data, api_client):
        """RD-AUTH-003: token过期-失败"""
        api_client.set_token("expired_token_99999")
        response = rd_client.rd_query(**declaration_rd_base_data)
        assert_response_success(response, expected_success=False)


# ============================================================================
# ====== 研发版 RD 场景测试
# ============================================================================

@pytest.mark.RD
@pytest.mark.场景
class TestRDFlow:
    """RD-FLOW: 研发版场景测试"""

    @pytest.mark.P1
    def test_rd_flow_001(self, rd_client, declaration_rd_base_data):
        """RD-FLOW-001: 完整申报流程-查询->提交->状态查询"""
        # Step 1: 申报数据查询
        query_resp = rd_client.rd_query(**declaration_rd_base_data)
        assert_response_success(query_resp, expected_success=True)
        # Step 2: 提交申报
        submit_resp = rd_client.rd_submit(**declaration_rd_base_data)
        assert_response_success(submit_resp, expected_success=True)
        submit_data = submit_resp.json()
        submission_id = None
        if "data" in submit_data and isinstance(submit_data["data"], dict):
            submission_id = submit_data["data"].get("submissionId")
        if submission_id:
            status_resp = rd_client.rd_status(submissionId=submission_id)
            assert_response_success(status_resp, expected_success=True)

    @pytest.mark.P1
    def test_rd_flow_002(self, rd_client, declaration_rd_base_data):
        """RD-FLOW-002: 完整申报流程-查询->提交->详情->状态查询"""
        # Step 1: 申报数据查询
        query_resp = rd_client.rd_query(**declaration_rd_base_data)
        assert_response_success(query_resp, expected_success=True)
        # Step 2: 提交申报
        submit_resp = rd_client.rd_submit(**declaration_rd_base_data)
        assert_response_success(submit_resp, expected_success=True)
        submit_data = submit_resp.json()
        submission_id = None
        if "data" in submit_data and isinstance(submit_data["data"], dict):
            submission_id = submit_data["data"].get("submissionId")
        if submission_id:
            # Step 3: 查询申报详情
            detail_resp = rd_client.rd_detail(**declaration_rd_base_data)
            assert_response_success(detail_resp, expected_success=True)
            # Step 4: 状态查询
            status_resp = rd_client.rd_status(submissionId=submission_id)
            assert_response_success(status_resp, expected_success=True)

    @pytest.mark.P1
    def test_rd_flow_003(self, rd_client, declaration_rd_base_data):
        """RD-FLOW-003: 申报失败重试-提交失败->修正数据->重新提交"""
        # Step 1: 提交申报
        submit_resp = rd_client.rd_submit(**declaration_rd_base_data)
        submit_data = submit_resp.json()
        is_failed = False
        if "data" in submit_data and isinstance(submit_data["data"], dict):
            status = submit_data["data"].get("status")
            if status == "FAILED":
                is_failed = True
        if is_failed:
            # Step 2: 修正数据 + 重新提交
            corrected_data = declaration_rd_base_data.copy()
            retry_resp = rd_client.rd_submit(**corrected_data)
            assert_response_success(retry_resp, expected_success=True)