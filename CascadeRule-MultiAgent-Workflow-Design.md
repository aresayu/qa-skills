# CascadeRule 多 Agent 自动流转工作流产品设计文档

> **项目代号**：CascadeFlow  
> **版本**：v1.0  
> **基于**：astraworks-platform (AWP) + astraworks-vibe 工作流引擎  
> **目标**：支持任意自定义的 CascadeRule 多 Agent 之间自动流转功能，默认实现"产品→架构→研发→测试"流程模板 + 可视化流程设计器

---

## 目录

1. [概述](#1-概述)
2. [核心概念](#2-核心概念)
3. [系统架构](#3-系统架构)
4. [CascadeRule 数据模型](#4-cascaderule-数据模型)
5. [工作流引擎增强](#5-工作流引擎增强)
6. [预置流程模板](#6-预置流程模板)
7. [可视化流程设计器](#7-可视化流程设计器)
8. [API 设计](#8-api-设计)
9. [前端组件设计](#9-前端组件设计)
10. [实现计划](#10-实现计划)

---

## 1. 概述

### 1.1 背景与目标

现有 `astraworks-platform` 已经具备：

- **AWP (AstraWorks Workflow Protocol)**：6 阶段工作流协议（PULL → CONTEXT → PLAN → EXECUTE → DELIVER → CLOSE）
- **CascadeTriggerService**：事件驱动的下游任务创建机制（基于 GitLab MR/Issue/Pipeline 事件）
- **WorkflowEngine**：DAG 流程引擎，支持串行、并行、条件分支、审批、脚本等步骤类型
- **StepExecutor**：步骤执行器，与 Agent 通过 AWP 协议交互

当前 **CascadeRule** 仅支持预定义的外部事件触发（`mr_opened`、`pipeline_passed` 等），不支持：

1. **自定义 Agent → Agent 的级联规则**（如产品 Agent 完成后自动触发架构 Agent）
2. **可视化流程设计器**（当前仅支持 YAML 导入/导出）
3. **预置的研发流程模板**（如"产品→架构→研发→测试"标准流程）

### 1.2 设计目标

| 目标 | 描述 |
|------|------|
| **任意自定义 CascadeRule** | 支持用户定义任意两个 Agent Role 之间的级联规则，支持条件表达式 |
| **多 Agent 自动流转** | 基于规则引擎实现 Agent 之间的自动任务分发和状态同步 |
| **预置流程模板** | 提供"产品→架构→研发→测试"等常用研发流程模板，开箱即用 |
| **可视化流程设计器** | 拖拽式 DAG 编辑器，支持步骤拖放、连线、属性配置 |
| **规则可视化** | 将 CascadeRule 可视化展示在流程图中 |

### 1.3 设计原则

1. **向后兼容**：现有 CascadeTriggerService 和 WorkflowEngine 保持兼容
2. **规则优先于硬编码**：所有流转逻辑通过规则引擎驱动，而非硬编码
3. **可视化优先**：所有配置可通过可视化界面完成，YAML 仅作导出备份
4. **插件化扩展**：新增步骤类型和触发条件通过插件机制扩展

---

## 2. 核心概念

### 2.1 CascadeRule（级联规则）

**定义**：描述"当某个 Agent 完成特定任务后，自动触发下游 Agent 执行特定任务"的规则。

```yaml
cascade_rule:
  id: "rule-custom-01"
  name: "产品文档 → 架构设计"
  trigger_on:
    event: "step_completed"          # 触发事件类型
    step_type: "agent_task"          # 步骤类型过滤
    agent_role: "产品经理"            # 任意字符串，不限于预定义
    step_id_pattern: "*需求分析*"     # 步骤名称模式匹配
  condition: "output.quality_score >= 8"  # 条件表达式（可选）
  downstream:
    agent_role: "架构师"              # 任意字符串，不限于预定义
    task_template:
      title: "架构设计：{input.title}"
      description: "根据产品需求文档 {input.doc_url} 进行架构设计"
      type: "architecture"
      priority: "P1"
      labels: ["cascade", "auto-generated"]
  output_mapping:
    input: "{trigger.output}"        # 将触发步骤的输出映射为下游步骤的输入
  on_failure:
    action: "notify"
    notify_roles: ["产品经理"]        # 任意 Role 名称
```

### 2.2 Agent Role（Agent 角色）

> **重要约束**：Agent Role **不硬编码**，由用户在工作流模板或规则中**自定义声明**。
> 系统不限定角色名称，支持任意字符串（如 `"产品经理"`、`"安全审计员"`、`"法务顾问"`）。

**Role 注册机制**：

| 组件 | 职责 |
|------|------|
| **Role 注册表** | 工作流/模板声明所需 Role → 映射到 WorkGroup 中对应 Agent 实例 |
| **Role 解析器** | 运行时根据 `agent_role` 字符串，查询 WorkGroup 中该 Role 的在线 Agent |
| **Role 匹配策略** | 支持精确匹配、通配符（`*`）、正则表达式 |

**Role 声明示例**：

```yaml
# 工作流模板中声明所需 Role（声明式，不限定具体 Agent 实例）
workflow_template:
  id: "tpl-custom-workflow"
  name: "自定义工作流"
  required_roles:
    - name: "产品经理"
      description: "负责需求分析和 PRD 撰写"
      required_skills: ["需求分析", "PRD 撰写"]
    - name: "架构师"
      description: "负责技术方案设计"
      required_skills: ["系统设计", "技术选型"]
    - name: "安全审计员"
      description: "负责安全审查"
      required_skills: ["代码安全", "渗透测试"]

# CascadeRule 中使用任意 Role
cascade_rule:
  trigger:
    source_agent_role: "产品经理"    # 任意字符串
  downstream:
    agent_role: "架构师"              # 任意字符串
```

**系统预置的 5 个 Role 仅作为参考示例**，实际使用时用户可以：
1. 直接使用任意字符串作为 Role 名称
2. 在模板的 `required_roles` 中声明所需 Role
3. Role → Agent 实例的映射由系统在运行时解析

### 2.3 Workflow Template（工作流模板）

**定义**：可复用的完整工作流定义，包含步骤序列、CascadeRule、变量定义。

```yaml
workflow_template:
  id: "tpl-product-arch-dev-qa"
  name: "产品研发标准流程"
  description: "标准的"产品→架构→研发→测试"研发流程模板"
  version: "1.0.0"
  # 声明本模板所需的 Role（声明式，由系统解析到具体 Agent 实例）
  required_roles:
    - name: "产品经理"
    - name: "架构师"
    - name: "研发工程师"
    - name: "测试工程师"
    - name: "运维工程师"
  variables:
    project_name: ""
    repo_url: ""
    team_id: ""
  steps:
    - id: "step-product"
      name: "需求分析"
      type: "agent_task"
      agent_role: "产品经理"           # 任意字符串
      task_template:
        title: "需求分析：{variables.project_name}"
        type: "requirement"
      cascade_rules:
        - id: "rule-product-to-arch"
          trigger_on:
            event: "step_completed"
            step_id: "step-product"
          downstream:
            agent_role: "架构师"        # 任意字符串
```

### 2.4 Event（事件）

| 事件类型 | 描述 | 载荷数据 |
|----------|------|---------|
| `step_started` | 步骤开始执行 | `{step_id, step_name, agent_id, instance_id}` |
| `step_completed` | 步骤成功完成 | `{step_id, step_name, agent_id, instance_id, output}` |
| `step_failed` | 步骤执行失败 | `{step_id, step_name, agent_id, instance_id, error}` |
| `step_waiting` | 步骤等待外部信号 | `{step_id, step_name, agent_id, instance_id, wait_type}` |
| `handoff_requested` | Agent 间交接请求 | `{handoff_id, source_agent, target_agent, context}` |
| `handoff_accepted` | 交接请求被接受 | `{handoff_id, accepted_agent, context}` |
| `approval_requested` | 审批请求发起 | `{approval_id, step_id, approvers}` |
| `approval_completed` | 审批完成 | `{approval_id, verdict, approvers}` |

---

## 3. 系统架构

### 3.1 整体架构图

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              CascadeFlow 工作流平台                          │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐           │
│  │  可视化流程设计器  │    │  规则配置中心    │    │   模板市场      │           │
│  │  Visual Editor  │    │  Rule Config    │    │  Template Hub  │           │
│  └────────┬────────┘    └────────┬────────┘    └────────┬────────┘           │
│           │                       │                       │                   │
│           └───────────────────────┼───────────────────────┘                   │
│                                   ▼                                           │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                    CascadeFlow Backend Service                         │   │
│  │  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐         │   │
│  │  │  Workflow      │  │  CascadeRule   │  │  Event         │         │   │
│  │  │  Service       │  │  Engine        │  │  Processor     │         │   │
│  │  └───────┬────────┘  └───────┬────────┘  └───────┬────────┘         │   │
│  │          │                   │                   │                   │   │
│  │          ▼                   ▼                   ▼                   │   │
│  │  ┌──────────────────────────────────────────────────────────────┐    │   │
│  │  │              Workflow Execution Engine (DAG Runner)             │    │   │
│  │  │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐     │    │   │
│  │  │  │  PULL  │→│CONTEXT │→│  PLAN  │→│ EXECUTE │→│DELIVER │     │    │   │
│  │  │  └────────┘ └────────┘ └────────┘ └────────┘ └────────┘     │    │   │
│  │  └──────────────────────────────────────────────────────────────┘    │   │
│  │                              │                                        │   │
│  │                              ▼                                        │   │
│  │  ┌──────────────────────────────────────────────────────────────┐    │   │
│  │  │              CascadeRule Evaluator                             │    │   │
│  │  │  • 规则匹配  • 条件计算  • 下游任务创建  • 状态同步            │    │   │
│  │  └──────────────────────────────────────────────────────────────┘    │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                   │                                           │
│                                   ▼                                           │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                    OpenClaw Agent Runtime                             │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │  │
│  │  │产品经理 │  │ 架构师   │  │ 研发工程师    │  │ 测试工程师    │ │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘ │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.2 核心模块职责

| 模块 | 职责 | 技术栈 |
|------|------|--------|
| **可视化流程设计器** | 拖拽式 DAG 编辑，步骤/连线/属性配置 | React + React Flow |
| **规则配置中心** | CascadeRule 的 CRUD、可视化编辑、测试 | FastAPI + Pydantic |
| **模板市场** | 预置模板浏览、安装、分享 | FastAPI + PostgreSQL |
| **Workflow Service** | 工作流定义管理、实例管理 | FastAPI + PostgreSQL |
| **CascadeRule Engine** | 规则注册、事件监听、级联执行 | Python asyncio |
| **Event Processor** | 统一事件总线，事件分发、订阅 | Python asyncio + Redis |
| **Workflow Execution Engine** | DAG 执行引擎，步骤调度 | Python asyncio |
| **AWP Adapter** | 与 OpenClaw Agent 通信 | WebSocket + AWP Protocol |

---

## 4. CascadeRule 数据模型

### 4.1 核心数据模型

```python
# models/cascade_rule.py

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from uuid import uuid4


class TriggerEvent(str, Enum):
    """触发事件类型"""
    STEP_STARTED = "step_started"
    STEP_COMPLETED = "step_completed"
    STEP_FAILED = "step_failed"
    STEP_WAITING = "step_waiting"
    HANDOFF_REQUESTED = "handoff_requested"
    HANDOFF_ACCEPTED = "handoff_accepted"
    APPROVAL_REQUESTED = "approval_requested"
    APPROVAL_COMPLETED = "approval_completed"
    MANUAL = "manual"
    SCHEDULE = "schedule"
    WEBHOOK = "webhook"


class ConditionOperator(str, Enum):
    """条件操作符"""
    EQ = "eq"
    NE = "ne"
    GT = "gt"
    GTE = "gte"
    LT = "lt"
    LTE = "lte"
    CONTAINS = "contains"
    MATCHES = "matches"


class FailureAction(str, Enum):
    """失败处理策略"""
    STOP = "stop"
    SKIP = "skip"
    RETRY = "retry"
    NOTIFY = "notify"


class CascadeRuleCondition(BaseModel):
    """级联条件表达式"""
    field: str = Field(..., description="字段路径，如 output.quality_score")
    operator: ConditionOperator = Field(..., description="操作符")
    value: Any = Field(..., description="比较值")
    logic: Optional[str] = Field("AND", description="逻辑组合 AND/OR")


class CascadeRuleTrigger(BaseModel):
    """级联规则触发器配置"""
    event: TriggerEvent = Field(..., description="触发事件类型")
    source_agent_role: Optional[str] = Field(None, description="触发 Agent 角色")
    source_step_id_pattern: Optional[str] = Field(None, description="触发步骤 ID 模式")
    source_step_type: Optional[str] = Field(None, description="触发步骤类型")
    target_agent_role: Optional[str] = Field(None, description="目标 Agent 角色")
    conditions: Optional[List[CascadeRuleCondition]] = Field(None, description="触发条件列表")


class OutputMapping(BaseModel):
    """输入输出映射配置"""
    mappings: Dict[str, str] = Field(default_factory=dict, description="映射规则")
    pass_through_all: bool = Field(False, description="透传上游所有输出")


class DownstreamTaskConfig(BaseModel):
    """下游任务配置"""
    agent_role: str = Field(..., description="下游 Agent 角色")
    agent_id: Optional[str] = Field(None, description="指定 Agent 实例 ID")
    task_template: Dict[str, Any] = Field(default_factory=dict, description="任务模板")
    create_task: bool = Field(True, description="是否创建任务")
    task_title_template: Optional[str] = Field(None, description="任务标题模板")
    task_description_template: Optional[str] = Field(None, description="任务描述模板")
    task_type: str = Field("feature", description="任务类型")
    task_priority: str = Field("P2", description="任务优先级")
    task_labels: List[str] = Field(default_factory=lambda: ["cascade"], description="任务标签")


class CascadeRuleOnFailure(BaseModel):
    """级联失败处理配置"""
    action: FailureAction = Field(FailureAction.STOP, description="失败处理策略")
    retry_count: int = Field(0, ge=0, le=5, description="重试次数")
    retry_interval_seconds: int = Field(60, description="重试间隔秒数")
    notify_roles: Optional[List[str]] = Field(None, description="通知角色列表")
    fallback_agent_role: Optional[str] = Field(None, description="失败时回退到的 Agent 角色")


class CascadeRule(BaseModel):
    """级联规则完整定义"""
    id: str = Field(default_factory=lambda: f"rule-{uuid4().hex[:12]}")
    name: str = Field(..., min_length=1, max_length=200, description="规则名称")
    description: Optional[str] = Field(None, max_length=2000, description="规则描述")
    group: Optional[str] = Field(None, description="规则分组")
    trigger: CascadeRuleTrigger = Field(..., description="触发器配置")
    downstream: DownstreamTaskConfig = Field(..., description="下游任务配置")
    output_mapping: Optional[OutputMapping] = Field(None, description="输入输出映射")
    on_failure: CascadeRuleOnFailure = Field(
        default_factory=lambda: CascadeRuleOnFailure(),
        description="失败处理配置"
    )
    enabled: bool = Field(True, description="是否启用")
    priority: int = Field(100, ge=0, description="规则优先级")
    created_by: Optional[str] = Field(None, description="创建者")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(None, description="更新时间")
    workflow_id: Optional[str] = Field(None, description="所属工作流 ID")
    step_id: Optional[str] = Field(None, description="关联的步骤 ID")


class CascadeRuleEvaluationResult(BaseModel):
    """规则评估结果"""
    rule_id: str
    matched: bool
    condition_results: List[Dict[str, Any]] = Field(default_factory=list)
    downstream_agent_id: Optional[str] = None
    downstream_agent_role: Optional[str] = None
    task_id: Optional[str] = None
    error: Optional[str] = None
    fired_at: Optional[datetime] = None
```

### 4.2 数据库 Schema

```sql
-- cascade_rules 表
CREATE TABLE cascade_rules (
    id VARCHAR(64) PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    "group" VARCHAR(100),
    trigger_event VARCHAR(50) NOT NULL,
    source_agent_role VARCHAR(100),
    source_step_id_pattern VARCHAR(200),
    source_step_type VARCHAR(50),
    target_agent_role VARCHAR(100),
    conditions JSONB,
    downstream_agent_role VARCHAR(100) NOT NULL,
    downstream_agent_id VARCHAR(100),
    task_template JSONB,
    output_mapping JSONB,
    on_failure JSONB,
    enabled BOOLEAN DEFAULT TRUE,
    priority INTEGER DEFAULT 100,
    workflow_id VARCHAR(64),
    step_id VARCHAR(64),
    created_by VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    CONSTRAINT fk_workflow FOREIGN KEY (workflow_id) REFERENCES workflows(id) ON DELETE SET NULL
);

-- cascade_rule_executions 表
CREATE TABLE cascade_rule_executions (
    id VARCHAR(64) PRIMARY KEY,
    rule_id VARCHAR(64) NOT NULL,
    trigger_event VARCHAR(50) NOT NULL,
    trigger_context JSONB NOT NULL,
    matched BOOLEAN NOT NULL,
    downstream_agent_id VARCHAR(100),
    task_id VARCHAR(64),
    status VARCHAR(20) NOT NULL,
    error_message TEXT,
    fired_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    CONSTRAINT fk_rule FOREIGN KEY (rule_id) REFERENCES cascade_rules(id) ON DELETE CASCADE
);

CREATE INDEX idx_cascade_rules_trigger ON cascade_rules(trigger_event);
CREATE INDEX idx_cascade_rules_source_role ON cascade_rules(source_agent_role);
CREATE INDEX idx_cascade_rules_enabled ON cascade_rules(enabled);
CREATE INDEX idx_cascade_executions_rule ON cascade_rule_executions(rule_id);
```

### 4.3 Agent Role 注册表

> **核心设计**：Agent Role 不硬编码，由工作流/模板声明所需 Role，系统在运行时将 Role 解析为具体的 Agent 实例。

```python
class AgentRoleRegistry(BaseModel):
    """Agent Role 注册表"""
    
    # WorkGroup 内的 Role → Agent 实例映射
    # key: role_name (任意字符串，如 "产品经理"、"安全审计员")
    # value: 在线的 Agent 实例列表
    role_to_agents: Dict[str, List[AgentInstance]] = Field(
        default_factory=dict,
        description="Role 到 Agent 实例的映射"
    )
    
    def register_agent(self, agent: AgentInstance, roles: List[str]) -> None:
        """将 Agent 注册到多个 Role"""
        for role in roles:
            if role not in self.role_to_agents:
                self.role_to_agents[role] = []
            if agent not in self.role_to_agents[role]:
                self.role_to_agents[role].append(agent)
    
    def unregister_agent(self, agent: AgentInstance, roles: List[str]) -> None:
        """从 Role 中注销 Agent"""
        for role in roles:
            if role in self.role_to_agents:
                self.role_to_agents[role] = [
                    a for a in self.role_to_agents[role] if a.id != agent.id
                ]
    
    def resolve_role(
        self, 
        role: str, 
        workgroup_id: str,
        preferred_agent_id: Optional[str] = None
    ) -> Optional[AgentInstance]:
        """解析 Role 为具体的 Agent 实例
        
        解析策略：
        1. 如果指定了 preferred_agent_id，优先使用该 Agent
        2. 在 WorkGroup 中查找该 Role 的在线 Agent
        3. 如果有多个在线 Agent，可选使用负载均衡策略
        
        Args:
            role: Role 名称（任意字符串）
            workgroup_id: WorkGroup ID
            preferred_agent_id: 偏好的 Agent 实例 ID
            
        Returns:
            Agent 实例，或 None（如果该 Role 没有可用 Agent）
        """
        agents = self.role_to_agents.get(role, [])
        if not agents:
            return None
        
        # 过滤出在线且属于该 WorkGroup 的 Agent
        online_agents = [
            a for a in agents 
            if a.is_online and a.workgroup_id == workgroup_id
        ]
        
        if preferred_agent_id:
            # 优先使用指定的 Agent
            preferred = next(
                (a for a in online_agents if a.id == preferred_agent_id), 
                None
            )
            if preferred:
                return preferred
        
        if not online_agents:
            return None
        
        # 简单策略：返回第一个在线 Agent
        # 未来可扩展：负载均衡、Agent 能力匹配等策略
        return online_agents[0]


class WorkGroupRoleConfig(BaseModel):
    """工作组的 Role 配置"""
    workgroup_id: str
    roles: List[RoleDefinition] = Field(
        default_factory=list,
        description="工作组声明的 Role 列表"
    )


class RoleDefinition(BaseModel):
    """Role 定义"""
    name: str = Field(..., description="Role 名称（任意字符串）")
    description: Optional[str] = Field(None, description="Role 描述")
    required_skills: List[str] = Field(
        default_factory=list, 
        description="该 Role 要求的技能列表"
    )
    max_concurrent_tasks: int = Field(
        default=5, 
        ge=1,
        description="该 Role 最大并发任务数"
    )
```

**数据库 Schema**：

```sql
-- agent_roles 表（WorkGroup 中声明的 Role）
CREATE TABLE agent_roles (
    id VARCHAR(64) PRIMARY KEY,
    workgroup_id VARCHAR(64) NOT NULL,
    role_name VARCHAR(100) NOT NULL,
    description TEXT,
    required_skills JSONB DEFAULT '[]',
    max_concurrent_tasks INTEGER DEFAULT 5,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    UNIQUE (workgroup_id, role_name),
    CONSTRAINT fk_workgroup FOREIGN KEY (workgroup_id) 
        REFERENCES workgroups(id) ON DELETE CASCADE
);

-- agent_role_assignments 表（Agent 实例到 Role 的绑定）
CREATE TABLE agent_role_assignments (
    id VARCHAR(64) PRIMARY KEY,
    agent_instance_id VARCHAR(64) NOT NULL,
    workgroup_id VARCHAR(64) NOT NULL,
    role_name VARCHAR(100) NOT NULL,
    is_primary BOOLEAN DEFAULT FALSE,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (agent_instance_id, workgroup_id, role_name),
    CONSTRAINT fk_agent FOREIGN KEY (agent_instance_id) 
        REFERENCES agent_instances(id) ON DELETE CASCADE,
    CONSTRAINT fk_workgroup FOREIGN KEY (workgroup_id) 
        REFERENCES workgroups(id) ON DELETE CASCADE
);

CREATE INDEX idx_agent_roles_workgroup ON agent_roles(workgroup_id);
CREATE INDEX idx_agent_role_assignments_agent ON agent_role_assignments(agent_instance_id);
CREATE INDEX idx_agent_role_assignments_role ON agent_role_assignments(workgroup_id, role_name);
```

**Role 解析流程**：

```
CascadeRule 执行流程：
  
  1. 规则匹配成功，确定下游 agent_role = "架构师"
  2. 调用 RoleRegistry.resolve_role(role="架构师", workgroup_id="wg-xxx")
  3. 查询 agent_role_assignments 表：
     SELECT agent_instance_id 
     FROM agent_role_assignments 
     WHERE workgroup_id = 'wg-xxx' AND role_name = '架构师'
  4. 检查 Agent 实例是否在线（通过心跳机制）
  5. 返回可用的 Agent 实例 ID
  6. 创建任务并分配给该 Agent
```

### 4.4 预置 CascadeRule 示例

> **说明**：以下示例使用中文字符串作为 Role 名称，实际使用时 Role 名称可以为任意字符串。

```yaml
# 预置规则 1：产品需求 → 架构设计
- id: "preset-product-to-architecture"
  name: "产品需求 → 架构设计"
  group: "研发流程"
  trigger:
    event: "step_completed"
    source_agent_role: "产品经理"              # 任意字符串
    source_step_type: "agent_task"
    conditions:
      - field: "output.prd_approved"
        operator: "eq"
        value: true
  downstream:
    agent_role: "架构师"                       # 任意字符串
    task_template:
      title: "架构设计：{input.project_name}"
      description: "根据 PRD 文档进行技术架构设计"
      type: "architecture"
      priority: "P1"
      labels: ["cascade", "architecture"]

# 预置规则 2：架构设计 → 研发任务
- id: "preset-architecture-to-development"
  name: "架构设计 → 研发任务"
  group: "研发流程"
  trigger:
    event: "step_completed"
    source_agent_role: "架构师"               # 任意字符串
    conditions:
      - field: "output.design_approved"
        operator: "eq"
        value: true
  downstream:
    agent_role: "研发工程师"                   # 任意字符串
    task_template:
      title: "研发任务：{input.feature_name}"
      description: "根据架构设计文档实现功能"
      type: "feature"
      priority: "P2"
      labels: ["cascade", "development"]

# 预置规则 3：研发完成 → 测试
- id: "preset-development-to-qa"
  name: "研发完成 → 测试"
  group: "研发流程"
  trigger:
    event: "step_completed"
    source_agent_role: "研发工程师"            # 任意字符串
    conditions:
      - field: "output.code_review_approved"
        operator: "eq"
        value: true
      - field: "output.mr_merged"
        operator: "eq"
        value: true
  downstream:
    agent_role: "测试工程师"                   # 任意字符串
    task_template:
      title: "测试任务：{input.feature_name}"
      description: "功能开发完成，开始测试验证"
      type: "testing"
      priority: "P1"
      labels: ["cascade", "qa"]

# 预置规则 4：测试通过 → 部署
- id: "preset-qa-to-devops"
  name: "测试通过 → 部署"
  group: "发布流程"
  trigger:
    event: "step_completed"
    source_agent_role: "测试工程师"            # 任意字符串
    conditions:
      - field: "output.test_passed"
        operator: "eq"
        value: true
      - field: "output.bug_count"
        operator: "lte"
        value: 0
  downstream:
    agent_role: "运维工程师"                   # 任意字符串
    task_template:
      title: "部署发布：{input.project_name}"
      description: "所有测试通过，准备生产环境部署"
      type: "deployment"
      priority: "P0"
      labels: ["cascade", "deployment"]
```

---

## 5. 工作流引擎增强

### 5.1 增强的步骤类型

```python
class StepType(str, Enum):
    """工作流步骤类型（扩展）"""
    # === 现有类型 ===
    AGENT_TASK = "agent_task"
    HUMAN_APPROVAL = "human_approval"
    CONDITION = "condition"
    PARALLEL_GROUP = "parallel_group"
    NOTIFICATION = "notification"
    WAIT = "wait"
    WAIT_NOTIFY = "wait_notify"
    SCRIPT = "script"
    HANDOFF = "handoff"
    
    # === 新增类型 ===
    CASCADE_TRIGGER = "cascade_trigger"     # 级联触发步骤
    AGENT_CHAT = "agent_chat"               # Agent 间对话步骤
    STATE_SYNC = "state_sync"               # 状态同步步骤
```

### 5.2 级联触发器服务

```python
# cascade_rule/engine.py

from typing import Any, Dict, List, Optional, Callable
from datetime import datetime
from loguru import logger
import re


class CascadeRuleEngine:
    """级联规则引擎"""
    
    def __init__(self):
        self._rules: Dict[str, CascadeRule] = {}
        self._rules_by_event: Dict[TriggerEvent, List[str]] = {}
        self._rules_by_workflow: Dict[str, List[str]] = {}
        self._event_listeners: Dict[TriggerEvent, List[Callable]] = {}
        self._execution_history: List[CascadeRuleEvaluationResult] = []
    
    def register_rule(self, rule: CascadeRule) -> None:
        """注册级联规则"""
        self._rules[rule.id] = rule
        
        event = rule.trigger.event
        if event not in self._rules_by_event:
            self._rules_by_event[event] = []
        self._rules_by_event[event].append(rule.id)
        
        if rule.workflow_id:
            if rule.workflow_id not in self._rules_by_workflow:
                self._rules_by_workflow[rule.workflow_id] = []
            self._rules_by_workflow[rule.workflow_id].append(rule.id)
        
        logger.info(f"CascadeRuleEngine: registered rule {rule.id}")
    
    def unregister_rule(self, rule_id: str) -> bool:
        """注销级联规则"""
        if rule_id not in self._rules:
            return False
        
        rule = self._rules[rule_id]
        
        event = rule.trigger.event
        if event in self._rules_by_event:
            self._rules_by_event[event] = [
                rid for rid in self._rules_by_event[event] if rid != rule_id
            ]
        
        if rule.workflow_id and rule.workflow_id in self._rules_by_workflow:
            self._rules_by_workflow[rule.workflow_id] = [
                rid for rid in self._rules_by_workflow[rule.workflow_id] if rid != rule_id
            ]
        
        del self._rules[rule_id]
        return True
    
    def get_rule(self, rule_id: str) -> Optional[CascadeRule]:
        return self._rules.get(rule_id)
    
    def list_rules(
        self,
        workflow_id: Optional[str] = None,
        event_type: Optional[TriggerEvent] = None,
        enabled_only: bool = True,
    ) -> List[CascadeRule]:
        rules = list(self._rules.values())
        
        if workflow_id:
            rules = [r for r in rules if r.workflow_id == workflow_id]
        
        if event_type:
            rules = [r for r in rules if r.trigger.event == event_type]
        
        if enabled_only:
            rules = [r for r in rules if r.enabled]
        
        rules.sort(key=lambda r: r.priority)
        return rules
    
    async def on_event(
        self, 
        event: TriggerEvent, 
        context: Dict[str, Any]
    ) -> List[CascadeRuleEvaluationResult]:
        """触发事件处理"""
        logger.info(f"CascadeRuleEngine: received event {event}")
        
        candidate_rule_ids = self._rules_by_event.get(event, [])
        results = []
        
        for rule_id in candidate_rule_ids:
            rule = self._rules.get(rule_id)
            if not rule or not rule.enabled:
                continue
            
            result = await self._evaluate_rule(rule, context)
            results.append(result)
            
            if result.matched:
                await self._execute_rule(rule, context, result)
        
        self._execution_history.extend(results)
        return results
    
    async def _evaluate_rule(
        self, 
        rule: CascadeRule, 
        context: Dict[str, Any]
    ) -> CascadeRuleEvaluationResult:
        """评估单条规则是否匹配"""
        result = CascadeRuleEvaluationResult(
            rule_id=rule.id,
            matched=False,
            condition_results=[]
        )
        
        trigger = rule.trigger
        
        if trigger.source_agent_role:
            source_role = context.get("source_agent_role", "")
            if not self._match_pattern(source_role, trigger.source_agent_role):
                return result
        
        if trigger.source_step_id_pattern:
            source_step_id = context.get("source_step_id", "")
            if not self._match_pattern(source_step_id, trigger.source_step_id_pattern):
                return result
        
        if trigger.source_step_type:
            source_step_type = context.get("source_step_type", "")
            if source_step_type != trigger.source_step_type:
                return result
        
        if trigger.conditions:
            condition_results = await self._evaluate_conditions(
                trigger.conditions, context
            )
            result.condition_results = condition_results
            
            if not all(cr["passed"] for cr in condition_results):
                return result
        
        result.matched = True
        result.downstream_agent_role = rule.downstream.agent_role
        
        return result
    
    async def _execute_rule(
        self,
        rule: CascadeRule,
        context: Dict[str, Any],
        result: CascadeRuleEvaluationResult
    ) -> None:
        """执行级联规则"""
        try:
            agent_id = await self._resolve_downstream_agent(
                rule.downstream.agent_role,
                rule.downstream.agent_id,
                context
            )
            result.downstream_agent_id = agent_id
            
            task_data = await self._render_task_template(
                rule.downstream.task_template,
                context
            )
            
            if rule.output_mapping:
                task_data = self._apply_output_mapping(
                    task_data,
                    rule.output_mapping,
                    context
                )
            
            if rule.downstream.create_task and agent_id:
                task_id = await self._create_downstream_task(
                    agent_id=agent_id,
                    task_data=task_data,
                    rule=rule,
                    context=context
                )
                result.task_id = task_id
            
            result.fired_at = datetime.utcnow()
            
        except Exception as e:
            result.error = str(e)
            logger.error(f"CascadeRuleEngine: rule {rule.id} execution failed: {e}")
            await self._handle_failure(rule, e, context)
    
    def _match_pattern(self, value: str, pattern: str) -> bool:
        """匹配值与模式（支持 * 通配符）"""
        if pattern in ("*", ""):
            return True
        regex_pattern = pattern.replace("*", ".*")
        try:
            return bool(re.fullmatch(regex_pattern, value, re.IGNORECASE))
        except re.error:
            return value.lower() == pattern.lower()
    
    def _get_nested_value(self, obj: Dict[str, Any], path: str) -> Any:
        """获取嵌套字典中的值"""
        keys = path.split(".")
        value = obj
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
            else:
                return None
        return value
    
    def _compare_values(self, actual: Any, operator: ConditionOperator, expected: Any) -> bool:
        """比较两个值"""
        if actual is None:
            return operator == ConditionOperator.EQ and expected is None
        
        try:
            if operator == ConditionOperator.EQ:
                return actual == expected
            elif operator == ConditionOperator.NE:
                return actual != expected
            elif operator == ConditionOperator.GT:
                return actual > expected
            elif operator == ConditionOperator.GTE:
                return actual >= expected
            elif operator == ConditionOperator.LT:
                return actual < expected
            elif operator == ConditionOperator.LTE:
                return actual <= expected
            elif operator == ConditionOperator.CONTAINS:
                return expected in str(actual)
            elif operator == ConditionOperator.MATCHES:
                return bool(re.search(str(expected), str(actual)))
        except (TypeError, ValueError):
            return False
        return False
    
    async def _evaluate_conditions(
        self,
        conditions: List[CascadeRuleCondition],
        context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """评估条件列表"""
        results = []
        for condition in conditions:
            field_path = condition.field
            operator = condition.operator
            expected_value = condition.value
            
            actual_value = self._get_nested_value(context, field_path)
            passed = self._compare_values(actual_value, operator, expected_value)
            
            results.append({
                "field": field_path,
                "operator": operator.value,
                "expected": expected_value,
                "actual": actual_value,
                "passed": passed
            })
        return results
    
    async def _resolve_downstream_agent(
        self,
        agent_role: str,
        agent_id: Optional[str],
        context: Dict[str, Any]
    ) -> Optional[str]:
        """解析下游 Agent"""
        if agent_id:
            return agent_id
        
        # 从 WorkGroup 中查找对应角色的 Agent
        workgroup_id = context.get("workgroup_id")
        if workgroup_id:
            agent = await self._find_agent_by_role(workgroup_id, agent_role)
            if agent:
                return agent
        return None
    
    async def _find_agent_by_role(
        self, 
        workgroup_id: str, 
        role: str
    ) -> Optional[str]:
        """在工作组中查找对应角色的 Agent"""
        # TODO: 实现 Agent 查找逻辑
        return None
    
    async def _render_task_template(
        self,
        template: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """渲染任务模板"""
        result = {}
        for key, value in template.items():
            if isinstance(value, str):
                try:
                    value = value.format(**context)
                except (KeyError, ValueError):
                    pass
            result[key] = value
        return result
    
    def _apply_output_mapping(
        self,
        task_data: Dict[str, Any],
        output_mapping: OutputMapping,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """应用输出映射"""
        for target_field, source_expr in output_mapping.mappings.items():
            value = self._get_nested_value(context, source_expr)
            task_data[target_field] = value
        
        if output_mapping.pass_through_all:
            task_data.setdefault("context", {}).update(context)
        
        return task_data
    
    async def _create_downstream_task(
        self,
        agent_id: str,
        task_data: Dict[str, Any],
        rule: CascadeRule,
        context: Dict[str, Any]
    ) -> Optional[str]:
        """创建下游任务"""
        from capability.task_service.service import get_task_service
        
        task_service = get_task_service()
        
        title = task_data.get("title", f"Cascade Task from {rule.name}")
        description = task_data.get("description", "")
        task_type = task_data.get("type", "feature")
        priority = task_data.get("priority", "P2")
        labels = task_data.get("labels", [])
        
        task = await task_service.create_task(
            title=title,
            description=description,
            task_type=task_type,
            priority=priority,
            labels=labels,
            assignee_agent_id=agent_id,
            workgroup_id=context.get("workgroup_id"),
            metadata={
                "cascade_rule_id": rule.id,
                "trigger_instance_id": context.get("instance_id"),
                "trigger_step_id": context.get("step_id"),
            }
        )
        
        return task.get("id") if task else None
    
    async def _handle_failure(
        self,
        rule: CascadeRule,
        error: Exception,
        context: Dict[str, Any]
    ) -> None:
        """处理规则执行失败"""
        action = rule.on_failure.action
        
        if action == FailureAction.NOTIFY:
            for role in (rule.on_failure.notify_roles or []):
                await self._notify_role(role, rule, error, context)
        
        elif action == FailureAction.FALLBACK:
            if rule.on_failure.fallback_agent_role:
                await self._execute_with_fallback(
                    rule, 
                    rule.on_failure.fallback_agent_role, 
                    context
                )
```

---

## 6. 预置流程模板

### 6.1 "产品→架构→研发→测试"标准流程

```yaml
# 预置模板：产品研发标准流程 v1.0
template:
  id: "tpl-product-arch-dev-qa"
  name: "产品研发标准流程"
  description: |
    标准的软件产品研发流程，从需求分析到测试验收的完整闭环。
    包含以下阶段：
    1. 需求分析（产品经理）
    2. 架构设计（架构师）
    3. 研发实现（研发工程师）
    4. 测试验证（测试工程师）
  version: "1.0.0"
  category: "研发流程"
  tags: ["产品", "架构", "研发", "测试", "标准流程"]
  
variables:
  project_name:
    type: "string"
    required: true
    description: "项目/产品名称"
  repo_url:
    type: "string"
    description: "代码仓库地址"
  team_id:
    type: "string"
    required: true
    description: "团队 ID"
  default_priority:
    type: "string"
    default: "P2"
    description: "默认优先级"

steps:
  # ===== 阶段 1：需求分析 =====
  - id: "step-product-analysis"
    name: "需求分析"
    type: "agent_task"
    agent_role: "产品经理"
    description: "产品经理 进行需求分析，输出 PRD 文档"
    task_template:
      title: "需求分析：{variables.project_name}"
      description: |
        ## 任务描述
        对项目「{variables.project_name}」进行全面的需求分析。
        
        ## 输入
        - 项目背景：{input.background}
        - 业务目标：{input.business_goals}
        
        ## 输出
        完成《需求规格说明书》（PRD），包含：
        - 功能需求列表
        - 非功能需求
        - 用户故事地图
        - 优先级排序
      type: "requirement"
      priority: "{variables.default_priority}"
      labels: ["product", "requirement"]
    cascade_rules:
      - id: "rule-product-to-arch"
        name: "需求分析 → 架构设计"
        enabled: true
        trigger:
          event: "step_completed"
          source_agent_role: "产品经理"
          conditions:
            - field: "output.prd_approved"
              operator: "eq"
              value: true
        downstream:
          agent_role: "架构师"
          task_template:
            title: "架构设计：{variables.project_name}"
            description: |
              ## 来源
              需求分析阶段已完成，PRD 已审批通过。
              
              ## 任务
            基于《需求规格说明书》进行技术架构设计。
              
              ## PRD 链接
              {input.prd_url}
              
              ## 输出要求
              - 技术架构图
              - 核心模块设计
              - 技术选型说明
              - 接口设计
            type: "architecture"
            priority: "{variables.default_priority}"
            labels: ["architecture", "cascade"]

  # ===== 阶段 2：架构设计 =====
  - id: "step-architecture-design"
    name: "架构设计"
    type: "agent_task"
    agent_role: "架构师"
    description: "架构师 进行技术架构设计"
    depends_on: ["step-product-analysis"]
    task_template:
      title: "架构设计：{variables.project_name}"
      type: "architecture"
      labels: ["architecture"]
    cascade_rules:
      - id: "rule-arch-to-dev"
        name: "架构设计 → 研发实现"
        enabled: true
        trigger:
          event: "step_completed"
          source_agent_role: "架构师"
          conditions:
            - field: "output.design_approved"
              operator: "eq"
              value: true
        downstream:
          agent_role: "研发工程师"
          task_template:
            title: "功能研发：{input.feature_name}"
            description: "根据架构设计文档实现功能开发"
            type: "feature"
            priority: "P2"
            labels: ["development", "cascade"]

  # ===== 阶段 3：研发实现 =====
  - id: "step-development"
    name: "功能研发"
    type: "agent_task"
    agent_role: "研发工程师"
    description: "研发工程师 进行功能代码实现"
    depends_on: ["step-architecture-design"]
    task_template:
      title: "功能研发：{variables.project_name}"
      type: "feature"
      labels: ["development"]
    cascade_rules:
      - id: "rule-dev-to-qa"
        name: "研发完成 → 测试验证"
        enabled: true
        trigger:
          event: "step_completed"
          source_agent_role: "研发工程师"
          conditions:
            - field: "output.code_review_approved"
              operator: "eq"
              value: true
            - field: "output.mr_merged"
              operator: "eq"
              value: true
        downstream:
          agent_role: "测试工程师"
          task_template:
            title: "测试验证：{input.feature_name}"
            description: "功能开发完成，进入测试验证阶段"
            type: "testing"
            priority: "P1"
            labels: ["qa", "cascade"]

  # ===== 阶段 4：测试验证 =====
  - id: "step-qa"
    name: "测试验证"
    type: "agent_task"
    agent_role: "测试工程师"
    description: "测试工程师 进行测试用例执行和缺陷管理"
    depends_on: ["step-development"]
    task_template:
      title: "测试验证：{variables.project_name}"
      type: "testing"
      labels: ["qa"]
    cascade_rules:
      - id: "rule-qa-to-deploy"
        name: "测试通过 → 部署发布"
        enabled: true
        trigger:
          event: "step_completed"
          source_agent_role: "测试工程师"
          conditions:
            - field: "output.test_passed"
              operator: "eq"
              value: true
            - field: "output.bug_count"
              operator: "lte"
              value: 3
        downstream:
          agent_role: "运维工程师"
          task_template:
            title: "部署发布：{variables.project_name}"
            description: "测试全部通过，准备生产环境部署"
            type: "deployment"
            priority: "P0"
            labels: ["deployment", "cascade"]

  # ===== 阶段 5：部署发布 =====
  - id: "step-deploy"
    name: "部署发布"
    type: "agent_task"
    agent_role: "运维工程师"
    description: "运维工程师 执行 CI/CD 流水线，完成部署"
    depends_on: ["step-qa"]
    task_template:
      title: "部署发布：{variables.project_name}"
      type: "deployment"
      labels: ["deployment"]
    on_failure:
      action: "notify"
      notify_roles: ["研发工程师", "架构师"]

# 质量门禁配置
quality_gates:
  - step: "step-product-analysis"
    required_outputs: ["prd_url", "prd_approved"]
    approval_required: true
  
  - step: "step-architecture-design"
    required_outputs: ["design_doc_url", "design_approved"]
    tech_review_required: true
  
  - step: "step-development"
    required_outputs: ["mr_url", "code_review_approved", "mr_merged"]
    ci_pass_required: true
  
  - step: "step-qa"
    required_outputs: ["test_report_url", "test_passed"]
    bug_threshold: 3
```

### 6.2 模板市场

| 模板 ID | 名称 | 描述 | 适用场景 |
|---------|------|------|----------|
| `tpl-product-arch-dev-qa` | 产品研发标准流程 | "需求→架构→研发→测试"完整流程 | 通用软件产品开发 |
| `tpl-agile-scrum` | 敏捷 Scrum 流程 | Sprint 规划 → 开发 → 评审 → 回顾 | 敏捷团队 |
| `tpl-bug-fix` | Bug 修复流程 | 发现 → 定位 → 修复 → 验证 | 缺陷处理 |
| `tpl-release` | 发布流程 | 测试 → 预发布 → 正式发布 → 监控 | 版本发布 |
| `tpl-security-review` | 安全审计流程 | 代码扫描 → 漏洞修复 → 安全评审 → 上线 | 安全敏感项目 |

---

## 7. 可视化流程设计器

### 7.1 设计目标

1. **拖拽式编辑**：通过拖拽添加步骤节点、连线
2. **实时预览**：所见即所得的流程预览
3. **属性配置面板**：点击节点打开属性配置面板
4. **规则可视化**：在流程图中展示 CascadeRule 的触发关系
5. **模板支持**：从模板创建、导出为模板

### 7.2 组件架构

```
┌─────────────────────────────────────────────────────────────────┐
│                    Visual Workflow Designer                       │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌──────────────────────────────┐  ┌─────────┐ │
│  │  组件面板   │  │                              │  │  属性   │ │
│  │  Step      │  │       React Flow Canvas       │  │  配置   │ │
│  │  Palette   │  │                              │  │  Panel  │ │
│  │            │  │   [Product] → [Arch] → ...   │  │         │ │
│  │  • Agent   │  │                              │  │  Step   │ │
│  │  • Cond    │  │                              │  │  Config │ │
│  │  • Approv  │  │                              │  │         │ │
│  │  • Parallel│  │                              │  │  Rule   │ │
│  │  • Notify  │  │                              │  │  Config │ │
│  └─────────────┘  └──────────────────────────────┘  └─────────┘ │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │  Toolbar: Save | Validate | Export YAML | Preview | Undo/Redo│ │
│  └──────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### 7.3 React Flow 节点类型

```typescript
// components/workflow-designer/nodes/

// 基础节点组件
export interface BaseStepNodeData {
  stepId: string;
  stepName: string;
  stepType: StepType;
  agentRole?: string;
  status: 'idle' | 'running' | 'completed' | 'failed';
  config: Record<string, any>;
  cascadeRules: CascadeRule[];
}

// Agent Task 节点
export interface AgentTaskNodeData extends BaseStepNodeData {
  stepType: 'agent_task';
  agentRole: string;
  taskTemplate: TaskTemplate;
}

// Condition 节点
export interface ConditionNodeData extends BaseStepNodeData {
  stepType: 'condition';
  condition: string;
  branches: { label: string; targetStepId: string }[];
}

// Approval 节点
export interface ApprovalNodeData extends BaseStepNodeData {
  stepType: 'human_approval';
  approvers: string[];
  approvalStrategy: 'any_one' | 'all' | 'majority';
}

// Parallel Group 节点
export interface ParallelGroupNodeData extends BaseStepNodeData {
  stepType: 'parallel_group';
  parallelSteps: string[];
  parallelNodes?: string[];  // 可视化子节点 ID
}

// Cascade Trigger 节点（新增）
export interface CascadeTriggerNodeData extends BaseStepNodeData {
  stepType: 'cascade_trigger';
  rules: CascadeRule[];
}

// 边类型
export interface WorkflowEdgeData {
  edgeType: 'dependency' | 'condition_branch' | 'cascade';
  label?: string;
  ruleId?: string;  // 如果是 cascade 边，关联的规则 ID
  condition?: string;  // 如果是条件分支边
}
```

### 7.4 可视化规则展示

在流程图中，通过不同颜色和样式的边来区分 CascadeRule 触发的下游关系：

| 边类型 | 样式 | 描述 |
|--------|------|------|
| `dependency` | 灰色实线 | 标准的步骤依赖关系 |
| `condition_branch` | 蓝色虚线 | 条件分支，带分支标签 |
| `cascade` | 橙色波浪线 + 箭头 | Agent → Agent 级联触发 |

```
    ┌──────────────┐
    │  Product     │
    │  Analysis    │
    └──────┬───────┘
           │ (灰色依赖线)
           ▼
    ┌──────────────┐
    │  Architecture │──────┐
    │  Design      │      │ (橙色级联线)
    └──────────────┘      │
                          ▼
                   ┌──────────────┐
                   │  Development │
                   └──────────────┘
                          │
           ┌──────────────┴──────────────┐
           │ (灰色依赖线)                 │ (橙色级联线)
           ▼                             ▼
    ┌──────────────┐             ┌──────────────┐
    │  Code Review │             │     QA       │
    └──────────────┘             └──────────────┘
           │                             │
           └──────────────┬──────────────┘
                          ▼
                   ┌──────────────┐
                   │   Deploy     │
                   └──────────────┘
```

### 7.5 关键组件实现

```tsx
// components/workflow-designer/WorkflowDesigner.tsx

import React, { useCallback, useState } from 'react';
import ReactFlow, {
  Node,
  Edge,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  addEdge,
  Connection,
  Handle,
  Position,
  NodeProps,
} from 'reactflow';
import 'reactflow/dist/style.css';

import { AgentTaskNode } from './nodes/AgentTaskNode';
import { ConditionNode } from './nodes/ConditionNode';
import { ApprovalNode } from './nodes/ApprovalNode';
import { ParallelGroupNode } from './nodes/ParallelGroupNode';
import { CascadeTriggerNode } from './nodes/CascadeTriggerNode';
import { StepPalette } from './StepPalette';
import { PropertiesPanel } from './PropertiesPanel';
import { WorkflowToolbar } from './WorkflowToolbar';

const nodeTypes = {
  agent_task: AgentTaskNode,
  condition: ConditionNode,
  human_approval: ApprovalNode,
  parallel_group: ParallelGroupNode,
  cascade_trigger: CascadeTriggerNode,
};

export interface WorkflowDesignerProps {
  initialWorkflow?: WorkflowDefinition;
  onSave: (workflow: WorkflowDefinition) => void;
  onValidate: (workflow: WorkflowDefinition) => ValidationResult;
  onExport: (workflow: WorkflowDefinition) => string;
}

export function WorkflowDesigner({
  initialWorkflow,
  onSave,
  onValidate,
  onExport,
}: WorkflowDesignerProps) {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialWorkflow?.nodes || []);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialWorkflow?.edges || []);
  const [selectedNode, setSelectedNode] = useState<Node | null>(null);
  const [workflow, setWorkflow] = useState<WorkflowDefinition>(initialWorkflow);

  const onConnect = useCallback(
    (params: Connection) => {
      const newEdge = {
        ...params,
        type: 'workflow-edge',
        animated: false,
        style: { stroke: '#94a3b8' },
      };
      setEdges((eds) => addEdge(newEdge, eds));
    },
    [setEdges]
  );

  const onNodeClick = useCallback((_: React.MouseEvent, node: Node) => {
    setSelectedNode(node);
  }, []);

  const onNodeDragStop = useCallback(
    (_: React.MouseEvent, node: Node) => {
      // 更新节点位置到 workflow 定义
    },
    []
  );

  const handleSave = useCallback(() => {
    if (workflow) {
      onSave(workflow);
    }
  }, [workflow, onSave]);

  const handleValidate = useCallback(() => {
    if (workflow) {
      const result = onValidate(workflow);
      if (!result.valid) {
        alert(`验证失败：\n${result.errors.map((e) => e.message).join('\n')}`);
      } else {
        alert('验证通过！');
      }
    }
  }, [workflow, onValidate]);

  const handleExport = useCallback(() => {
    if (workflow) {
      const yaml = onExport(workflow);
      // 下载 YAML 文件
      const blob = new Blob([yaml], { type: 'text/yaml' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${workflow.name}.yaml`;
      a.click();
    }
  }, [workflow, onExport]);

  return (
    <div className="workflow-designer h-screen flex flex-col">
      <WorkflowToolbar
        onSave={handleSave}
        onValidate={handleValidate}
        onExport={handleExport}
        onUndo={() => {}}
        onRedo={() => {}}
      />

      <div className="flex-1 flex">
        <StepPalette />

        <div className="flex-1">
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onConnect={onConnect}
            onNodeClick={onNodeClick}
            nodeTypes={nodeTypes}
            fitView
            snapToGrid
            snapGrid={[15, 15]}
          >
            <Background />
            <Controls />
          </ReactFlow>
        </div>

        {selectedNode && (
          <PropertiesPanel
            node={selectedNode}
            onClose={() => setSelectedNode(null)}
            onUpdate={(updatedNode) => {
              setNodes((nds) =>
                nds.map((n) => (n.id === updatedNode.id ? updatedNode : n))
              );
            }}
          />
        )}
      </div>
    </div>
  );
}
```

### 7.6 CascadeRule 可视化编辑器

```tsx
// components/workflow-designer/CascadeRuleEditor.tsx

import React, { useState } from 'react';
import { CascadeRule, TriggerEvent, ConditionOperator } from '@/types';

interface CascadeRuleEditorProps {
  rule?: CascadeRule;
  stepId: string;
  availableAgentRoles: string[];
  onSave: (rule: CascadeRule) => void;
  onDelete?: () => void;
}

export function CascadeRuleEditor({
  rule,
  stepId,
  availableAgentRoles,
  onSave,
  onDelete,
}: CascadeRuleEditorProps) {
  const [formData, setFormData] = useState<CascadeRule>(
    rule || {
      id: `rule-${Date.now()}`,
      name: '',
      trigger: {
        event: TriggerEvent.STEP_COMPLETED,
        source_agent_role: '',
        conditions: [],
      },
      downstream: {
        agent_role: availableAgentRoles[0] || '研发工程师',
        task_template: {},
        create_task: true,
      },
      enabled: true,
      priority: 100,
    }
  );

  const handleAddCondition = () => {
    setFormData((prev) => ({
      ...prev,
      trigger: {
        ...prev.trigger,
        conditions: [
          ...(prev.trigger.conditions || []),
          { field: '', operator: ConditionOperator.EQ, value: '' },
        ],
      },
    }));
  };

  const handleConditionChange = (
    index: number,
    field: string,
    value: any
  ) => {
    setFormData((prev) => ({
      ...prev,
      trigger: {
        ...prev.trigger,
        conditions: prev.trigger.conditions?.map((c, i) =>
          i === index ? { ...c, [field]: value } : c
        ),
      },
    }));
  };

  return (
    <div className="cascade-rule-editor p-4 space-y-4">
      <div className="text-sm font-medium text-gray-700">CascadeRule 配置</div>

      {/* 规则名称 */}
      <div>
        <label className="block text-xs text-gray-500 mb-1">规则名称</label>
        <input
          type="text"
          value={formData.name}
          onChange={(e) => setFormData((p) => ({ ...p, name: e.target.value }))}
          className="w-full px-3 py-2 border rounded-md"
          placeholder="如：需求分析 → 架构设计"
        />
      </div>

      {/* 触发条件 */}
      <div>
        <label className="block text-xs text-gray-500 mb-1">触发事件</label>
        <select
          value={formData.trigger.event}
          onChange={(e) =>
            setFormData((p) => ({
              ...p,
              trigger: { ...p.trigger, event: e.target.value as TriggerEvent },
            }))
          }
          className="w-full px-3 py-2 border rounded-md"
        >
          <option value={TriggerEvent.STEP_STARTED}>步骤开始</option>
          <option value={TriggerEvent.STEP_COMPLETED}>步骤完成</option>
          <option value={TriggerEvent.STEP_FAILED}>步骤失败</option>
          <option value={TriggerEvent.STEP_WAITING}>步骤等待</option>
        </select>
      </div>

      {/* 条件表达式 */}
      <div>
        <div className="flex items-center justify-between mb-2">
          <label className="text-xs text-gray-500">触发条件</label>
          <button
            type="button"
            onClick={handleAddCondition}
            className="text-xs text-blue-600 hover:underline"
          >
            + 添加条件
          </button>
        </div>

        {formData.trigger.conditions?.map((condition, index) => (
          <div key={index} className="flex gap-2 mb-2 items-center">
            <input
              type="text"
              value={condition.field}
              onChange={(e) =>
                handleConditionChange(index, 'field', e.target.value)
              }
              className="flex-1 px-2 py-1 border rounded text-xs"
              placeholder="字段路径，如 output.quality"
            />
            <select
              value={condition.operator}
              onChange={(e) =>
                handleConditionChange(
                  index,
                  'operator',
                  e.target.value as ConditionOperator
                )
              }
              className="px-2 py-1 border rounded text-xs"
            >
              <option value={ConditionOperator.EQ}>等于</option>
              <option value={ConditionOperator.NE}>不等于</option>
              <option value={ConditionOperator.GT}>大于</option>
              <option value={ConditionOperator.LTE}>小于等于</option>
              <option value={ConditionOperator.CONTAINS}>包含</option>
            </select>
            <input
              type="text"
              value={condition.value}
              onChange={(e) =>
                handleConditionChange(index, 'value', e.target.value)
              }
              className="w-24 px-2 py-1 border rounded text-xs"
              placeholder="值"
            />
          </div>
        ))}
      </div>

      {/* 下游 Agent */}
      <div>
        <label className="block text-xs text-gray-500 mb-1">下游 Agent 角色</label>
        <select
          value={formData.downstream.agent_role}
          onChange={(e) =>
            setFormData((p) => ({
              ...p,
              downstream: { ...p.downstream, agent_role: e.target.value },
            }))
          }
          className="w-full px-3 py-2 border rounded-md"
        >
          {availableAgentRoles.map((role) => (
            <option key={role} value={role}>
              {role}
            </option>
          ))}
        </select>
      </div>

      {/* 操作按钮 */}
      <div className="flex gap-2 pt-4 border-t">
        <button
          type="button"
          onClick={() => onSave(formData)}
          className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
        >
          保存规则
        </button>
        {onDelete && (
          <button
            type="button"
            onClick={onDelete}
            className="px-4 py-2 text-red-600 border border-red-600 rounded-md hover:bg-red-50"
          >
            删除
          </button>
        )}
      </div>
    </div>
  );
}
```

---

## 8. API 设计

### 8.1 CascadeRule API

```
POST   /api/v1/cascade-rules              # 创建级联规则
GET    /api/v1/cascade-rules              # 列出级联规则
GET    /api/v1/cascade-rules/{rule_id}    # 获取单个规则
PUT    /api/v1/cascade-rules/{rule_id}    # 更新规则
DELETE /api/v1/cascade-rules/{rule_id}    # 删除规则
POST   /api/v1/cascade-rules/{rule_id}/test  # 测试规则执行
GET    /api/v1/cascade-rules/executions  # 获取规则执行历史
```

### 8.2 API 请求/响应示例

```json
// POST /api/v1/cascade-rules
// Request
{
  "name": "产品需求 → 架构设计",
  "description": "当产品需求分析完成且 PRD 审批通过后，自动触发架构设计任务",
  "group": "研发流程",
  "trigger": {
    "event": "step_completed",
    "source_agent_role": "产品经理",
    "conditions": [
      {
        "field": "output.prd_approved",
        "operator": "eq",
        "value": true
      }
    ]
  },
  "downstream": {
    "agent_role": "架构师",
    "create_task": true,
    "task_template": {
      "title": "架构设计：{input.project_name}",
      "description": "根据 PRD 进行技术架构设计",
      "type": "architecture",
      "priority": "P1",
      "labels": ["cascade", "architecture"]
    }
  },
  "enabled": true,
  "priority": 100,
  "workflow_id": "wf-xxx",
  "step_id": "step-product"
}

// Response
{
  "id": "rule-abc123",
  "name": "产品需求 → 架构设计",
  "description": "...",
  "group": "研发流程",
  "trigger": {...},
  "downstream": {...},
  "enabled": true,
  "priority": 100,
  "created_at": "2026-04-27T09:00:00Z",
  "created_by": "user-xxx"
}
```

### 8.3 Workflow Template API

```
POST   /api/v1/workflow-templates              # 创建工作流模板
GET    /api/v1/workflow-templates              # 列出工作流模板
GET    /api/v1/workflow-templates/{template_id}  # 获取模板详情
PUT    /api/v1/workflow-templates/{template_id}  # 更新模板
DELETE /api/v1/workflow-templates/{template_id}  # 删除模板
POST   /api/v1/workflow-templates/{template_id}/instantiate  # 从模板创建工作流实例
GET    /api/v1/workflow-templates/market       # 获取模板市场列表
POST   /api/v1/workflow-templates/{template_id}/publish  # 发布到模板市场
```

---

## 9. 前端组件设计

### 9.1 组件列表

| 组件 | 描述 | 位置 |
|------|------|------|
| `WorkflowDesigner` | 可视化流程设计器主组件 | `components/workflow-designer/` |
| `StepPalette` | 步骤类型面板（左侧拖拽源） | `components/workflow-designer/` |
| `PropertiesPanel` | 属性配置面板（右侧） | `components/workflow-designer/` |
| `WorkflowToolbar` | 工具栏（保存、验证、导出） | `components/workflow-designer/` |
| `AgentTaskNode` | Agent 任务节点 | `components/workflow-designer/nodes/` |
| `ConditionNode` | 条件分支节点 | `components/workflow-designer/nodes/` |
| `ApprovalNode` | 审批节点 | `components/workflow-designer/nodes/` |
| `ParallelGroupNode` | 并行组节点 | `components/workflow-designer/nodes/` |
| `CascadeTriggerNode` | 级联触发节点 | `components/workflow-designer/nodes/` |
| `CascadeRuleEditor` | 级联规则编辑器 | `components/workflow-designer/` |
| `WorkflowGraph` | 工作流执行状态图 | `components/workflow/` |
| `WorkflowList` | 工作流列表 | `pages/WorkflowList.tsx` |
| `TemplateMarket` | 模板市场 | `pages/TemplateMarket.tsx` |
| `RuleList` | 规则列表 | `pages/RuleList.tsx` |

### 9.2 页面路由

```
/workflows                           # 工作流列表
/workflows/new                        # 创建工作流（打开设计器）
/workflows/:id/edit                   # 编辑工作流
/workflows/:id/instances              # 工作流实例列表
/workflows/:id/instances/:instanceId  # 实例详情
/workflows/templates                  # 模板管理
/workflows/templates/market           # 模板市场
/rules                                # 级联规则列表
/rules/new                            # 创建规则
/rules/:id                            # 编辑规则
```

---

## 10. 实现计划

### 10.1 阶段划分

| 阶段 | 名称 | 主要交付物 | 预计工期 |
|------|------|-----------|----------|
| **Phase 1** | 基础设施 | CascadeRule 数据模型、API、数据库 Schema | 2 周 |
| **Phase 2** | 规则引擎 | CascadeRuleEngine 核心逻辑、事件处理 | 2 周 |
| **Phase 3** | 预置模板 | "产品→架构→研发→测试"模板 + 4 条预置规则 | 1 周 |
| **Phase 4** | 可视化设计器 | React Flow 集成、节点组件、属性面板 | 3 周 |
| **Phase 5** | 规则可视化 | 级联关系在流程图中的可视化展示 | 1 周 |
| **Phase 6** | 集成测试 | 与现有 WorkflowEngine、AWP 协议集成测试 | 2 周 |
| **Phase 7** | 上线部署 | 文档、监控、告警配置 | 1 周 |

**总工期**：约 12 周

### 10.2 Phase 1 详细任务

1. 设计并创建 `cascade_rules` 和 `cascade_rule_executions` 表
2. 实现 `CascadeRule` Pydantic 模型
3. 实现 `CascadeRuleRepository` 数据访问层
4. 实现 `CascadeRuleService` 业务逻辑层
5. 实现 REST API 端点
6. 编写单元测试

### 10.3 Phase 2 详细任务

1. 实现 `CascadeRuleEngine` 类
2. 实现规则注册、注销、查询功能
3. 实现事件监听和规则匹配逻辑
4. 实现条件下游任务创建
5. 实现失败处理策略
6. 实现与 `WorkflowEngine` 的集成

### 10.4 技术依赖

- **前端**：React 18+, React Flow, Tailwind CSS, React Query
- **后端**：Python 3.11+, FastAPI, Pydantic v2, SQLAlchemy 2.0
- **数据库**：PostgreSQL 15+, Redis（可选，用于事件队列）
- **测试**：pytest, pytest-asyncio, Playwright

### 10.5 风险与应对

| 风险 | 影响 | 应对措施 |
|------|------|---------|
| 规则循环依赖 | 工作流死循环 | 引入规则依赖图检测，限制最大级联深度 |
| 规则性能问题 | 大量规则时事件处理慢 | 按事件类型索引规则，引入规则缓存 |
| 与现有 AWP 协议冲突 | 集成失败 | 保持向后兼容，新增接口独立部署 |
| 可视化设计器复杂度 | 开发周期长 | 使用成熟的 React Flow，先实现核心功能 |

---

## 附录

### A. 术语表

| 术语 | 英文 | 定义 |
|------|------|------|
| 级联规则 | CascadeRule | 描述 Agent 间任务自动触发关系的规则 |
| 触发事件 | Trigger Event | 导致规则评估的事件，如步骤完成 |
| 下游任务 | Downstream Task | 规则触发后创建的任务 |
| 规则引擎 | Rule Engine | 执行规则匹配和任务创建的系统 |
| 模板市场 | Template Market | 分享和发现工作流模板的平台 |

### B. 参考资料

- astraworks-platform/backend/coordination/workflow_engine/ — 现有工作流引擎
- astraworks-platform/backend/coordination/workflow_engine/cascade_trigger.py — 现有级联触发器
- astraworks-vibe/packages/shared-ui/src/components/workflow/ — 现有流程图组件
- React Flow 官方文档：https://reactflow.dev/

### C. 变更记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|---------|------|
| 2026-04-27 | v1.0 | 初始版本 | CascadeFlow Team |

---

_本文档基于现有 astraworks-platform 和 astraworks-vibe 代码库实现设计_
