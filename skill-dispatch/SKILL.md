---
name: task-dispatch
description: 任务分发 — 读取 Checklist，按 DAG 依赖分发任务给 Worker
version: 1.2.0
metadata:
  astraworks:
    capability_type: task-dispatch
    category: execution
    tags: [task, dispatch, subtask]
    target_agents: [Atlas]
---

# 任务分发（Task Dispatch）

## 概述

本 skill 定义 Agent 协调任务分发的工作流程。

**核心原则**：
- Agent 负责任务决策（分发谁、如何处理进度报告）
- 平台工具负责长循环（监听事件、发送消息）
- Agent 按指令调用工具，不需要代码调用 LLM

---

## Agent 工作流

1. **加载 Checklist**：读取连接配置 → curl 获取 Todo List → 生成 topological_order
2. **分发任务**：遍历 topological_order，对可分发的任务调用 `matrix_send_message` 发送分发消息
3. **生成报告**：所有 Todo 完成后，组装报告并通过 `matrix_send_message` 发送

---

## Step 1：加载 Checklist

Agent 读取配置文件，构造 curl 请求获取当前 Todo List，生成带完成状态的 topological_order。

### 1.1 读取连接配置

从配置文件 `~/.openclaw/astraworks-connection.json` 读取三个字段：

| 字段 | 说明 |
|------|------|
| `nodeId` | Node ID，用于 URL query 参数 |
| `token` | Node Token，用于 `X-Node-Token` 请求头 |
| `platformUrl` | AstraWorks 平台基础地址 |

> 配置文件路径：`~/.openclaw/astraworks-connection.json`

示例配置文件内容：

```json
{
  "nodeId": "node-926587b6",
  "token": "tk_cd1b24cf347ae7629f50885897a680fb",
  "platformUrl": "https://nondeprecating-sommer-cantoral.ngrok-free.dev"
}
```

### 1.2 构造并发送 curl 请求

**curl 请求格式**：

```bash
curl -s -X GET "{platformUrl}/awp/tasks/{task_id}/todos?node_id={nodeId}" \
  -H "X-Node-Token: {token}"
```

> 注意：使用 GET 方法

### 1.3 解析响应，构建 topological_order

响应格式示例（参见 `todo_example.json`）：

```json
{
  "todos": [
    {
      "id": "a95abdcc-e92c-4f71-9bfa-da95c0cb2bfa",
      "task_id": "c8fd3085-d7c0-4fbf-a824-6a6d7cd4b83e",
      "title": "需求分析与PRD输出",
      "description": "...",
      "status": "pending",
      "order": 0,
      "progress_pct": 0,
      "output_summary": null,
      "item_id": "item-2-1",
      "type": "analysis",
      "depends_on": [],
      "required_skills": ["analysis"],
      "assignee_role": "Analyst",
      "created_at": "2026-05-19T06:24:13.652397",
      "updated_at": "2026-05-19T06:24:13.652397"
    },
    ...
  ]
}
```

### 1.4 带完成状态的 topological_order 模板

基于上述响应结果，按 DAG 依赖关系和 `order` 字段排序，生成如下结构：

