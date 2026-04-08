"""
测试数据生成器 - 生成各类测试数据
"""
import random
import string
from datetime import datetime
from typing import List, Dict, Any


class DataGenerator:
    """测试数据生成工具类"""

    @staticmethod
    def random_string(length: int = 8, chars: str = None) -> str:
        """生成随机字符串"""
        if chars is None:
            chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(length))

    @staticmethod
    def random_numeric(length: int = 8) -> str:
        """生成随机数字字符串"""
        return ''.join(random.choice(string.digits) for _ in range(length))

    @staticmethod
    def random_phone() -> str:
        """生成随机手机号"""
        prefixes = ['130', '131', '132', '133', '134', '135', '136', '137', '138', '139',
                    '150', '151', '152', '153', '155', '156', '157', '158', '159',
                    '180', '181', '182', '183', '184', '185', '186', '187', '188', '189']
        return random.choice(prefixes) + ''.join(random.choice(string.digits) for _ in range(8))

    @staticmethod
    def random_id_card() -> str:
        """生成随机身份证号(18位)"""
        # 随机地区码
        area_code = random.choice(['310000', '320000', '330000', '110000', '440000'])
        # 随机出生日期(1980-2000年)
        year = random.randint(1980, 2000)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        birth_date = f"{year:04d}{month:02d}{day:02d}"
        # 随机顺序码
        seq_code = f"{random.randint(0, 999):03d}"
        # 校验码
        check_code = random.choice(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'X'])
        return f"{area_code[:2]}0{random.randint(0, 9)}{birth_date}{seq_code}{check_code}"

    @staticmethod
    def random_credit_code() -> str:
        """生成随机统一社会信用代码(18位)"""
        # 18位数字字母组合
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choice(chars) for _ in range(18))

    @staticmethod
    def random_nsrsbh() -> str:
        """生成随机纳税人识别号(18-20位)"""
        length = random.choice([15, 17, 18, 20])
        return ''.join(random.choice(string.digits) for _ in range(length))

    @staticmethod
    def random_agent_code() -> str:
        """生成随机扣缴义务人编码(4-16位字母数字)"""
        length = random.randint(4, 16)
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(length))

    @staticmethod
    def current_sdyf() -> str:
        """获取当前月份的sdyf格式(YYYYMM)"""
        return datetime.now().strftime('%Y%m')

    @staticmethod
    def next_month_sdyf() -> str:
        """获取下个月的sdyf格式"""
        from datetime import timedelta
        next_month = datetime.now() + timedelta(days=32)
        return next_month.strftime('%Y%m')

    @staticmethod
    def random_sdyf(years_back: int = 0, years_forward: int = 0) -> str:
        """生成随机sdyf"""
        from datetime import timedelta
        days_offset = random.randint(-years_back * 365, years_forward * 365)
        target_date = datetime.now() + timedelta(days=days_offset)
        return target_date.strftime('%Y%m')

    # ==================== 扣缴义务人模块数据 ====================

    @staticmethod
    def withholding_agent_create_data(**overrides) -> Dict[str, Any]:
        """生成新增扣缴义务人请求数据"""
        data = {
            "cpId": 1001,
            "agentCode": f"AG{random.randint(10000, 99999)}",
            "agentName": f"测试公司{random.randint(1000, 9999)}",
            "nsrsbh": DataGenerator.random_nsrsbh(),
            "sbmm": "12345678",
            "passwordVerificationType": "01",
            "areaid": "310000",
            "djxhid": f"DJXH{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "zgswjg": "国家税务总局上海市税务局",
            "bmbh": f"BM{random.randint(100, 999)}"
        }
        data.update(overrides)
        return data

    @staticmethod
    def withholding_agent_update_data(**overrides) -> Dict[str, Any]:
        """生成更新扣缴义务人请求数据"""
        data = {
            "cpId": 1001,
            "taxClassCode": "TC001",
            "agentName": f"更名公司{random.randint(1000, 9999)}",
            "sbmm": "87654321"
        }
        data.update(overrides)
        return data

    @staticmethod
    def withholding_agent_list_query(**overrides) -> Dict[str, Any]:
        """生成扣缴义务人列表查询参数"""
        data = {
            "cpId": 1001,
            "pageNum": 1,
            "pageSize": 10
        }
        data.update(overrides)
        return data

    # ==================== 人员报送模块数据 ====================

    @staticmethod
    def person_create_data(**overrides) -> Dict[str, Any]:
        """生成新增人员请求数据"""
        data = {
            "cpId": "1001",
            "xm": f"员工{random.randint(1000, 9999)}",
            "zzlx": "A",
            "zzhm": DataGenerator.random_id_card(),
            "kjsrybm": f"AG{random.randint(100, 999)}",
            "kjsry": "XX科技有限公司",
            "sfgy": "01",
            "sdyf": DataGenerator.current_sdyf(),
            "taxClassCode": f"PLAN_{DataGenerator.random_string(12)}",
            "lxdh": DataGenerator.random_phone()
        }
        data.update(overrides)
        return data

    @staticmethod
    def person_query_data(**overrides) -> Dict[str, Any]:
        """生成人员查询参数"""
        data = {
            "cpId": "1001",
            "pageNum": 1,
            "pageSize": 20
        }
        data.update(overrides)
        return data

    @staticmethod
    def person_batch_ids(count: int = 3) -> List[str]:
        """生成批量人员ID列表"""
        return [f"PSN{datetime.now().strftime('%Y%m%d')}{str(i).zfill(4)}"
                for i in range(1, count + 1)]

    # ==================== 个税计算模块数据 ====================

    @staticmethod
    def salary_import_data(**overrides) -> Dict[str, Any]:
        """生成薪酬数据导入请求"""
        data = {
            "cpId": 1001,
            "nsrsbh": DataGenerator.random_nsrsbh(),
            "taxClassCode": f"TC{DataGenerator.random_numeric(6)}",
            "sdyf": DataGenerator.current_sdyf(),
            "dysd": [
                {
                    "xm": f"员工{i}",
                    "zzlx": "A",
                    "zzhm": DataGenerator.random_id_card(),
                    "itemCode": "01010101",
                    "pch": i,
                    "sre": round(random.uniform(3000, 50000), 2),
                    "jbylaobxf": round(random.uniform(200, 2000), 2),
                    "jbylbxf": round(random.uniform(50, 500), 2),
                    "sybxf": round(random.uniform(20, 200), 2),
                    "zfgjj": round(random.uniform(200, 2000), 2)
                }
                for i in range(1, 3)
            ]
        }
        data.update(overrides)
        return data

    @staticmethod
    def salary_list_query(**overrides) -> Dict[str, Any]:
        """生成薪酬数据查询参数"""
        data = {
            "cpId": 1001,
            "taxClassCode": f"TC{DataGenerator.random_numeric(6)}",
            "sdyf": DataGenerator.current_sdyf(),
            "pageNum": 1,
            "pageSize": 20
        }
        data.update(overrides)
        return data

    @staticmethod
    def zero_wage_data(**overrides) -> Dict[str, Any]:
        """生成0工资记录请求"""
        data = {
            "cpId": 1001,
            "taxClassCode": f"TC{DataGenerator.random_numeric(6)}",
            "sdyf": DataGenerator.current_sdyf(),
            "personIds": [DataGenerator.random_id_card() for _ in range(2)]
        }
        data.update(overrides)
        return data

    @staticmethod
    def tax_compute_trigger_data(**overrides) -> Dict[str, Any]:
        """生成触发算税请求"""
        data = {
            "cpId": 1001,
            "taxClassCode": f"TC{DataGenerator.random_numeric(6)}",
            "sdyf": DataGenerator.current_sdyf(),
            "triggerType": "BATCH",
            "computeMode": "SKJS"
        }
        data.update(overrides)
        return data

    @staticmethod
    def tax_compute_retry_data(**overrides) -> Dict[str, Any]:
        """生成重新算税请求"""
        data = {
            "cpId": 1001,
            "taxClassCode": f"TC{DataGenerator.random_numeric(6)}",
            "sdyf": DataGenerator.current_sdyf()
        }
        data.update(overrides)
        return data

    # ==================== 个税申报模块数据 ====================

    @staticmethod
    def declaration_query_data(**overrides) -> Dict[str, Any]:
        """生成申报查询请求"""
        data = {
            "agentCode": f"AG{random.randint(1000, 9999)}",
            "sdyf": DataGenerator.current_sdyf(),
            "sdlx": "综合所得",
            "areaid": "310000",
            "djxhid": f"DJXH{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "sbmm": "12345678"
        }
        data.update(overrides)
        return data

    @staticmethod
    def declaration_execute_data(**overrides) -> Dict[str, Any]:
        """生成申报执行请求"""
        data = {
            "agentCode": f"AG{random.randint(1000, 9999)}",
            "sdyf": DataGenerator.current_sdyf(),
            "sdlx": "综合所得",
            "areaid": "310000",
            "djxhid": f"DJXH{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "sbmm": "12345678"
        }
        data.update(overrides)
        return data

    # ==================== 研发版申报数据 ====================

    @staticmethod
    def declaration_ext_query_data(**overrides) -> Dict[str, Any]:
        """生成研发版申报查询请求"""
        data = {
            "taxClassCode": f"TAX_CLASS_{DataGenerator.random_numeric(6)}",
            "cpId": 1001,
            "sdyf": datetime.now().strftime('%Y-%m'),
            "categoryCode": "01",
            "pageNum": 1,
            "pageSize": 20
        }
        data.update(overrides)
        return data

    @staticmethod
    def declaration_ext_submit_data(**overrides) -> Dict[str, Any]:
        """生成研发版申报提交请求"""
        data = {
            "taxClassCode": f"TAX_CLASS_{DataGenerator.random_numeric(6)}",
            "cpId": 1001,
            "sdyf": datetime.now().strftime('%Y-%m'),
            "categoryCode": "01"
        }
        data.update(overrides)
        return data
