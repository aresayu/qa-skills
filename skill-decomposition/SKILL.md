---
name: task-decomposition
description: 任务拆解与规划 — 分析任务、拆解子任务、验证 DAG、生成 Checklist
version: 1.0.0
metadata:
  astraworks:
    capability_type: task-decomposition
    category: planning
    tags: [task, decomposition, planning, dag, checklist]
    target_agents: [Atlas]
---

# 任务拆解与规划（Task Decomposition）

## 概述

本 skill 定义 Agent 执行任务拆解的工作流程。

**核心原则**：Agent 直接按本指令完成任务拆解，无需代码调用 LLM API。

---

## 输入

| 字段 | 必需 | 类型 | 说明 |
|------|------|------|------|
| task_id | 是 | string | 任务 ID |
| task_title | 是 | string | 任务标题 |
| task_description | 是 | string | 任务详细描述 |
| workgroup_id | 是 | string | 工作组 ID |
| goal | 否 | string | 任务目标/成功标准 |

---

## 工作流

```
Step 1: 理解任务
        分析 task_description，理解目标、约束、验收标准

Step 2: 拆解子任务
        Agent 直接完成拆解（调用自身 LLM 能力）
        - 每个子任务原子化：单一职责，可独立验证
        - depends_on 表达依赖关系（支持 DAG）
        - required_skills + assignee_role 指定执行者

Step 3: DAG 验证
        调用 scripts.dag.validate_dag() 检查：
        - 循环依赖
        - 前向引用（depends_on 引用不存在的 id）
        - 空列表

Step 4: 拓扑排序
        调用 scripts.dag.get_topological_order() 生成分发顺序

Step 5: 生成 Checklist
        按标准结构组装数据

Step 6: 持久化
        调用平台工具保存到 Task.extra_data.checklist
```

---

## 子任务结构

```json
{
  "id": "item-1-1",
  "title": "编写后端登录 API",
  "description": "实现用户名密码验证接口，返回 JWT token",
  "required_skills": ["coding", "security"],
  "depends_on": [],
  "assignee_role": "Coder"
}
```

### 拆解原则

1. **原子化**：每个子任务单一职责，可独立验证完成
2. **可并行**：无依赖的子任务可并行执行
3. **技能匹配**：required_skills 与角色技能标签对应
4. **数量控制**：建议 3-10 个子任务

### 技能标签参考

| 标签 | 适用角色 |
|------|----------|
| analysis | Analyst |
| design | Designer |
| coding | Coder |
| frontend | Frontend |
| backend | Backend |
| testing | QA |
| infra | DevOps |
| review | Reviewer |

---

## DAG 验证

调用工具函数：

```python
from scripts.dag import validate_dag, get_topological_order

# 验证
is_valid, error = validate_dag(subtasks)
if not is_valid:
    # 重新规划

# 拓扑排序
order = get_topological_order(subtasks)
# order = ["item-1", "item-2", "item-3"]
```

### 错误类型

| 错误 | 说明 |
|------|------|
| 循环依赖 | A→B→C→A |
| 前向引用 | depends_on 引用不存在的 id |
| 空列表 | 无子任务 |

---

## Checklist 结构

Agent 生成符合以下结构的 Checklist：

```yaml
checklist:
  version: "1.0"
  skill_name: "task-decomposition"

  task_info:
    task_id: "task-xxx"
    title: "实现用户登录功能"
    description: "用户通过用户名密码登录"
    goal: "登录成功率达到 99% 以上"
    workgroup_id: "wg-xxx"

  decomposition:
    status: completed
    created_at: "2024-01-01T10:00:00Z"

  execution:
    status: pending

  dag:
    nodes: 3
    edges: 2
    is_valid: true

  subtasks:
    - id: "item-1-1"
      title: "编写后端登录 API"
      description: "实现用户名密码验证"
      required_skills: ["coding"]
      depends_on: []
      assignee_role: "Coder"
      status: pending
      created_at: "2024-01-01T10:00:00Z"

  topological_order: ["item-1-1", "item-1-2", "item-1-3"]
```

---

## 输出

| 字段 | 类型 | 说明 |
|------|------|------|
| success | bool | 是否成功 |
| checklist | dict | 完整的 Checklist |
| topological_order | List[str] | 分发顺序 |
| total_subtasks | int | 子任务总数 |
| error | string | 错误信息（失败时） |

---

## 约束

- Agent 直接按本指令工作，无需代码调用 LLM
- Checklist 必须持久化到平台
- 所有时间戳使用 UTC ISO 8601 格式
- `depends_on` 仅接受已存在的 `subtask.id`
- 建议子任务数不超过 50 个