```yaml
topological_order:
  - id: "a95abdcc-e92c-4f71-9bfa-da95c0cb2bfa"
    item_id: "item-2-1"
    title: "需求分析与PRD输出"
    type: "analysis"
    status: "done"
    assignee_role: "Analyst"
    depends_on: []
    completed: true

  - id: "9d1cd9a7-f55a-4890-95e1-081466ed8ba9"
    item_id: "item-2-2"
    title: "技术方案与API接口设计"
    type: "other"
    status: "pending"
    assignee_role: "Designer"
    depends_on: ["item-2-1"]
    completed: false

  - id: "563e9e31-5b2a-48c4-a50a-42635d244237"
    item_id: "item-2-3"
    title: "数据库用户表设计"
    type: "other"
    status: "pending"
    assignee_role: "Designer"
    depends_on: ["item-2-1"]
    completed: false

  - id: "c02dbfa8-d45a-492c-86d1-019a7ad6a408"
    item_id: "item-2-4"
    title: "后端登录API开发"
    type: "implementation"
    status: "pending"
    assignee_role: "Coder"
    depends_on: ["item-2-2", "item-2-3"]
    completed: false

  - id: "9baaa61d-dca8-4bf7-9de5-52b4b26337b4"
    item_id: "item-2-5"
    title: "前端登录页面开发"
    type: "implementation"
    status: "pending"
    assignee_role: "Coder"
    depends_on: ["item-2-2", "item-2-4"]
    completed: false

  - id: "f4293d56-df35-4b93-86f6-3eb55fe3383e"
    item_id: "item-2-6"
    title: "安全与权限测试"
    type: "testing"
    status: "pending"
    assignee_role: "QA"
    depends_on: ["item-2-4", "item-2-5"]
    completed: false

  - id: "89ca3c6f-f517-4e4a-a422-9b90fe5ace6d"
    item_id: "item-2-7"
    title: "集成测试与验收"
    type: "testing"
    status: "pending"
    assignee_role: "QA"
    depends_on: ["item-2-6"]
    completed: false
```

其中 `completed` 字段由 Agent 根据 `status` 计算得出：

```
completed = (status === "done" or status === "skipped")
```

### 1.5 校验 Checklist

检查:
  - todos 列表非空 → 空则返回错误
  - todos[].item_id 唯一 → 重复则返回错误
  - DAG 无循环依赖 → 有环则返回错误

---

## Step 2：分发任务

Agent 按 `topological_order` 遍历，对每个可分发的子任务：

### 2.1 判断是否可分发

```
can_dispatch(subtask) 当且仅当：
  - subtask.status === "pending"
  - subtask.depends_on 所有 item_id 均对应的 todo.status === "done"
```

### 2.2 选择执行者

```
选择策略（按优先级）:
  1. subtask.assignee_role 匹配可用 Agent
  2. required_skills 匹配可用 Agent
  3. 默认分配给 Coder 角色
```

### 2.3 发送分发消息

```
工具: matrix_send_message
输入:
  {
    room_id: get_room_for_role(subtask.assignee_role),
    type: "com.astraworks.task.assigned",
    content: {
      msg_id: "dispatch-{uuid}",
      task_id: "task-xxx",
      subtask: {
        id: subtask.id,
        item_id: subtask.item_id,
        title: subtask.title,
        description: subtask.description,
        type: subtask.type,
        required_skills: subtask.required_skills,
        depends_on: subtask.depends_on,
        assignee_role: subtask.assignee_role,
      }
    }
  }
```

---

## Step 3：生成报告

当所有 `subtasks[].status === "done"` 或有 `status === "skipped"` 时：

### 3.1 Agent 组装报告

```yaml
report:
  version: "1.0"
  skill_name: "task-dispatch"

  task_info:
    task_id: "task-xxx"
    title: "实现用户登录功能"

  generated_at: "2024-01-01T14:00:00Z"

  summary:
    total_subtasks: 7
    done: 7
    skipped: 0
    success_rate: "100.0%"

  subtasks_detail:
    - id: "a95abdcc-e92c-4f71-9bfa-da95c0cb2bfa"
      item_id: "item-2-1"
      title: "需求分析与PRD输出"
      assignee_role: "Analyst"
      status: "done"
      completed_at: "2024-01-01T10:25:00Z"
      actual_duration_minutes: 20
      output_summary: "输出PRD文档"

  issues_encountered: []
  next_steps:
    - "建议进行端到端测试"
```

### 3.2 发送报告到 Matrix 群

```
工具: matrix_send_message
输入:
  {
    room_id: get_default_room(),
    type: "com.astraworks.execution.report",
    content: { report }
  }
```

---

## 平台工具定义

### matrix_send_message

发送 Matrix 消息。

```
输入: { room_id, type, content }
输出: { success, msg_id, error? }
```

---

## 约束

- 执行前必须存在有效的 Todo List（从 API 获取）
- todos 必须非空
- DAG 无循环依赖
- Agent 按本指令调用平台工具
- 所有时间戳使用 UTC ISO 8601
- 连接配置从 `~/.openclaw/astraworks-connection.json` 读取
