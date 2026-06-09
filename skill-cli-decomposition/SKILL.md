---
name: task-decomposition-cli
description: 任务拆解与规划（CLI版）— 分析任务、拆解子任务、验证 DAG、生成并上传 Checklist
version: 3.1.0
metadata:
  astraworks:
    capability_type: task-decomposition
    category: planning
    tags: [task, decomposition, planning, dag, checklist, cli]
    target_agents: [Atlas]
---

# 任务拆解与规划（Task Decomposition - CLI）

## 概述

本 skill 定义 Atlas Agent 执行任务拆解的工作流程。

**核心原则**：
- 使用 `astraworks-cli orch mragents <room_id> --json` 获取 Matrix Room 中可用的 Agent 列表及其能力，用于辅助子任务分配和 required_skills 推断
- 使用 `astraworks-cli orch dag validate`、`astraworks-cli orch dag order` 完成所有 DAG 验证和排序
- 使用 `astraworks-cli orch platform upload` 将 Checklist 上传到平台
- Agent 负责任务分析和子任务拆解，不调用外部 LLM

---

## 输入

| 字段 | 必需 | 类型 | 说明 |
|------|------|------|------|
| task_id | 是 | string | 任务 ID |
| task_title | 是 | string | 任务标题 |
| task_description | 是 | string | 任务详细描述 |
| workgroup_id | 是 | string | 工作组 ID |
| goal | 否 | string | 任务目标/成功标准 |
| room_id | 否 | string | Matrix Room ID（用于获取可用 Agent 能力） |

---

## 工作流

```
Step 0: 获取可用 Agent（可选，当 room_id 提供时）
        astraworks-cli orch mragents <room_id> --json
        分析 Agent 能力列表，用于后续分配决策

Step 1: 理解任务
        分析 task_description，理解目标、约束、验收标准

Step 2: 拆解子任务
        Agent 直接完成拆解
        - 每个子任务原子化：单一职责，可独立验证
        - depends_on 表达依赖关系（支持 DAG）
        - required_skills + assignee_role 指定执行者
        - 所有子任务 item_id 必须唯一

Step 3: 写入临时文件
        将 subtasks 写入 JSON 文件

Step 4: DAG 验证
        astraworks-cli orch dag validate <file> --json

Step 5: 拓扑排序
        astraworks-cli orch dag order <file> --json

Step 6: 生成 Checklist
        按平台标准结构组装数据

Step 7: 上传 Checklist
        astraworks-cli orch platform upload <file> --json
```

---

## Step 0：获取可用 Agent（可选）

当输入包含 `room_id` 时，执行此步骤获取 Matrix Room 内所有可用 Agent 及其技能。

### 调用 CLI

```bash
astraworks-cli orch mragents <room_id> --json
```

### 响应结构

```json
{
  "room_id": "!abc123:astraworks.local",
  "agents": [
    {
            "agent_id": "00f9758d-4772-4065-a446-2a53c895094d",
            "agent_instance_id": "00f9758d-4772-4065-a446-2a53c895094d",
            "agent_name": "worker1",
            "virtual_user_id": "vu_24e611a74002",
            "matrix_user_id": "@agent_vu_24e611a74002:astraworks.local",
            "matrix_status": "active",
            "instance_id": "0fd17a20-73c9-41ed-b883-38aa8517ec3b-uavn",
            "definition_id": "0fd17a20-73c9-41ed-b883-38aa8517ec3b",
            "openclaw_agent_id": "worker1",
            "status": "idle",
            "version": "1.0.0",
            "installed_at": "2026-06-09T04:35:13.290913",
            "last_heartbeat": "2026-06-09T08:09:31.656711",
            "node_id": "9706df90-87c6-4636-bae8-6f6ef5790ce0",
            "definition": {
                "id": "0fd17a20-73c9-41ed-b883-38aa8517ec3b",
                "name": "agent-worker1",
                "display_name": "worker",
                "description": "worker - 由平台创建",
                "role": "assistant",
                "level": "workgroup",
                "skills": {
                    "core_skills": [
                        "git-operations",
                        "matrix-event-listener",
                        "workgroup-design",
                        "skill-document-generator"
                    ],
                    "domain_skills": []
                },
                "tools": {
                    "mcp_servers": [],
                    "tools": []
                }
            },
            "definition_skills": {
                "core_skills": [
                    "git-operations",
                    "matrix-event-listener",
                    "workgroup-design",
                    "skill-document-generator"
                ],
                "domain_skills": []
            },
            "definition_tools": {
                "mcp_servers": [],
                "tools": []
            },
            "skills": []
        }
  ]
}
```

