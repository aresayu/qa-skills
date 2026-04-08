# API 接口测试用例总览

## 文档信息
- 版本：v1.0
- 创建日期：2026-04-02
- 更新日期：2026-04-02

---

## 索引导航

| 模块 | 目录 | 接口数量 | 用例数量 |
|------|------|----------|----------|
| 概述 | [10-概述](./10-概述/10-测试用例概述.md) | - | - |
| 扣缴义务人模块 | [20-扣缴义务人模块](./20-扣缴义务人模块/20-测试用例.md) | 9 | 60+ |
| 人员报送模块 | [30-人员报送模块](./30-人员报送模块/30-测试用例.md) | 7 | 50+ |
| 个税计算模块 | [40-个税计算模块](./40-个税计算模块/40-测试用例.md) | 9 | 80+ |
| 个税申报模块 | [50-个税申报模块](./50-个税申报模块/50-测试用例.md) | 6+4 | 50+50+ |
| └─ 旧版 | [50-测试用例.md](./50-个税申报模块/50-测试用例.md) | 6 | 50+ |
| └─ 研发版 | [51-研发版测试用例.md](./50-个税申报模块/51-研发版测试用例.md) | 4 | 40+ |

---

## 测试用例统计

| 模块 | 正向用例 | 反向用例 | 边界值用例 | 鉴权用例 | 分页用例 | 其他 |
|------|----------|----------|------------|----------|----------|------|
| 扣缴义务人 | ~15 | ~20 | ~10 | 3 | 2 | 幂等 |
| 人员报送 | ~15 | ~15 | ~10 | 3 | 2 | 幂等 |
| 个税计算 | ~20 | ~30 | ~15 | 3 | 5 | 幂等 |
| 个税申报-旧版 | ~15 | ~20 | ~5 | 3 | - | 场景 |
| 个税申报-研发版 | ~12 | ~8 | ~5 | 3 | 4 | 场景 |

---

## 接口覆盖概览

### 扣缴义务人模块 (9个接口)
1. 新增扣缴义务人 - POST /api/v2/tax/withholding-agent/create
2. 更新扣缴义务人 - POST /api/v2/tax/withholding-agent/update
3. 获取扣缴义务人详情 - POST /api/v2/tax/withholding-agent/detail
4. 查询扣缴义务人列表 - POST /api/v2/tax/withholding-agent/list
5. 搜索扣缴义务人 - POST /api/v2/tax/withholding-agent/query
6. 删除扣缴义务人 - POST /api/v2/tax/withholding-agent/delete
7. 获取报税地区列表 - POST /api/v2/tax/withholding-agent/tax-regions
8. 预获取税局任务ID - POST /api/v2/tax/withholding-agent/tax-authority
9. 根据任务ID查询税务机关 - POST /api/v2/tax/withholding-agent/tax-authority-by-taskId

### 人员报送模块 (7个接口)
1. 查询人员列表 - POST /api/v2/tax/person/query
2. 新增人员 - POST /api/v2/tax/person/create
3. 修改人员 - POST /api/v2/tax/person/update
4. 删除人员 - POST /api/v2/tax/person/delete
5. 批量删除人员 - POST /api/v2/tax/person/batch-delete
6. 单个报送人员 - POST /api/v2/tax/person/submit
7. 批量报送人员 - POST /api/v2/tax/person/batch-submit

### 个税计算模块 (9个接口)
1. 薪酬数据导入 - POST /api/v2/tax/salaryData/import
2. 薪酬数据查询 - POST /api/v2/tax/salaryData/list
3. 生成0工资记录 - POST /api/v2/tax/salaryData/zeroWage
4. 触发算税 - POST /api/v2/tax/taxCompute/trigger
5. 重新触发算税 - POST /api/v2/tax/taxCompute/retry
6. 算税结果查询 - POST /api/v2/tax/taxCompute/result/list
7. 算税汇总统计 - POST /api/v2/tax/taxCompute/result/summary
8. 算税记录详情 - POST /api/v2/tax/taxCompute/result/detail
9. 导出算税结果 - POST /api/v2/tax/taxCompute/result/export

### 个税申报模块 (6+4=10个接口)

**旧版 (6个接口)**
1. 申报数据查询服务 - POST /api/v2/tax/declaration/query
2. 个税申报执行服务 - POST /api/v2/tax/declaration/execute
3. 申报状态查询服务 - GET /api/v2/tax/declaration/status/{accept_id}
4. 待填附表人员查询服务 - POST /api/v2/tax/declaration/pending-persons
5. 附表人员数据保存服务 - POST /api/v2/tax/declaration/attachment/save
6. 附表规则字典查询服务 - POST /api/v2/tax/declaration/attachment/rules

**研发版 (4个接口)**
1. 申报数据查询 - POST /api/tax-declaration/external/query
2. 个税申报提交 - POST /api/tax-declaration/external/submit
3. 申报详情查询 - POST /api/tax-declaration/external/detail
4. 申报状态查询 - POST /api/tax-declaration/external/status

---

## 用例设计方法论

### 1. 正向测试 (Happy Path)
- 验证接口在正常参数下的成功响应
- 覆盖核心业务逻辑

### 2. 反向测试 (Negative)
- 必填参数缺失
- 参数类型错误
- 参数格式错误
- 业务规则违背

### 3. 边界值测试 (Boundary)
- 长度边界：最小值、最大值、刚好超界
- 数量边界：0、最大数量、空数组
- 格式边界：最小格式、最大格式

### 4. 鉴权测试 (Authentication)
- 无token访问
- token无效
- token过期

### 5. 分页测试 (Pagination)
- pageNum分页
- pageSize分页
- 最大pageSize验证

### 6. 幂等测试 (Idempotency)
- 重复操作
- 重复删除

### 7. 场景测试 (Scenario)
- 完整业务流程
- 状态流转
- 多接口组合

---

## 优先级定义

| 优先级 | 说明 |
|--------|------|
| P0 | 核心功能,必须覆盖 |
| P1 | 重要功能,建议覆盖 |
| P2 | 边缘功能,可选覆盖 |

---

## 生成依据

- 源文档：`/home/openclaw-developer/.openclaw/workspace-developer/API/`
- 生成工具：new-api-testcase-generator
- 技能版本：v1.0
