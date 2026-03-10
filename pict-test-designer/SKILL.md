---
name: pict-test-designer
description: 使用PICT（成对独立组合测试）设计全面的测试用例。分析需求或代码，生成包含参数、值和约束的PICT模型，输出测试用例表格和预期结果。适用于任何AI模型。
---

# PICT 测试用例设计器

本技能支持使用PICT（成对独立组合测试）进行系统化的测试用例设计。根据需求或代码，分析系统以识别测试参数，生成带有适当约束的PICT模型，将结果格式化为带预期输出的测试用例。

## 何时使用本技能

当出现以下情况时使用本技能：
- 为具有多个输入参数的功能、函数或系统设计测试用例
- 为具有多种组合的配置创建测试套件
- 需要用最少的测试用例实现全面覆盖
- 分析需求以识别测试场景
- 处理具有多个条件路径的代码
- 为API端点、Web表单或系统配置构建测试矩阵

## 工作流程

按以下流程进行测试设计：

### 1. 分析需求或代码

从用户的需求或代码中识别：
- **参数**：输入变量、配置选项、环境因素
- **值**：每个参数的可能值（使用等价划分）
- **约束**：业务规则、技术限制、参数之间的依赖关系
- **预期结果**：不同组合应该发生什么

**分析示例：**

对于登录功能需求：
- 用户可以使用用户名/密码登录
- 支持2FA（开/关）
- 在受信任设备上记住登录
- 3次失败后限制速率

识别的参数：
- 凭证：有效、无效
- 双因素认证：启用、禁用
- 记住我：勾选、未勾选
- 之前失败次数：0、1、2、3、4

### 2. 生成PICT模型

创建包含以下内容的PICT模型：
- 清晰的参数名称
- 明确定义的值集（使用等价划分和边界值）
- 无效组合的约束
- 解释业务规则的注释

**模型结构：**
```
# 参数定义
参数名: 值1, 值2, 值3

# 约束（如果有）
IF [参数1] = "值" THEN [参数2] <> "其他值";
```

**参考references/pict_syntax.md获取：**
- 完整语法参考
- 约束语法和运算符
- 高级功能（子模型、别名、负向测试）
- 命令行选项
- 详细约束模式

**参考references/examples.md获取：**
- 各领域的完整真实示例
- 软件功能测试示例
- Web应用、API和移动测试示例
- 数据库和配置测试模式
- 认证、资源访问、错误处理的常见模式

### 3. 执行PICT模型

生成PICT模型文本并格式化给用户。你可以直接使用Python代码来处理模型：

```python
# 定义参数和约束
parameters = {
    "OS": ["Windows", "Linux", "MacOS"],
    "Browser": ["Chrome", "Firefox", "Safari"],
    "Memory": ["4GB", "8GB", "16GB"]
}

constraints = [
    'IF [OS] = "MacOS" THEN [Browser] IN {Safari, Chrome}',
    'IF [Memory] = "4GB" THEN [OS] <> "MacOS"'
]

# 生成模型文本
model_lines = []
for param_name, values in parameters.items():
    values_str = ", ".join(values)
    model_lines.append(f"{param_name}: {values_str}")

if constraints:
    model_lines.append("")
    for constraint in constraints:
        if not constraint.endswith(';'):
            constraint += ';'
        model_lines.append(constraint)

model_text = "\n".join(model_lines)
print(model_text)
```

**使用辅助脚本（可选）：**
`scripts/pict_helper.py`脚本提供模型生成和输出格式化的工具：

```bash
# 从JSON配置生成模型
python scripts/pict_helper.py generate config.json

# 将PICT工具输出格式化为markdown表格
python scripts/pict_helper.py format output.txt

# 解析PICT输出为JSON
python scripts/pict_helper.py parse output.txt
```

**生成实际测试用例**，用户可以：
1. 将PICT模型保存到文件（例如`model.txt`）
2. 使用在线PICT工具：
   - https://pairwise.yuuniworks.com/
   - https://pairwise.teremokgames.com/
3. 或在本地安装PICT（参见references/pict_syntax.md）

### 4. 确定预期输出

根据以下内容确定每个生成的测试用例的预期结果：
- 业务需求
- 代码逻辑
- 有效/无效组合

创建与每个测试用例对应的预期输出列表。

### 5. 格式化完整测试套件

向用户提供：
1. **PICT模型** - 带有参数和约束的完整模型
2. **Markdown表格** - 带测试编号的测试用例表格
3. **预期输出** - 每个测试用例的预期结果

## 输出格式

按以下结构呈现结果：

````markdown
## PICT模型

```
# 参数
参数1: 值1, 值2, 值3
参数2: 值A, 值B

# 约束
IF [参数1] = "值1" THEN [参数2] = "值A";
```

## 生成的测试用例

| 测试 # | 参数1 | 参数2 | 预期输出 |
| --- | --- | --- | --- |
| 1 | 值1 | 值A | 成功 |
| 2 | 值2 | 值B | 成功 |
| 3 | 值1 | 值B | 错误: 无效组合 |
...

## 测试用例摘要

- 总测试用例数: N
- 覆盖率: 成对测试（所有2-way组合）
- 应用的约束: N
````

## 最佳实践

### 参数识别

**好的做法：**
- 使用描述性名称：`AuthMethod`、`UserRole`、`PaymentType`
- 应用等价划分：`FileSize: Small, Medium, Large`，而不是 `FileSize: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10`
- 包含边界值：`Age: 0, 17, 18, 65, 66`
- 添加负向值用于错误测试：`Amount: ~-1, 0, 100, ~999999`