### Agent 能力分析

分析获取的 Agent 列表，建立能力映射：

|| Agent ID | Agent Name | 技能 |
||----------|------------|------|
|| uuid-1 | Atlas | analysis, design, planning |
|| uuid-2 | Coder-1 | coding, python, backend |
|| uuid-3 | Coder-2 | coding, frontend, typescript |
|| uuid-4 | QA-1 | testing, qa, automation |

### 规划决策

根据 `required_skills` 选择合适的 Agent：

- 分析每个 subtask 需要的 `required_skills`
- 在 Agent 列表中找出技能覆盖的 Agent
- 若无精确匹配，选择技能最接近的 Agent
- 若无法分配，标记为 `unassigned`

**注意**：此步骤仅获取和理解 Agent 能力，Agent 自身决定如何分配任务。

---

## Step 1：理解任务

分析 `task_description`，明确以下要素：

- **目标**：要交付什么（功能/文档/配置/系统等）
- **约束**：技术栈、语言、框架、代码规范等限制条件
- **验收标准**：如何判断任务完成（可测试、可验证）
- **边界**：哪些不做（Scope out）

必要时结合 `goal` 字段补充成功标准。

---

## Step 2：拆解子任务

### 2.1 拆解原则

1. **原子化**：每个子任务单一职责，可独立验证完成
2. **可并行**：无依赖的子任务可并行执行
3. **技能匹配**：`required_skills` 与 Agent 技能对应
4. **数量控制**：建议 3-10 个子任务，最多不超过 50 个
5. **依赖表达**：通过 `depends_on` 描述执行先后关系，支持 DAG（有向无环图）
6. **唯一 item_id**：所有子任务 `item_id` 全局唯一

### 2.2 分配决策（基于 Step 0 获取的 Agent 能力）

当 `room_id` 提供时，Agent 应参考可用 Agent 能力进行分配决策：

1. **分析 subtask 需求**：明确每个 subtask 的 `required_skills`
2. **匹配 Agent**：根据技能选择合适的 Agent
3. **设置 assignee_role**：将 `matrix_user_id` 填入 `assignee_role` 字段（如 `@agent_coder1:astraworks.local`）

示例分配逻辑：

| Subtask type | required_skills | 推荐 Agent | assignee_role |
|--------------|-----------------|-----------|--------------|
| analysis | ["analysis"] | Atlas | @agent_atlas:astraworks.local |
| design | ["design"] | Atlas | @agent_atlas:astraworks.local |
| coding | ["coding", "backend", "python"] | Coder-1 | @agent_coder1:astraworks.local |
| coding | ["coding", "frontend", "typescript"] | Coder-2 | @agent_coder2:astraworks.local |
| testing | ["testing", "qa"] | QA-1 | @agent_qa1:astraworks.local |

### 2.3 任务类型参考

| type | 说明 | 典型 assignee_role |
|------|------|--------------------|
| `analysis` | 需求分析、PRD 输出 | Analyst |
| `design` | 技术方案、API 设计 | Designer |
| `implementation` | 功能开发 | Coder |
| `coding` | 编码实现（前后端） | Coder / Frontend / Backend |
| `testing` | 单元测试、集成测试 | QA |
| `review` | 代码评审 | Reviewer |
| `infra` | 基础设施、CI/CD | DevOps |
| `other` | 其他类型 | 视情况 |

### 2.3 任务类型参考

|| type | 说明 | 典型 required_skills |
|------|------|--------------------|
|| `analysis` | 需求分析、PRD 输出 | `["analysis"]` |
|| `design` | 技术方案、API 设计 | `["design"]` |
|| `implementation` | 功能开发 | `["coding"]` |
|| `coding` | 编码实现（前后端） | `["coding", "backend"]` 或 `["coding", "frontend"]` |
|| `testing` | 单元测试、集成测试 | `["testing", "qa"]` |
|| `review` | 代码评审 | `["review", "coding"]` |
|| `infra` | 基础设施、CI/CD | `["infra", "devops"]` |
|| `other` | 其他类型 | 视情况 |

