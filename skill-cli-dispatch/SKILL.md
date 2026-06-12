---
name: task-dispatch-cli
description: 任务分发（CLI版）— 读取 Checklist，按 DAG 依赖分发任务给 Worker
version: 3.0.0
metadata:
  astraworks:
    capability_type: task-dispatch
    category: execution
    tags: [task, dispatch, subtask, cli]
    target_agents: [Atlas]
---

# 任务分发（Task Dispatch - CLI）

## 概述

本 skill 定义 Atlas Agent 协调任务分发的工作流程。

**核心原则**：
- 使用 `astraworks-cli orch platform todos` 获取平台 todos
- 使用 `astraworks-cli orch dag order` 一次获取所有可分发的任务
- 使用 `astraworks-cli orch dispatch` 发送分发消息到 Matrix Room
- 使用 `astraworks-cli orch report` 发送任务完成报告到 Matrix Room

---

## 输入

| 字段 | 必需 | 类型 | 说明 |
|------|------|------|------|
| task_id | 是 | string | 任务 ID |

---

## Agent 工作流

```
Step 1: 获取 Todos
        astraworks-cli orch platform todos <task_id> --output /tmp/todos.json --json

Step 2: 获取可分发任务（一行命令，自动从输入文件取 status）
        astraworks-cli orch dag order /tmp/todos.json --json
        → result.dispatchable 即所有可分发的 item_id

Step 3: 分发任务
        对 result.dispatchable 中每个 item_id 调用：
        astraworks-cli orch dispatch <item_id> --todos-file /tmp/todos.json --json

Step 4: 生成报告
        所有 Todo 完成后，组装报告发送到Matrix Room
        astraworks-cli orch reprot /tmp/todos.json --json

Step 4.4: 标记任务完成
        报告发送成功后，调用 forcedone 把 task 置为 done
        astraworks-cli orch forcedone <task_id> --json

```

---

## Step 1：获取 Todos

```bash
astraworks-cli orch platform todos <task_id> --output /tmp/todos.json --json
```

**CLI 内部实现**：读取 `~/.openclaw/astraworks-connection.json` 配置，调用 GET `/awp/tasks/{task_id}/todos`。

**CLI 返回示例**：

```json
{
  "success": true,
  "task": {
    "id": "c8fd3085-d7c0-4fbf-a824-6a6d7cd4b83e",
    "title": "用户登录功能开发",
    "description": "实现用户注册、登录、登出功能",
    "matrix_room_id": "!abc123:astraworks.local"
  },
  "todos": [
    {
      "id": "uuid-1",
      "item_id": "item-2-1",
      "title": "需求分析与PRD输出",
      "description": "...",
      "status": "pending",
      "order": 0,
      "progress_pct": 0,
      "output_summary": null,
      "type": "analysis",
      "depends_on": [],
      "required_skills": ["analysis"],
      "assignee_role": "uuid-xxx",
      "created_at": "2026-05-19T06:24:13Z",
      "updated_at": "2026-05-19T06:24:13Z"
    },
    {
      "id": "uuid-2",
      "item_id": "item-2-2",
      "title": "技术方案与API接口设计",
      "description": "...",
      "status": "pending",
      "order": 1,
      "type": "other",
      "depends_on": ["item-2-1"],
      "required_skills": ["design"],
      "assignee_role": "uuid-yyy",
      "created_at": "2026-05-19T06:24:13Z",
      "updated_at": "2026-05-19T06:24:13Z"
    }
  ],
  "total": 2,
  "done": 0,
  "pending": 2,
  "in_progress": 0
}
```

**关键字段说明**：

| 字段 | 说明 |
|------|------|
| `task.id` | 任务 ID |
| `task.title` | 任务标题 |
| `task.matrix_room_id` | Matrix Room ID，用于后续消息发送 |
| `id` | 平台数据库 UUID，用于 worker start/complete |
| `item_id` | 业务层唯一标识，用于 dag can-dispatch / dispatch |
| `status` | `pending` \| `in_progress` \| `done` \| `skipped` |
| `depends_on` | 依赖的 item_id 列表 |
| `assignee_role` | Agent 虚拟用户 ID（matrix_user_id），用于匹配 Agent 发送消息 |

**如果指定了 `--output`**，todos 将保存到文件，后续 `dag order` 和 `dispatch` 可直接引用该文件。

---

## Step 2：分析可分发任务

一次调用 `dag order` 即可拿到所有可分发的任务，无需逐个检查。

```bash
astraworks-cli orch dag order /tmp/todos.json --json
```