**避免：**
- 通用名称：`Param1`、`Value1`、`V1`
- 没有划分的过多值
- 遗漏边界情况

### 约束编写

**好的做法：**
- 记录理由：`# Safari仅在MacOS上可用`
- 从简单开始，逐步增加
- 测试约束是否按预期工作

**避免：**
- 过度约束（消除太多有效组合）
- 约束不足（生成无效测试用例）
- 复杂嵌套逻辑而没有清晰文档

### 预期输出定义

**要具体：**
- "登录成功，用户跳转到仪表板"
- "HTTP 400: 凭据无效错误"
- "显示2FA提示"

**不要模糊：**
- "可用"
- "错误"
- "成功"

### 可扩展性

对于大型参数集：
- 使用子模型对相关参数进行分组
- 考虑将不相关的功能分离为单独的测试套件
- 从order 2（成对）开始，对关键组合增加
- 典型的成对测试将测试用例减少80-90%vs穷举测试

## 常见模式

### Web表单测试

```python
parameters = {
    "Name": ["Valid", "Empty", "TooLong"],
    "Email": ["Valid", "Invalid", "Empty"],
    "Password": ["Strong", "Weak", "Empty"],
    "Terms": ["Accepted", "NotAccepted"]
}

constraints = [
    'IF [Terms] = "NotAccepted" THEN [Name] = "Valid"',  # 即使条款未接受也要测试验证
]
```

### API端点测试

```python
parameters = {
    "HTTPMethod": ["GET", "POST", "PUT", "DELETE"],
    "Authentication": ["Valid", "Invalid", "Missing"],
    "ContentType": ["JSON", "XML", "FormData"],
    "PayloadSize": ["Empty", "Small", "Large"]
}

constraints = [
    'IF [HTTPMethod] = "GET" THEN [PayloadSize] = "Empty"',
    'IF [Authentication] = "Missing" THEN [HTTPMethod] IN {GET, POST}'
]
```

### 配置测试

```python
parameters = {
    "Environment": ["Dev", "Staging", "Production"],
    "CacheEnabled": ["True", "False"],
    "LogLevel": ["Debug", "Info", "Error"],
    "Database": ["SQLite", "PostgreSQL", "MySQL"]
}

constraints = [
    'IF [Environment] = "Production" THEN [LogLevel] <> "Debug"',
    'IF [Database] = "SQLite" THEN [Environment] = "Dev"'
]
```

## 故障排除

### 没有生成测试用例

- 检查约束是否过度限制
- 验证约束语法（必须以`;`结尾）
- 确保约束中的参数名称与定义匹配（使用`[参数名]`）

### 测试用例过多

- 验证使用order 2（成对）而非更高阶
- 考虑拆分为子模型
- 检查参数是否可以分离为独立的测试套件

### 输出中有无效组合

- 添加缺失的约束
- 验证约束逻辑正确
- 检查是否需要使用`NOT`或`<>`运算符

### 脚本错误

- 确保已安装pypict：`pip install pypict --break-system-packages`
- 检查Python版本（3.7+）
- 验证模型语法有效

## 参考资料

- **references/pict_syntax.md** - 完整PICT语法参考，包含语法和运算符
- **references/examples.md** - 各领域综合真实示例
- **scripts/pict_helper.py** - 用于模型生成和输出格式化的Python工具
- [PICT GitHub仓库](https://github.com/microsoft/pict) - 官方PICT文档
- [pypict文档](https://github.com/kmaehashi/pypict) - Python绑定文档
- [在线PICT工具](https://pairwise.yuuniworks.com/) - 基于Web的PICT生成器

## 示例

### 示例1：简单函数测试

**用户请求：**"为接受两个数字并返回结果的除法函数设计测试。"

**分析：**
- 参数：被除数（数字）、除数（数字）
- 值：使用等价划分和边界
  - 数字：负数、零、正数、大值
- 约束：除以零无效
- 预期输出：结果或错误

**PICT模型：**
```
Dividend: -10, 0, 10, 1000
Divisor: ~0, -5, 1, 5, 100

IF [Divisor] = "0" THEN [Dividend] = "10";
```

**测试用例：**

| 测试 # | Dividend | Divisor | 预期输出 |
| --- | --- | --- | --- |
| 1 | 10 | 0 | 错误: 除以零 |
| 2 | -10 | 1 | -10.0 |
| 3 | 0 | -5 | 0.0 |
| 4 | 1000 | 5 | 200.0 |
| 5 | 10 | 100 | 0.1 |

### 示例2：电商结账

**用户请求：**"为结账流程设计测试，包括支付方式、 shipping选项和用户类型。"

**分析：**
- 支付：信用卡、PayPal、银行转账（受用户类型限制）
- Shipping：标准、加急、当日
- 用户：访客、注册用户、VIP
- 约束：访客不能使用银行转账，VIP用户免费加急

**PICT模型：**
```
PaymentMethod: CreditCard, PayPal, BankTransfer
ShippingMethod: Standard, Express, Overnight
UserType: Guest, Registered, Premium

IF [UserType] = "Guest" THEN [PaymentMethod] <> "BankTransfer";
IF [UserType] = "Premium" AND [ShippingMethod] = "Express" THEN [PaymentMethod] IN {CreditCard, PayPal};
```

**输出：** 12-15个测试用例，覆盖所有有效的支付/shipping/用户组合及预期成本和结果。
