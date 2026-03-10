# PICT 测试用例设计器

一个用于使用PICT（成对独立组合测试）设计全面测试用例的Skill。本技能支持通过成对组合测试以最少的测试用例保持高覆盖率进行系统化测试用例设计。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🎯 什么是PICT？

PICT（成对独立组合测试）是微软开发的组合测试工具。它生成的测试用例能有效覆盖所有参数的成对组合，与穷举测试相比大幅减少测试总数。

**示例：** 测试一个具有8个参数、每个参数3-5个值的系统：
- 穷举测试：**25,920个测试用例**
- PICT成对测试：**约30个测试用例**（减少99.88%！）

## 🚀 功能

- **自动化测试用例生成**：将需求转换为结构化的PICT模型
- **基于约束的测试**：应用业务规则消除无效组合
- **预期输出生成**：自动确定每个测试用例的预期结果
- **全面覆盖**：确保测试所有成对参数交互
- **多领域适用**：适用于软件功能、API、Web表单、配置等

## 📋 目录

- [功能说明](#功能说明)
- [快速开始](#快速开始)
- [ATM系统测试示例](#atm系统测试示例)
- [工作原理](#工作原理)
- [使用场景](#使用场景)
- [参考资料](#参考资料)

## 🔧 安装

### 前置条件

- 任何支持Skill的AI助手/Agent框架
- （可选）Python 3.7+ 和 `pypict` 用于高级用法

### 安装方法

#### 方法1：克隆到Skills目录

**OpenClaw用户：**
```bash
# 克隆到OpenClaw skills目录
git clone https://github.com/omkamal/pypict-claude-skill.git /opt/openclaw/app/skills/pict-test-designer
```

**Cursor用户：**
```bash
# 克隆到Cursor skills目录
git clone https://github.com/omkamal/pypict-claude-skill.git ~/.cursor/skills/pict-test-designer
```

**通用安装：**
```bash
# 克隆到任意skills目录
git clone https://github.com/omkamal/pypict-claude-skill.git <你的skills目录>/pict-test-designer
```

#### 方法2：下载ZIP包

从 [GitHub Releases](https://github.com/omkamal/pypict-claude-skill/releases) 下载预打包的安装包：

```bash
# 下载最新版本
wget https://github.com/omkamal/pypict-claude-skill/releases/latest/download/pict-test-designer-minimal.zip

# 解压并安装
unzip pict-test-designer-minimal.zip
mv pict-test-designer-minimal <你的skills目录>/pict-test-designer
```

### 验证安装

安装后，Skill会在相关时自动加载。你可以通过以下方式验证：

询问AI助手：
```
你能使用pict-test-designer技能吗？
```

或者直接开始使用：
```
为具有用户名、密码和记住我复选框的登录功能设计测试用例。
```

## 🚀 快速开始

安装后，只需向AI助手请求：

```
为具有用户名、密码和记住我复选框的登录功能设计测试用例。
```

AI会：
- 分析需求
- 识别参数和值
- 生成带约束的PICT模型
- 创建带预期输出的测试用例
- 以格式化表格呈现结果

## 📊 示例：ATM系统测试

本仓库包含一个完整的ATM系统测试真实示例，参见 [examples](/omkamal/pypict-claude-skill/blob/main/examples) 目录：

- [ATM规格说明](/omkamal/pypict-claude-skill/blob/main/examples/atm-specification.md)：涵盖硬件、软件、安全和功能需求的完整ATM系统规格
- [ATM测试计划](/omkamal/pypict-claude-skill/blob/main/examples/atm-test-plan.md)：使用PICT方法生成的综合测试计划，包含31个测试用例（从25,920种可能组合减少）

### ATM示例摘要

系统参数：
- 交易类型（5）：取款、存款、查询余额、转账、修改密码
- 卡类型（3）：EMV芯片卡、磁条卡、无效卡
- PIN状态（4）：有效、无效尝试1-3次
- 账户类型（3）：活期、定期、两者
- 交易金额（4）：限额内、最大额、超单笔限额、超日限额
- 现金可用性（3）：充足、不足、为零
- 网络状态（3）：主网络、备份网络、断连
- 卡状态（3）：良好、损坏、过期

测试结果：
- 总可能组合：25,920
- 生成的PICT测试用例：31
- 减少：99.88%
- 覆盖率：所有成对（2-way）交互
- 测试执行时间：从数周减少到数小时

## 🔍 工作原理

### 1. 需求分析

分析你的需求以识别：
- 参数：输入变量、配置选项、环境因素
- 值：使用等价划分的可能值
- 约束：业务规则和依赖关系
- 预期结果：不同组合应该如何

### 2. PICT模型生成

创建结构化模型：
```
# 参数
Browser: Chrome, Firefox, Safari
OS: Windows, MacOS, Linux
Memory: 4GB, 8GB, 16GB

# 约束
IF [OS] = "MacOS" THEN [Browser] <> "IE";
IF [Memory] = "4GB" THEN [OS] <> "MacOS";
```

### 3. 测试用例生成

生成覆盖所有成对组合的最小测试用例：

| Test # | Browser | OS | Memory | Expected Output |
|--------|---------|-----|--------|-----------------|
| 1 | Chrome | Windows | 4GB | Success |
| 2 | Firefox | MacOS | 8GB | Success |
| 3 | Safari | Linux | 16GB | Success |

### 4. 预期输出确定

根据以下内容确定每个测试用例的预期结果：
- 业务需求
- 代码逻辑
- 有效/无效组合

## 🎯 使用场景

### 软件测试
- 多参数的功能测试
- API端点测试
- 数据库查询测试
- 算法验证

### 配置测试
- 系统配置组合
- 特性开关测试
- 环境设置验证
- 浏览器兼容性测试

### Web应用测试
- 表单验证
- 用户认证流程
- 电商结账流程
- 购物车功能

### 移动测试
- 设备和操作系统组合
- 屏幕尺寸和方向
- 网络条件
- 应用权限

### 硬件测试
- 设备兼容性
- 接口测试
- 协议验证
- 不同条件下的性能

## 📚 文档

- [SKILL.md](/omkamal/pypict-claude-skill/blob/main/SKILL.md)：包含工作流程和最佳实践的完整技能文档
- [PICT语法参考](/omkamal/pypict-claude-skill/blob/main/references/pict_syntax.md)：完整语法指南
- [示例](/omkamal/pypict-claude-skill/blob/main/references/examples.md)：各领域真实示例
- [辅助脚本](/omomkamal/pypict-claude-skill/blob/main/scripts/pict_helper.py)：PICT的Python工具

## 💡 获得最佳结果的技巧

### 好的参数名称
- 使用描述性名称：`AuthMethod`、`UserRole`、`PaymentType`
- 应用等价划分：`FileSize: Small, Medium, Large`
- 包含边界值：`Age: 0, 17, 18, 65, 66`
- 添加负向值：`Amount: ~-1, 0, 100, ~999999`

### 编写约束
- 记录理由：`# Safari仅在MacOS上可用`
- 从简单开始，逐步增加
- 测试约束是否按预期工作

### 预期输出
- 要具体：`"登录成功，用户跳转到仪表板"`
- 不要模糊：`"可用"` 或 `"成功"`

## 🙏 致谢

本技能基于以下优秀工作：
- [Microsoft PICT](https://github.com/microsoft/pict)：微软研究院开发的原始成对独立组合测试工具
- [pypict](https://github.com/kmaehashi/pypict)：Kenichi Maehashi的PICT Python绑定

### 关于PICT

PICT由微软研究院的Jacew Czerwonka开发。它是一个强大的组合测试工具，已在微软内部广泛用于测试具有多个交互参数的复杂系统。

参考资料：
- [PICT：成对独立组合测试](https://github.com/microsoft/pict)
- [成对测试方法论](https://www.pairwisetesting.com/)
- [软件自动组合测试](https://csrc.nist.gov/projects/automated-combinatorial-testing-for-software)

## 📝 许可证

本项目基于MIT许可证 - 有关详细信息，请参阅 [LICENSE](/omkamal/pypict-claude-skill/blob/main/LICENSE) 文件。

微软的底层PICT工具也基于MIT许可证。

## 🔗 链接

- Microsoft PICT: [https://github.com/microsoft/pict](https://github.com/microsoft/pict)
- pypict: [https://github.com/kmaehashi/pypict](https://github.com/kmaehashi/pypict)
- 在线PICT工具:
  - [https://pairwise.yuuniworks.com/](https://pairwise.yuuniworks.com/)
  - [https://pairwise.teremokgames.com/](https://pairwise.teremokgames.com/)

---

如果你觉得这个技能有用，请给仓库点个星，帮助更多人发现它！

为测试社区而生 ❤️
由微软PICT和pypict驱动