**关键变化**：`dag order` 自动检测输入文件是否包含 `status` 字段（todos 格式）。若有，自动计算并返回 `dispatchable` 字段 —— **第一个包含 pending 任务的 layer 中的所有 pending 任务**，即当前可分发的。

**返回结构**：

```json
{
  "success": true,
  "order": ["item-2-1", "item-2-2", "item-2-3", "item-2-4", "item-2-5"],
  "layers": [
    ["item-2-1"],
    ["item-2-2"],
    ["item-2-3"],
    ["item-2-4"],
    ["item-2-5"]
  ],
  "dispatchable": ["item-2-4"]
}
```

示例场景：item-2-1 ~ item-2-3 已完成（done/skipped），item-2-4 是 layers[3] 中第一个包含 pending 的任务，故 dispatchable = ["item-2-4"]。跳过已完成的 layers[0~2]，直接定位下一个可分发波次。

**重要**：`dispatchable` 数组内可能有多个可并行分发的任务，全部需要分发，不要只取第一个。

---

## Step 3：分发任务

### 3.1 数据来源

```
数据来源:
  - room_id: 从 Step 1 响应的 task.matrix_room_id 获取
  - matrix_user_id: 从 Step 1 响应的 todo.assignee_role 获取（即 Agent 的 matrix_user_id）
  - item_id: 从 Step 2 得到的 dispatchable 列表中获取
```

### 3.2 发送分发消息

```bash
astraworks-cli orch dispatch <item_id> --todos-file /tmp/todos.json --json
```

**CLI 内部实现流程**：

1. 从 `--todos-file` 加载 todos，查找对应 `item_id` 的 todo。
2. 调用 can-dispatch 逻辑校验该子任务是否允许分发。
3. 获取 `room_id`（`task.matrix_room_id`），获取目标 Agent matrix_user_id（`todo.assignee_role`）。
4. 构造 Matrix 消息，调用 `POST /api/v1/chat/matrix/send` 发送。

### 3.3 Matrix 消息格式与要求

**Matrix User ID 格式**：
`assignee_role`（即 `matrix_user_id`）本身已经是完整的 Matrix User ID 格式：
例如：`assignee_role = "@_astraworks_xxx:astraworks.local"` → 直接使用，无需转换

**发送端信息获取**（当前 Agent）：
- `sender_id`：`POST /awp/me` 返回的 `matrix_user_id`；请求失败时 fallback 为 `agent_${cfg.nodeId}`
- `sender_name`：`POST /awp/me` 返回的 `display_name`；请求失败时 fallback 为 `cfg.nodeId`

**`displayName` 获取**：
从 `GET /api/v1/virtual-users/by-matrix/<assignee_role>` 查询 `data.display_name`；查询失败时降级为 `assignee_role` 本身。

**消息请求体**（发送到 `POST /api/v1/chat/matrix/send`）：

```json
{
  "room_id": "<task.matrix_room_id>",
  "body": "@<displayName> 使用技能：skill-cli-worker完成任务：\n\n\"todo_id\": \"<todo.id>\",\n\"title\": \"<todo.title>\",\n\"description\": \"<todo.description>\",\n\"workgroup_id\": \"<task.workgroup_id || ''>\",\n\"matrix_room_id\": \"<task.matrix_room_id>\"",
  "html": "<p><span data-type=\"mention\" class=\"mention\" data-id=\"<assignee_role>\" data-label=\"<displayName>\" data-mention-suggestion-char=\"@\" style=\"color: rgb(0, 122, 255); font-weight: 500;\">@<displayName></span> 使用技能：skill-cli-worker完成任务：</p><p>\"todo_id\": \"<todo.id>\",</p><p>\"title\": \"<todo.title>\",</p><p>\"description\": \"<todo.description>\",</p><p>\"workgroup_id\": \"<task.workgroup_id || ''>\",</p><p>\"matrix_room_id\": \"<task.matrix_room_id>\"</p>",
  "sender_id": "<current_agent_matrix_user_id>",
  "sender_name": "<current_agent_display_name>",
  "mentions": ["<assignee_role>"]
}
```

**字段说明**：
- `displayName`：从 `/api/v1/virtual-users/by-matrix/<assignee_role>` 查询得到的 `display_name`，查询失败时降级为 `assignee_role`
- `html` 中的 mention span 使用语义化格式，`data-id` 为 `assignee_role`，`data-label` 为 `displayName`；每行内容包裹在 `<p>` 标签中
- `sender_id` / `sender_name`：当前 Agent 自身标识，从 `GET /awp/me` 获取，用于在 Matrix 消息中标注发送者身份