### 2.4 拆解示例（基于 Agent 能力分配）

```
假设 Step 0 获取的 Agent 能力：
  - Atlas (uuid-1): analysis, design, planning
  - Coder-1 (uuid-2): coding, python, backend
  - Coder-2 (uuid-3): coding, frontend, typescript
  - QA-1 (uuid-4): testing, qa, automation

拆解结果：
item-2-1 (analysis)       depends_on=[]         → assignee_role=@agent_atlas:astraworks.local (Atlas)
item-2-2 (design)        depends_on=[item-2-1] → assignee_role=@agent_atlas:astraworks.local (Atlas)
item-2-3 (design)        depends_on=[item-2-1] → assignee_role=@agent_atlas:astraworks.local (Atlas)
item-2-4 (coding)        depends_on=[item-2-2, item-2-3] → assignee_role=@agent_coder1:astraworks.local (Coder-1)
item-2-5 (coding)        depends_on=[item-2-2, item-2-3] → assignee_role=@agent_coder2:astraworks.local (Coder-2)
item-2-6 (testing)       depends_on=[item-2-4, item-2-5] → assignee_role=@agent_qa1:astraworks.local (QA-1)
item-2-7 (testing)       depends_on=[item-2-6] → assignee_role=@agent_qa1:astraworks.local (QA-1)
```

---

## Step 3：写入临时文件

### 3.1 准备 Subtasks JSON

Agent 生成符合以下结构的 JSON（直接数组格式，供 CLI 使用）：

```json
[
  {
    "item_id": "item-1-1",
    "title": "编写后端登录 API",
    "description": "实现用户名密码验证接口，返回 JWT token",
    "required_skills": ["coding", "backend", "python"],
    "depends_on": [],
    "assignee_role": "@agent_coder1:astraworks.local",
    "agent_name": "Coder-1",
    "type": "coding",
    "order": 0
  },
  {
    "item_id": "item-1-2",
    "title": "前端登录页面开发",
    "description": "实现登录表单 UI，调用后端登录 API",
    "required_skills": ["coding", "frontend", "typescript"],
    "depends_on": ["item-1-1"],
    "assignee_role": "@agent_coder2:astraworks.local",
    "agent_name": "Coder-2",
    "type": "coding",
    "order": 1
  }
]
```

### 3.2 写入文件

```bash
cat > /tmp/subtasks.json << 'EOF'
<paste_subtasks_json_here>
EOF
```

---

## Step 4：DAG 验证

```bash
astraworks-cli orch dag validate /tmp/subtasks.json --json
```

**CLI 返回示例（成功）**：

```json
{
  "success": true,
  "valid": true,
  "nodes": 3,
  "edges": 2,
  "errors": []
}
```

**CLI 返回示例（失败）**：

```json
{
  "success": true,
  "valid": false,
  "nodes": 3,
  "edges": 2,
  "errors": [
    { "type": "cycle", "message": "检测到循环依赖: A → B → C → A", "error_code": "DAG_CYCLE", "exit_code": 1 },
    { "type": "invalid_ref", "message": "item-1-3 引用了不存在的依赖 'item-99'", "error_code": "DAG_INVALID_REF", "exit_code": 1 }
  ]
}
```

**验证失败处理**：

- `DAG_CYCLE`：重新规划 subtasks，消除循环依赖后再次验证
- `DAG_INVALID_REF`：检查 `depends_on` 中所有 item_id 是否在 subtasks 数组中存在
- `DAG_EMPTY`：确认 subtasks 非空后重新验证

---

## Step 5：拓扑排序

```bash
astraworks-cli orch dag order /tmp/subtasks.json --json
```

**CLI 返回示例**：

```json
{
  "success": true,
  "order": ["item-1-1", "item-1-3", "item-1-2"],
  "layers": [
    ["item-1-1"],
    ["item-1-3"],
    ["item-1-2"]
  ]
}
```

