#!/usr/bin/env python3
# -*- coding: utf-8 -*-

with open('/home/openclaw-developer/.openclaw/workspace-developer/testcase/api/20-扣缴义务人模块/20-测试用例.md', 'r', encoding='utf-8') as f:
    content = f.read()

old_text_start = '#### WA02-005 更新扣缴义务人-修改agentName-成功'
idx = content.find(old_text_start)
print(f"oldText starts at: {idx}, file length: {len(content)}")

new_content_to_append = """
#### WA02-005 更新扣缴义务人-修改agentName-成功

| 字段 | 值 |
|------|-----|
| 用例编号 | WA02-005 |
| 用例标题 | 更新扣缴义务人-修改agentName-成功 |
| 接口路径 | POST /api/v2/tax/withholding-agent/update |
| 用例类型 | 正向 |
| 优先级 | P1 |
| 前置条件 | 已存在taxClassCode="TC001"的扣缴义务人 |
| 请求参数 | ```json { "cpId": 1001, "taxClassCode": "TC001", "agentName": "XX科技有限公司（更名）" }``` |
| 预期结果 | HTTP 200, success=true, msg="更新成功", data.agentName已更新为"XX科技有限公司（更名）" |

#### WA02-006 更新扣缴义务人-修改sbmm-成功

| 字段 | 值 |
|------|-----|
| 用例编号 | WA02-006 |
| 用例标题 | 更新扣缴义务人-修改sbmm-成功 |
| 接口路径 | POST /api/v2/tax/withholding-agent/update |
| 用例类型 | 正向 |
| 优先级 | P1 |
| 前置条件 | 已存在taxClassCode="TC001"的扣缴义务人 |
| 请求参数 | ```json { "cpId": 1001, "taxClassCode": "TC001", "sbmm": "newPassword123" }``` |
| 预期结果 | HTTP 200, success=true, msg="更新成功", sbmm已更新 |

#### WA02-007 更新扣缴义务人-修改areaid-成功

| 字段 | 值 |
|------|-----|
| 用例编号 | WA02-007 |
| 用例标题 | 更新扣缴义务人-修改areaid-成功 |
| 接口路径 | POST /api/v2/tax/withholding-agent/update |
| 用例类型 | 正向 |
| 优先级 | P1 |
| 前置条件 | 已存在taxClassCode="TC001"的扣缴义务人 |
| 请求参数 | ```json { "cpId": 1001, "taxClassCode": "TC001", "areaid": "320500" }``` |
| 预期结果 | HTTP 200, success=true, msg="更新成功", areaid已更新为"320500" |

#### WA02-008 更新扣缴义务人-sbmm长度不足8位-失败

| 字段 | 值 |
|------|-----|
| 用例编号 | WA02-008 |
| 用例标题 | 更新扣缴义务人-sbmm长度不足8位-失败 |
| 接口路径 | POST /api/v2/tax/withholding-agent/update |
| 用例类型 | 边界值 |
| 优先级 | P1 |
| 前置条件 | 已存在taxClassCode="TC001"的扣缴义务人 |
| 请求参数 | ```json { "cpId": 1001, "taxClassCode": "TC001", "sbmm": "1234567" }``` |
| 预期结果 | HTTP 200, success=false, 提示sbmm长度不足(需8-20位) |

#### WA02-009 更新扣缴义务人-sbmm长度超过20位-失败

| 字段 | 值 |
|------|-----|
| 用例编号 | WA02-009 |
| 用例标题 | 更新扣缴义务人-sbmm长度超过20位-失败 |
| 接口路径 | POST /api/v2/tax/withholding-agent/update |
| 用例类型 | 边界值 |
| 优先级 | P1 |
| 前置条件 | 已存在taxClassCode="TC001"的扣缴义务人 |
| 请求参数 | ```json { "cpId": 1001, "taxClassCode": "TC001", "sbmm": "123456789012345678901" }``` |
| 预期结果 | HTTP 200, success=false, 提示sbmm长度超限(需8-20位) |

#### WA02-010 更新扣缴义务人-areaid包含非数字-失败

| 字段 | 值 |
|------|-----|
| 用例编号 | WA02-010 |
| 用例标题 | 更新扣缴义务人-areaid包含非数字-失败 |
| 接口路径 | POST /api/v2/tax/withholding-agent/update |
| 用例类型 | 反向 |
| 优先级 | P1 |
| 前置条件 | 已存在taxClassCode="TC001"的扣缴义务人 |
| 请求参数 | ```json { "cpId": 1001, "taxClassCode": "TC001", "areaid": "31000A" }``` |
| 预期结果 | HTTP 200, success=false, 提示areaid必须为6位数字 |

#### WA02-011 更新扣缴义务人-nsrsbh尝试修改-失败

| 字段 | 值 |
|------|-----|
| 用例编号 | WA02-011 |
| 用例标题 | 更新扣缴义务人-nsrsbh尝试修改-失败 |
| 接口路径 | POST /api/v2/tax/withholding-agent/update |
| 用例类型 | 反向 |
| 优先级 | P1 |
| 前置条件 | 已存在taxClassCode="TC001"的扣缴义务人 |
| 请求参数 | ```json { "cpId": 1001, "taxClassCode": "TC001", "nsrsbh": "91310000XXXXXXXX2K" }``` |
| 预期结果 | HTTP 200, success=false, 提示nsrsbh不允许修改 |

#### WA02-012 更新扣缴义务人-不存在的taxClassCode-失败

| 字段 | 值 |
|------|-----|
| 用例编号 | WA02-012 |
| 用例标题 | 更新扣缴义务人-不存在的taxClassCode-失败 |
| 接口路径 | POST /api/v2/tax/withholding-agent/update |
| 用例类型 | 反向 |
| 优先级 | P1 |
| 请求参数 | ```json { "cpId": 1001, "taxClassCode": "INVALID_TC", "agentName": "XX科技有限公司（更名）" }``` |
| 预期结果 | HTTP 200, success=false, 提示taxClassCode不存在 |

---

## 03 获取扣缴义务人详情

**接口路径**：`POST /api/v2/tax/withholding-agent/detail`

### 用例列表

| 用例编号 | 用例标题 | 用例类型 | 优先级 |
|----------|----------|----------|--------|
| WA03-001 | 获取扣缴义务人详情-正常参数-成功 | 正向 | P0 |
| WA03-002 | 获取扣缴义务人详情-缺少cpId-失败 | 反向 | P0 |
| WA03-003 | 获取扣缴义务人详情-缺少taxClassCode-失败 | 反向 | P0 |
| WA03-004 | 获取扣缴义务人详情-taxClassCode不存在-失败 | 反向 | P1 |
| WA03-005 | 获取扣缴义务人详情-验证返回完整字段-成功 | 正向 | P1 |

### 详细用例

#### WA03-001 获取扣缴义务人详情-正常参数-成功

| 字段 | 值 |
|------|-----|
| 用例编号 | WA03-001 |
| 用例标题 | 获取扣缴义务人详情-正常参数-成功 |
| 接口路径 | POST /api/v2/tax/withholding-agent/detail |
| 用例类型 | 正向 |
| 优先级 | P0 |
| 前置条件 | 已存在taxClassCode="TC001"的扣缴义务人 |
| 请求参数 | ```json { "cpId": 1001, "taxClassCode": "TC001" }``` |
| 预期结果 | HTTP 200, success=true, data包含agentCode/agentName/nsrsbh/areaid/zgswjg等完整信息 |

#### WA03-002 获取扣缴义务人详情-缺少cpId-失败

| 字段 | 值 |
|------|-----|
| 用例编号 | WA03-002 |
| 用例标题 | 获取扣缴义务人详情-缺少cpId-失败 |
| 接口路径 | POST /api/v2/tax/withholding-agent/detail |
| 用例类型 | 反向 |
| 优先级 | P0 |
| 请求参数 | ```json { "taxClassCode": "TC001" }``` |
| 预期结果 | HTTP 200, success=false, 提示cpId必填 |

#### WA03-003 获取扣缴义务人详情-缺少taxClassCode-失败

| 字段 | 值 |
|------|-----|
| 用例编号 | WA03-003 |
| 用例标题 | 获取扣缴义务人详情-缺少taxClassCode-失败 |
| 接口路径 | POST /api/v2/tax/withholding-agent/detail |
| 用例类型 | 反向 |
| 优先级 | P0 |
| 请求参数 | ```json { "cpId": 1001 }``` |
| 预期结果 | HTTP 200, success=false, 提示taxClassCode必填 |

#### WA03-004 获取扣缴义务人详情-taxClassCode不存在-失败

| 字段 | 值 |
|------|-----|
| 用例编号 | WA03-004 |
| 用例标题 | 获取扣缴义务人详情-taxClassCode不存在-失败 |
| 接口路径 | POST /api/v2/tax/withholding-agent/detail |
| 用例类型 | 反向 |
| 优先级 | P1 |
| 请求参数 | ```json { "cpId": 1001, "taxClassCode": "INVALID_TC" }``` |
| 预期结果 | HTTP 200, success=false, 提示扣缴义务人不存在 |

#### WA03-005 获取扣缴义务人详情-验证返回完整字段-成功

| 字段 | 值 |
|------|-----|
| 用例编号 | WA03-005 |
| 用例标题 | 获取扣缴义务人详情-验证返回完整字段-成功 |
| 接口路径 | POST /api/v2/tax/withholding-agent/detail |
| 用例类型 | 正向 |
| 优先级 | P1 |
| 前置条件 | 已存在taxClassCode="TC001"的扣缴义务人 |
| 请求参数 | ```json { "cpId": 1001, "taxClassCode": "TC001" }``` |
| 预期结果 | HTTP 200, success=true, data包含agentCode/agentName/nsrsbh/sbmm/areaid/djxhid/zgswjg/taxClassCode/status等完整字段 |

---

## 04 查询扣缴义务人列表

**接口路径**：`POST /api/v2/tax/withholding-agent/list`

### 用例列表

| 用例编号 | 用例标题 | 用例类型 | 优先级 |
|----------|----------|----------|--------|
| WA04-001 | 查询扣缴义务人列表-正常参数-成功 | 正向 | P0 |
| WA04-002 | 查询扣缴义务人列表-缺少cpId-失败 | 反向 | P0 |
| WA04-003 | 查询扣缴义务人列表-无筛选条件-成功 | 正向 | P1 |
| WA04-004 | 查询扣缴义务人列表-按nsrsbh精确查询-成功 | 正向 | P1 |
| WA04-005 | 查询扣缴义务人列表-按agentName模糊查询-成功 | 正向 | P1 |
| WA04-006 | 查询扣缴义务人列表-按status筛选-成功 | 正向 | P1 |
| WA04-007 | 查询扣缴义务人列表-分页pageNum-成功 | 分页 | P1 |
| WA04-008 | 查询扣缴义务人列表-分页pageSize-成功 | 分页 | P1 |
| WA04-009 | 查询扣缴义务人列表-空结果-成功 | 正向 | P2 |
| WA04-010 | 查询扣缴义务人列表-验证返回字段完整性-成功 | 正向 | P1 |

### 详细用例

#### WA04-001 查询扣缴义务人列表-正常参数-成功

| 字段 | 值 |
|------|-----|
| 用例编号 | WA04-001 |
| 用例标题 | 查询扣缴义务人列表-正常参数-成功 |
| 接口路径 | POST /api/v2/tax/withholding-agent/list |
| 用例类型 | 正向 |
| 优先级 | P0 |
| 请求参数 | ```json { "cpId": 1001, "pageNum": 1, "pageSize": 20 }``` |
| 预期结果 | HTTP 200, success=true, data.list包含扣缴义务人列表, data.total为总数 |

#### WA04-002 查询扣缴义务人列表-缺少cpId-失败

| 字段 | 值 |
|------|-----|
| 用例编号 | WA04-002 |
| 用例标题 | 查询扣缴义务人列表-缺少cpId-失败 |
| 接口路径 | POST /api/v2/tax/withholding-agent/list |
| 用例类型 | 反向 |
| 优先级 | P0 |
| 请求参数 | ```json { "pageNum": 1, "pageSize": 20 }``` |
| 预期结果 | HTTP 200, success=false, 提示cpId必填 |

#### WA04-003 查询扣缴义务人列表-无筛选条件-成功

| 字段 | 值 |
|------|-----|
| 用例编号 | WA04-003 |
| 用例标题 | 查询扣缴义务人列表-无筛选条件-成功 |
| 接口路径 | POST /api/v2/tax/withholding-agent/list |
| 用例类型 | 正向 |
| 优先级 | P1 |
| 请求参数 | ```json { "cpId": 1001 }``` |
| 预期结果 | HTTP 200, success=true, 返回所有扣缴义务人(默认分页) |

#### WA04-004 查询扣缴义务人列表-按nsrsbh精确查询-成功

| 字段 | 值 |
|------|-----|
| 用例编号 | WA04-004 |
| 用例标题 | 查询扣缴义务人列表-按nsrsbh精确查询-成功 |
| 接口路径 | POST /api/v2/tax/withholding-agent/list |
| 用例类型 | 正向 |
| 优先级 | P1 |
| 请求参数 | ```json { "cpId": 1001, "nsrsbh": "91310000XXXXXXXX1K", "pageNum": 1, "pageSize": 20 }``` |
| 预期结果 | HTTP 200, success=true, 仅返回nsrsbh匹配的记录 |

#### WA04-005 查询扣缴义务人列表-按agentName模糊查询-成功

| 字段 | 值 |
|------|-----|
| 用例编号 | WA04-005 |
| 用例标题 | 查询扣缴义务人列表-按agentName模糊查询-成功 |
| 接口路径 | POST /api/v2/tax/withholding-agent/list |
| 用例类型 | 正向 |
| 优先级 | P1 |
| 请求参数 | ```json { "cpId": 1001, "agentName": "科技", "pageNum": 1, "pageSize": 20 }``` |
| 预期结果 | HTTP 200, success=true, 返回agentName包含"科技"的记录 |

#### WA04-006 查询扣缴义务人列表-按status筛选-成功

| 字段 | 值 |
|------|-----|
| 用例编号 | WA04-006 |
| 用例标题 | 查询扣缴义务人列表-按status筛选-成功 |
| 接口路径 | POST /api/v2/tax/withholding-agent/list |
| 用例类型 | 正向 |
| 优先级 | P1 |
| 请求参数 | ```json { "cpId": 1001, "status": "ACTIVE", "pageNum": 1, "pageSize": 20 }``` |
| 预期结果 | HTTP 200, success=true, 仅返回status为ACTIVE的记录 |

#### WA04-007 查询扣缴义务人列表-分页pageNum-成功

| 字段 | 值 |
|------|-----|
| 用例编号 | WA04-007 |
| 用例标题 | 查询扣缴义务人列表-分页pageNum-成功 |
| 接口路径 | POST /api/v2/tax/withholding-agent/list |
| 用例类型 | 分页 |
| 优先级 | P1 |
| 请求参数 | ```json { "cpId": 1001, "pageNum": 2, "pageSize": 10 }``` |
| 预期结果 | HTTP 200, success=true, 返回第2页数据(每页10条) |

#### WA04-008 查询扣缴义务人列表-分页pageSize-成功

| 字段 | 值 |
|------|-----|
| 用例编号 | WA04-008 |
| 用例标题 | 查询扣缴义务人列表-分页pageSize-成功 |
| 接口路径 | POST /api/v2/tax/withholding-agent/list |
| 用例类型 | 分页 |
| 优先级 | P1 |
| 请求参数 | ```json { "cpId": 1001, "pageNum": 1, "pageSize": 50 }``` |
| 预期结果 | HTTP 200, success=true, 返回50条数据 |

#### WA04-009 查询扣缴义务人列表-空结果-成功

| 字段 | 值 |
|------|-----|
| 用例编号 | WA04-009 |
| 用例标题 | 查询扣缴义务人列表-空结果-成功 |
| 接口路径 | POST /api/v2/tax/withholding-agent/list |
| 用例类型 | 正向 |
| 优先级 | P2 |
| 请求参数 | ```json { "cpId": 9999, "pageNum": 1, "pageSize": 20 }``` |
| 预期结果 | HTTP 200, success=true, data.list为空, data.total=0 |

#### WA04-010 查询扣缴义务人列表-验证返回字段完整性-成功

| 字段 | 值 |
|------|-----|
| 用例编号 | WA04-010 |
| 用例标题 | 查询扣缴义务人列表-验证返回字段完整性-成功 |
| 接口路径 | POST /api/v2/tax/withholding-agent/list |
| 用例类型 | 正向 |
| 优先级 | P1 |
| 请求参数 | ```json { "cpId": 1001, "pageNum": 1, "pageSize": 20 }``` |
| 预期结果 | HTTP 200, success=true, data.list中每条记录包含taxClassCode/agentCode/agentName/nsrsbh/status等字段 |

---

## 05 搜索扣缴义务人

**接口路径**：`POST /api/v2/tax/withholding-agent/query`

### 用例列表

| 用例编号 | 用例标题 | 用例类型 | 优先级 |
|----------|----------|----------|--------|
| WA05-001 | 搜索扣缴义务人-正常参数-成功 | 正向 | P0 |
| WA05-002 | 搜索扣缴义务人-缺少cpId-失败 | 反向 | P0 |
| WA05-003 | 搜索扣缴义务人-按agentCode模糊搜索-成功 | 正向 | P1 |
| WA05-004 | 搜索扣缴义务人-按agentName模糊搜索-成功 | 正向 | P1 |
| WA05-005 | 搜索扣缴义务人-按nsrsbh精确搜索-成功 | 正向 | P1 |
| WA05-006 | 搜索扣缴义务人-多关键词搜索-成功 | 正向 | P1 |
| WA05-007 | 搜索扣缴义务人-分页-成功 | 分页 | P1 |
| WA05-008 | 搜索扣缴义务人-空结果-成功 | 正向 | P2 |

### 详细用例

#### WA05-001 搜索扣缴义务人-正常参数-成功

| 字段 | 值 |
|------|-----|
| 用例编号 | WA05-001 |
| 用例标题 | 搜索扣缴义务人-正常参数-成功 |
| 接口路径 | POST /api/v2/tax/withholding-agent/query |
| 用例类型 | 正向 |
| 优先级 | P0 |
| 请求参数 | ```json { "cpId": 1001, "keyword": "科技", "pageNum": 1, "pageSize": 20 }``` |
| 预期结果 | HTTP 200, success=true, data.list包含匹配"科技"的扣缴义务人 |

#### WA05-002 搜索扣缴义务人-缺少cpId-失败

| 字段 | 值 |
|------|-----|
| 用例编号 | WA05-002 |
| 用例标题 | 搜索扣缴义务人-缺少cpId-失败 |
| 接口路径 | POST /api/v2/tax/withholding-agent/query |
| 用例类型 | 反向 |
| 优先级 | P0 |
| 请求参数 | ```json { "keyword": "科技", "pageNum": 1, "pageSize": 20 }``` |
| 预期结果 | HTTP 200, success=false, 提示cpId必填 |

#### WA05-003 搜索扣缴义务人-按agentCode模糊搜索-成功

| 字段 | 值 |
|------|-----|
| 用例编号 | WA05-003 |
| 用例标题 | 搜索扣缴义务人-按agentCode模糊搜索-成功 |
| 接口路径 | POST /api/v2/tax/withholding-agent/query |
| 用例类型 | 正向 |
| 优先级 | P1 |
| 请求参数 | ```json { "cpId": 1001, "keyword": "Agent", "pageNum": 1, "pageSize": 20 }``` |
| 预期结果 | HTTP 200, success=true, data.list包含agentCode包含"Agent"的记录 |

#### WA05-004 搜索扣缴义务人-按agentName模糊搜索-成功

| 字段 | 值 |
|------|-----|
| 用例编号 | WA05-004 |
| 用例标题 | 搜索扣缴义务人-按agentName模糊搜索-成功 |
| 接口路径 | POST /api/v2/tax/withholding-agent/query |
| 用例类型 | 正向 |
| 优先级 | P1 |
| 请求参数 | ```json { "cpId": 1001, "keyword": "有限", "pageNum": 1, "pageSize": 20 }``` |
| 预期结果 | HTTP 200, success=true, data.list包含agentName包含"有限"的记录 |

#### WA05-005 搜索扣缴义务人-按nsrsbh精确搜索-成功

| 字段 | 值 |
|------|-----|
| 用例编号 | WA05-005 |
| 用例标题 | 搜索扣缴义务人-按nsrsbh精确搜索-成功 |
| 接口路径 | POST /api/v2/tax/withholding-agent/query |
| 用例类型 | 正向 |
| 优先级 | P1 |
| 请求参数 | ```json { "cpId": 1001, "keyword": "91310000XXXXXXXX1K", "pageNum": 1, "pageSize": 20 }``` |
| 预期结果 | HTTP 200, success=true, data.list包含nsrsbh精确匹配的记录 |

#### WA05-006 搜索扣缴义务人-多关键词搜索-成功

| 字段 | 值 |
|------|-----|
| 用例编号 | WA05-006 |
| 用例标题 | 搜索扣缴义务人-多关键词搜索-成功 |
| 接口路径 | POST /api/v2/tax/withholding-agent/query |
| 用例类型 | 正向 |
| 优先级 | P1 |
| 请求参数 | ```json { "cpId": 1001, "keyword": "Agent 科技", "pageNum": 1, "pageSize": 20 }``` |
| 预期结果 | HTTP 200, success=true, data.list包含任一关键词匹配的记录 |

#### WA05-007 搜索扣缴义务人-分页-成功

| 字段 | 值 |
|------|-----|
| 用例编号 | WA05-007 |
| 用例标题 | 搜索扣缴义务人-分页-成功 |
| 接口路径 | POST /api/v2/tax/withholding-agent/query |
| 用例类型 | 分页 |
| 优先级 | P1 |
| 请求参数 | ```json { "cpId": 1001, "keyword": "科技", "pageNum": 1, "pageSize": 5 }``` |
| 预期结果 | HTTP 200, success=true, data.list返回5条, data.total为满足条件的总数 |

#### WA05-008 搜索扣缴义务人-空结果-成功

| 字段 | 值 |
|------|-----|
| 用例编号 | WA05-008 |
| 用例标题 | 搜索扣缴义务人-空结果-成功 |
| 接口路径 | POST /api/v2/tax/withholding-agent/query |
| 用例类型 | 正向 |
| 优先级 | P2 |
| 请求参数 | ```json { "cpId": 1001, "keyword": "不存在的关键词XYZ", "pageNum": 1, "pageSize": 20 }``` |
| 预期结果 | HTTP 200, success=true, data.list为空 |

---

## 06 删除扣缴义务人

**接口路径**：`POST /api/v2/tax/withholding-agent/delete`

### 用例列表

| 用例编号 | 用例标题 | 用例类型 | 优先级 |
|----------|----------|----------|--------|
| WA06-001 | 删除扣缴义务人-正常参数-成功 | 正向 | P0 |
| WA06-002 | 删除扣缴义务人-缺少cpId-失败 | 反向 | P0 |
| WA06-003 | 删除扣缴义务人-缺少taxClassCode-失败 | 反向 | P0 |
| WA06-004 | 删除扣缴义务人-taxClassCode不存在-失败 | 反向 | P1 |
| WA06-005 | 删除扣缴义务人-重复删除-幂等 | 幂等 | P1 |

### 详细用例

#### WA06-001 删除扣缴义务人-正常参数-成功

| 字段 | 值 |
|------|-----|
| 用例编号 | WA06-001 |
| 用例标题 | 删除扣缴义务人-正常参数-成功 |
| 接口路径 | POST /api/v2/tax/withholding-agent/delete |
| 用例类型 | 正向 |
| 优先级 | P0 |
| 前置条件 | 已存在taxClassCode="TC001"的扣缴义务人 |
| 请求参数 | ```json { "cpId": 1001, "taxClassCode": "TC001" }``` |
| 预期结果 | HTTP 200, success=true, msg="删除成功" |

#### WA06-002 删除扣缴义务人-缺少cpId-失败

| 字段 | 值 |
|------|-----|
| 用例编号 | WA06-002 |
| 用例标题 | 删除扣缴义务人-缺少cpId-失败 |
| 接口路径 | POST /api/v2/tax/withholding-agent/delete |
| 用例类型 | 反向 |
| 优先级 | P0 |
| 请求参数 | ```json { "taxClassCode": "TC001" }``` |
| 预期结果 | HTTP 200, success=false, 提示cpId必填 |

#### WA06-003 删除扣缴义务人-缺少taxClassCode-失败

| 字段 | 值 |
|------|-----|
| 用例编号 | WA06-003 |
| 用例标题 | 删除扣缴义务人-缺少taxClassCode-失败 |
| 接口路径 | POST /api/v2/tax/withholding-agent/delete |
| 用例类型 | 反向 |
| 优先级 | P0 |
| 请求参数 | ```json { "cpId": 1001 }``` |
| 预期结果 | HTTP 200, success=false, 提示taxClassCode必填 |

#### WA06-004 删除扣缴义务人-taxClassCode不存在-失败

| 字段 | 值 |
|------|-----|
| 用例编号 | WA06-004 |
| 用例标题 | 删除扣缴义务人-taxClassCode不存在-失败 |
| 接口路径 | POST /api/v2/tax/withholding-agent/delete |
| 用例类型 | 反向 |
| 优先级 | P1 |
| 请求参数 | ```json { "cpId": 1001, "taxClassCode": "INVALID_TC" }``` |
| 预期结果 | HTTP 200, success=false, 提示扣缴义务人不存在 |

#### WA06-005 删除扣缴义务人-重复删除-幂等

| 字段 | 值 |
|------|-----|
| 用例编号 | WA06-005 |
| 用例标题 | 删除扣缴义务人-重复删除-幂等 |
| 接口路径 | POST /api/v2/tax/withholding-agent/delete |
| 用例类型 | 幂等 |
| 优先级 | P1 |
| 前置条件 | taxClassCode="TC001"的扣缴义务人已删除 |
| 请求参数 | ```json { "cpId": 1001, "taxClassCode": "TC001" }``` |
| 预期结果 | HTTP 200, success=true, msg="删除成功"(幂等返回) |

---

## 07 获取报税地区列表

**接口路径**：`POST /api/v2/tax/withholding-agent/tax-regions`

### 用例列表

| 用例编号 | 用例标题 | 用例类型 | 优先级 |
|----------|----------|----------|--------|
| WA07-001 | 获取报税地区列表-正常参数-成功 | 正向 | P0 |
| WA07-002 | 获取报税地区列表-缺少cpId-失败 | 反向 | P0 |
| WA07-003 | 获取报税地区列表-验证返回字段-成功 | 正向 | P1 |
| WA07-004 | 获取报税地区列表-空结果-成功 | 正向 | P2 |

### 详细用例

#### WA07-001 获取报税地区列表-正常参数-成功

| 字段 | 值 |
|------|-----|
| 用例编号 | WA07-001 |
| 用例标题 | 获取报税地区列表-正常参数-成功 |
| 接口路径 | POST /api/v2/tax/withholding-agent/tax-regions |
| 用例类型 | 正向 |
| 优先级 | P0 |
| 请求参数 | ```json { "cpId": 1001 }``` |
| 预期结果 | HTTP 200, success=true, data.list包含地区列表(areaid/areaname) |

#### WA07-002 获取报税地区列表-缺少cpId-失败

| 字段 | 值 |
|------|-----|
| 用例编号 | WA07-002 |
| 用例标题 | 获取报税地区列表-缺少cpId-失败 |
| 接口路径 | POST /api/v2/tax/withholding-agent/tax-regions |
| 用例类型 | 反向 |
| 优先级 | P0 |
| 请求参数 | ```json {}``` |
| 预期结果 | HTTP 200, success=false, 提示cpId必填 |

#### WA07-003 获取报税地区列表-验证返回字段-成功

| 字段 | 值 |
|------|-----|
| 用例编号 | WA07-003 |
| 用例标题 | 获取报税地区列表-验证返回字段-成功 |
| 接口路径 | POST /api/v2/tax/withholding-agent/tax-regions |
| 用例类型 | 正向 |
| 优先级 | P1 |
| 请求参数 | ```json { "cpId": 1001 }``` |
| 预期结果 | HTTP 200, success=true, data.list中每条包含areaid/areaname等字段 |

#### WA07-004 获取报税地区列表-空结果-成功

| 字段 | 值 |
|------|-----|
| 用例编号 | WA07-004 |
| 用例标题 | 获取报税地区列表-空结果-成功 |
| 接口路径 | POST /api/v2/tax/withholding-agent/tax-regions |
| 用例类型 | 正向 |
| 优先级 | P2 |
| 请求参数 | ```json { "cpId": 9999 }``` |
| 预期结果 | HTTP 200, success=true, data.list为空 |

---

## 08 预获取税局任务ID

**接口路径**：`POST /api/v2/tax/withholding-agent/tax-authority`

### 用例列表

| 用例编号 | 用例标题 | 用例类型 | 优先级 |
|----------|----------|----------|--------|
| WA08-001 | 预获取税局任务ID-正常参数-成功 | 正向 | P0 |
| WA08-002 | 预获取税局任务ID-缺少cpId-失败 | 反向 | P0 |
| WA08-003 | 预获取税局任务ID-缺少nsrsbh-失败 | 反向 | P0 |
| WA08-004 | 预获取税局任务ID-缺少sdyf-失败 | 反向 | P0 |
| WA08-005 | 预获取税局任务ID-sdyf格式错误-失败 | 反向 | P1 |
| WA08-006 | 预获取税局任务ID-验证返回taskId-成功 | 正向 | P1 |

### 详细用例

#### WA08-001 预获取税局任务ID-正常参数-成功

| 字段 | 值 |
|------|-----|
| 用例编号 | WA08-001 |
| 用例标题 | 预获取税局任务ID-正常参数-成功 |
| 接口路径 | POST /api/v2/tax/withholding-agent/tax-authority |
| 用例类型 | 正向 |
| 优先级 | P0 |
| 请求参数 | ```json { "cpId": 1001, "nsrsbh": "91310000XXXXXXXX1K", "sdyf": "202503" }``` |
| 预期结果 | HTTP 200, success=true, data包含taxTaskId |

#### WA08-002 预获取税局任务ID-缺少cpId-失败

| 字段 | 值 |
|------|-----|
| 用例编号 | WA08-002 |
| 用例标题 | 预获取税局任务ID-缺少cpId-失败 |
| 接口路径 | POST /api/v2/tax/withholding-agent/tax-authority |
| 用例类型 | 反向 |
| 优先级 | P0 |
| 请求参数 | ```json { "nsrsbh": "91310000XXXXXXXX1K", "sdyf": "202503" }``` |
| 预期结果 | HTTP 200, success=false, 提示cpId必填 |

#### WA08-003 预获取税局任务ID-缺少nsrsbh-失败

| 字段 | 值 |
|------|-----|
| 用例编号 | WA08-003 |
| 用例标题 | 预获取税局任务ID-缺少nsrsbh-失败 |
| 接口路径 | POST /api/v2/tax/withholding-agent/tax-authority |
| 用例类型 | 反向 |
| 优先级 | P0 |
| 请求参数 | ```json { "cpId": 1001, "sdyf": "202503" }``` |
| 预期结果 | HTTP 200, success=false, 提示nsrsbh必填 |

#### WA08-004 预获取税局任务ID-缺少sdyf-失败

| 字段 | 值 |
|------|-----|
| 用例编号 | WA08-004 |
| 用例标题 | 预获取税局任务ID-缺少sdyf-失败 |
| 接口路径 | POST /api/v2/tax/withholding-agent/tax-authority |
| 用例类型 | 反向 |
| 优先级 | P0 |
| 请求参数 | ```json { "cpId": 1001, "nsrsbh": "91310000XXXXXXXX1K" }``` |
| 预期结果 | HTTP 200, success=false, 提示sdyf必填 |

#### WA08-005 预获取税局任务ID-sdyf格式错误-失败

| 字段 | 值 |
|------|-----|
| 用例编号 | WA08-005 |
| 用例标题 | 预获取税局任务ID-sdyf格式错误-失败 |
| 接口路径 | POST /api/v2/tax/withholding-agent/tax-authority |
| 用例类型 | 反向 |
| 优先级 | P1 |
| 请求参数 | ```json { "cpId": 1001, "nsrsbh": "91310000XXXXXXXX1K", "sdyf": "2025-03" }``` |
| 预期结果 | HTTP 200, success