### 3.4 返回样例

`POST /api/v1/chat/matrix/send` 返回：

```json
{
  "success": true,
  "message": "OK",
  "data": {
    "event_id": "$event_id_here"
  }
}
```

---

## Step 4：生成报告

> **执行前提**：所有 `status === "done"` 或 `status === "skipped"` 才执行。

### 4.1 检查完成状态

从 `astraworks-cli orch platform todos` 的响应中检查：

```
pending_count = todos.filter(t => t.status === "pending").length
in_progress_count = todos.filter(t => t.status === "in_progress").length
if pending_count > 0 or in_progress_count > 0:
    # 还有未完成的任务，退出本次流程
```

### 4.2 组装报告

报告 JSON 格式：

```json
{
  "room_id": "<task.matrix_room_id>",
  "task_id": "<task.id>",
  "task_title": "<task.title>",
  "task_description": "<task.description>",
  "subtasks": [
    {
      "title": "<todo.title>",
      "description": "<todo.description>"
    }
  ]
}
```

**说明**：
- `room_id` 即 `task.matrix_room_id`，用作 Matrix Room 目标地址
- `subtasks` 从 todos 中提取 `title` 和 `description`

### 4.3 写入文件

```bash
cat > /tmp/report.json << 'EOF'
<paste_report_json_here>
EOF
```

### 4.3 发送报告

```bash
astraworks-cli orch report --file /tmp/report.json --json
```

**CLI 内部实现**：
1. 读取报告 JSON 文件
2. 生成 HTML 格式报告（包含任务标题、描述、子任务列表）
3. 调用 `POST /api/v1/chat/matrix/send` 发送到 Matrix Room

**CLI 返回示例**：

```json
{
  "success": true,
  "room_id": "!abc123:astraworks.local",
  "report_file": "/tmp/report.json",
  "matrix_response": {
    "success": true,
    "data": {
      "event_id": "$event_id_here"
    }
  }
}
```

### 4.4 标记任务完成

报告成功发送到 Matrix Room 后，调用 `forcedone` 把 task 状态置为 `done`。

```bash
astraworks-cli orch forcedone <task_id> --json
```

**CLI 内部实现**：
1. 发送 `PATCH /api/v1/tasks/{task_id}/force-done` 请求
2. 认证方式：任意有效的 `X-Node-Token`（不校验 node-id 绑定）
3. 后端直接 `status=done, progress=100, completed_at=now()`，不走状态机
4. 已是 `done` 时幂等返回（不改字段）

**幂等行为**：若 task 之前已是 done，响应 `idempotent: true`，不做任何修改。

**CLI 返回示例**：

```json
{
  "success": true,
  "task_id": "5e292b1a-d160-483e-8c9d-8d2423ac063d",
  "status": "done",
  "progress": 100,
  "completed_at": "2026-06-10T...",
  "idempotent": false,
  "previous_status": "in_review"
}
```

**错误处理**：
- `401`：token 无效或过期，检查 `~/.openclaw/astraworks-connection.json` 的 token
- `404`：task_id 不存在
- `400`：task_id 格式非法

---

## 错误处理

| 场景 | 处理方式 |
|------|----------|
| platform todos 返回 404 | 确认 task_id 正确 |
| platform todos 返回 401/403 | 检查 `~/.openclaw/astraworks-connection.json` 或 `ASTRAWORKS_TOKEN` 环境变量 |
| dispatch 发送失败 | 检查 room_id 是否正确，Matrix 房间是否存在 |
| dispatch 预检查失败 | 检查 todo 的 depends_on 依赖是否都已 done |

---

## CLI 调用汇总

| 步骤 | CLI |
|------|-----|
| 获取 Todos | `astraworks-cli orch platform todos <task_id> --output <file> --json` |
| 获取可分发任务 | `astraworks-cli orch dag order <file> --json` |
| 发送分发 | `astraworks-cli orch dispatch <item_id> --todos-file <file> --json` |
| 发送报告 | `astraworks-cli orch report --file <report.json> --json` |
| 标记任务完成 | `astraworks-cli orch forcedone <task_id> --json` |

---

## 约束

- 所有 CLI 命令使用 `astraworks-cli orch` 前缀
- 使用 `--json` 标志便于 Agent 解析结构化输出
- `dag order` 和 `dispatch` 必须指定 `--todos-file`
- 所有时间戳使用 UTC ISO 8601 格式
- 连接配置从 `~/.openclaw/astraworks-connection.json` 读取（可通过 `ASTRAWORKS_TOKEN` 环境变量覆盖）