- `order`：所有节点的全序排列
- `layers`：分层执行顺序，同一层内的任务可并行执行

**注意**：`dag order` 内部会自动调用 `dag validate`，若 DAG 无效则返回验证错误。

---

## Step 6：生成 Checklist

### Checklist 结构

Agent 生成符合以下结构的 Checklist（供 `platform upload` 使用）：

```json
{
  "checklist": {
    "version": "1.0",
    "skill_name": "task-decomposition-cli",
    "task_info": {
      "task_id": "<task_id>",
      "title": "<task_title>",
      "description": "<task_description>",
      "goal": "<goal>",
      "workgroup_id": "<workgroup_id>"
    },
    "decomposition": {
      "status": "completed",
      "created_at": "<UTC ISO 8601>"
    },
    "execution": {
      "status": "pending"
    },
    "dag": {
      "nodes": 3,
      "edges": 2,
      "is_valid": true
    },
    "subtasks": [
      {
        "item_id": "item-1-1",
        "title": "编写后端登录 API",
        "description": "实现用户名密码验证接口",
        "required_skills": ["coding", "backend", "python"],
        "depends_on": [],
        "assignee_role": "@agent_coder1:astraworks.local",
        "agent_name": "Coder-1",
        "type": "coding",
        "order": 0,
        "status": "pending"
      }
    ],
    "topological_order": ["item-1-1", "item-1-3", "item-1-2"]
  }
}
```

### 写入 Checklist 文件

```bash
cat > /tmp/checklist.json << 'EOF'
<paste_checklist_json_here>
EOF
```

---

## Step 7：上传 Checklist

```bash
astraworks-cli orch platform upload /tmp/checklist.json --json
```

**CLI 内部实现**：读取 `~/.openclaw/astraworks-connection.json` 配置，调用 POST `/awp/plan`。

**请求体**（CLI 自动从 checklist.json 提取）：

```json
{
  "task_id": "<task_id>",
  "force_replan": true,
  "todos": [
    {
      "item_id": "item-1-1",
      "title": "...",
      "description": "...",
      "order": 0,
      "type": "coding",
      "depends_on": [],
      "required_skills": ["coding", "backend", "python"],
      "assignee_role": "@agent_coder1:astraworks.local"
    }
  ]
}
```

**CLI 返回示例**：

```json
{
  "success": true,
  "task_id": "abc-123",
  "todos": [
    { "item_id": "item-1-1", "id": "uuid-1", "status": "pending" },
    { "item_id": "item-1-2", "id": "uuid-2", "status": "pending" }
  ],
  "uploaded_at": "2026-05-25T10:00:00Z"
}
```

**成功**：打印成功消息，包含创建的所有 todo 条目。
**失败**：根据 HTTP 状态码处理（401 检查 token，404 确认 task_id，500 检查平台服务）。

---

## 输出

| 字段 | 类型 | 说明 |
|------|------|------|
| success | bool | 是否成功 |
| checklist | dict | 完整的 Checklist |
| topological_order | List[str] | 分发顺序（layers 扁平展开） |
| layers | List[List[str]] | 分层执行顺序 |
| total_subtasks | int | 子任务总数 |
| platform_task_id | string | 平台返回的 task_id |
| platform_todos | List[dict] | 平台返回的 todos（含 uuid） |
| error | string | 错误信息（失败时） |

---

## CLI 调用汇总

| 步骤 | CLI |
|------|-----|
| 获取可用 Agent |  |
| DAG 验证 | `astraworks-cli orch dag validate <file> --json` |
| 拓扑排序 | `astraworks-cli orch dag order <file> --json` |
| 上传 Checklist | `astraworks-cli orch platform upload <file> --json` |

---

## 约束

- 所有 CLI 命令使用 `astraworks-cli orch` 前缀
- 使用 `--json` 标志便于 Agent 解析结构化输出
- 所有时间戳使用 UTC ISO 8601 格式
- `depends_on` 仅接受 subtasks 数组中已存在的 `item_id`
- 建议子任务数不超过 50 个
- 连接配置从 `~/.openclaw/astraworks-connection.json` 读取（可通过 `ASTRAWORKS_TOKEN` 环境变量覆盖）
