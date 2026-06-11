---
name: task-worker-cli
description: Worker 任务执行（CLI版）— 接收分发任务，上报状态，执行并上报完成
version: 3.0.0
metadata:
  astraworks:
    capability_type: task-worker
    category: execution
    tags: [task, worker, execution, cli]
    target_agents: [WorkAgent]
---

# Worker 任务执行（Task Worker - CLI）

## 概述

本 skill 定义 WorkAgent 接收 Atlas 分发任务后的执行流程。

**核心原则**：
- 使用 `astraworks-cli orch worker start` 上报任务开始
- 使用 `astraworks-cli orch worker complete` 上报任务完成
- Agent 负责具体任务执行（Git 操作、调用其他 Skill）

---

## 前置条件

- Worker 已在 Matrix 中注册，并加入了对应的角色 Room
- Worker 收到了任务消息
- `~/.openclaw/astraworks-connection.json` 已正确配置

---

## Agent 工作流

```
Step 1: 接收任务分配消息
        解析 Matrix 消息

Step 2: 上报开始状态
        astraworks-cli orch worker start <todo_id> --json

Step 3: 执行任务
        Agent 调用其他 Skill 完成具体工作
        - Git 操作（fetch / checkout / pull / commit / push）
        - 使用工作空间下的 Skill 完成具体子任务

Step 4: 上报完成状态
        astraworks-cli orch worker complete <todo_id> --output <commit_id> --json
```

---

## Step 1：解析任务分配消息
**从消息内容提取任务信息**：
```
@agent_uuid-xxx 使用技能：skill-cli-worker完成任务：
任务ID: <todo.uuid>
<title>
<description>
```

**关键字段**：
- `todo.uuid` — 业务层唯一标识，用于后续 worker start/complete
- `title` — 任务标题
- `description` — 任务描述

---

## Step 2：上报开始状态

```bash
astraworks-cli orch worker start <todo_id> --json
```

**CLI 内部实现**：读取 `~/.openclaw/astraworks-connection.json` 配置，调用 PATCH `/awp/execute`。

**请求体**（CLI 自动构造）：

```json
{
  "todo_id": "<todo.uuid>",
  "status": "in_progress"
}
```

**CLI 返回示例**：

```json
{
  "success": true,
  "todo_id": "uuid-1",
  "status": "in_progress",
  "updated_at": "2026-05-19T10:25:00Z"
}
```

**错误处理**：

| HTTP 状态码 | 含义 | 处理 |
|-------------|------|------|
| 404 | todo_id 不存在 | 确认 todo.uuid 正确 |
| 409 | 任务已被其他 Worker 处理 | 放弃本次执行 |
| 401/403 | Token 无效 | 检查连接配置 |

---

## Step 3：执行任务

按以下顺序执行，完成后获得 Git commit id。

### 3.1 检查并切换正确分支

```bash
# 查看当前分支
git branch --show-current

# 查看远程分支
git fetch origin
git branch -r

# 切换到指定分支（如有指定）
git checkout <branch_name>

# 或基于 main 创建新分支
git checkout -b <branch_name>
```

### 3.2 拉取最新代码

```bash
# 确保本地与远程同步
git pull origin <branch_name> --rebase
```

### 3.3 获取当前 agent 的可用技能

先使用以下命令获取当前 node 下 agent 的可用技能信息：

```bash
astraworks-cli orch ownskills --json
```

从返回结果中定位当前正在执行任务的 agent，并读取其可用技能列表：
- 优先查看 `agents[].skills[].skill_name`
- 如需理解 agent 的内建能力，可辅助参考 `agents[].definition_skills`

**目标**：明确当前 agent 具备哪些可直接使用的 skill，供下一步选择。

### 3.4 从可用技能中选择合适技能完成任务

按 `subtask.title` 和 `subtask.description` 描述的任务要求，从 Step 3.3 查询到的技能中选择最合适的 skill 来完成任务：
- 优先选择与任务目标直接匹配的 skill
- 若多个 skill 都可完成，优先选择职责最单一、最贴近任务的 skill
- 若当前 agent 没有合适 skill，应先明确这一限制，再决定是否改为人工处理、切换 agent 或调整任务

执行具体工作时：
- 编写代码 / 修改配置 / 编写文档等
- 提交前确保代码可正常运行

### 3.5 提交并推送代码

```bash
# 查看变更
git status

# 添加变更文件
git add .

# 提交（描述应清晰说明改动内容）
git commit -m "feat: 完成 <任务标题>"

# 推送
git push origin <branch_name>
```

### 3.6 获取 commit id

```bash
# 获取 commit id（全长）
git rev-parse HEAD

# 获取 commit id（短格式，用于 --output）
git rev-parse --short HEAD
```

### 3.7 output_summary 规范

- `output_summary` 必须为 Git commit id（如 `a1b2c3d`）
- 如有多个仓库变更，以主仓库的 commit id 为准
- commit message 应清晰说明本次改动内容

---

## Step 4：上报完成状态

> **执行前提**：Step 3 必须已完成并获得 Git commit id。若执行失败，可上报 `failed` 状态或保持 `in_progress`。

```bash
astraworks-cli orch worker complete <todo_id> --output <commit_id> --json
```

**CLI 内部实现**：读取 `~/.openclaw/astraworks-connection.json` 配置，调用 PATCH `/awp/execute`。

**请求体**（CLI 自动构造）：

```json
{
  "todo_id": "<todo.uuid>",
  "status": "done",
  "output_summary": "<commit_id>"
}
```

**`--output` 参数格式**：Git commit id，例如 `--output a1b2c3d` 或 `--output a1b2c3d4e5f6`。

**CLI 返回示例**：

```json
{
  "success": true,
  "todo_id": "uuid-1",
  "status": "done",
  "output_summary": "a1b2c3d4e5f6",
  "updated_at": "2026-05-19T10:25:00Z"
}
```

**错误处理**：

| 场景 | 处理 |
|------|------|
| Step 3 未完成或无 commit id | 不执行 Step 4，保持 in_progress |
| Step 3 执行失败 | 可上报 `failed` 状态或保持 `in_progress` |

---


## CLI 调用汇总

| 步骤 | CLI |
|------|-----|
| 上报开始 | `astraworks-cli orch worker start <todo_id> --json` |
| 上报完成 | `astraworks-cli orch worker complete <todo_id> --output <commit_id> --json` |

---

## 约束

- 所有 CLI 命令使用 `astraworks-cli orch` 前缀
- 使用 `--json` 标志便于 Agent 解析结构化输出
- `worker start/complete` 的参数是 `subtask.id`（平台 UUID），不是 `item_id`（业务 ID）
- `output_summary` 必须为 Git commit id
- 所有时间戳使用 UTC ISO 8601 格式
- 连接配置从 `~/.openclaw/astraworks-connection.json` 读取（可通过 `ASTRAWORKS_TOKEN` 环境变量覆盖）
