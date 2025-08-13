# 独立关系抽取脚本使用说明

## 概述

`standalone_relation_extractor.py` 是一个独立的Python脚本，可以直接运行进行实体关系抽取和自然语言描述生成，无需依赖其他项目文件。

## 功能特性

1. **实体抽取**: 从文本中识别关键实体（网络元素、告警、人员、工具等）
2. **关系抽取**: 识别实体间的语义关系（触发、导致、检测、执行等）
3. **描述生成**: 将关系转换为完整的自然语言描述句子
4. **表达变体**: 生成多种不同的表达方式

## 安装依赖

```bash
pip install openai asyncio
```

## 使用方法

### 1. 设置API密钥

```bash
export DEEPSEEK_API_KEY="your_deepseek_api_key_here"
```

或者直接使用内置的API密钥（已配置好您的DeepSeek API）

### 2. 直接运行

```bash
python standalone_relation_extractor.py
```

### 3. 自定义文本

修改脚本中的 `example_text` 变量，替换为您自己的文本内容。

## 输出结果

脚本会生成以下文件：
- `relation_extraction_result.json`: 完整的抽取结果

结果包含：
- 抽取的实体列表
- 识别的关系
- 生成的描述句子
- 统计信息

## 示例输出

```
开始处理示例文本...
开始抽取实体...
开始抽取关系...
开始生成关系描述...
格式化输出结果...
处理成功！
抽取到 8 个实体
识别到 5 个关系
生成了 15 个描述句子
结果已保存到 relation_extraction_result.json

=== 生成的描述句子 ===
1. UDM服务不可用告警触发了运维工程师的响应行动
2. 运维工程师使用华为5G云管理平台检测到UDM实例异常状态
3. 数据库连接中断导致了UDM服务失败
4. 运维工程师重启了UDM实例，恢复了服务正常运行
5. 监控系统持续监控网络状态，确保服务稳定性
... 还有 10 个描述
```

## 核心方法

### `extract_entities(text)`
- 输入：文本字符串
- 输出：按类型分类的实体字典

### `extract_relations(text, entities)`
- 输入：文本和实体字典
- 输出：关系列表

### `generate_relation_descriptions(relations, context)`
- 输入：关系列表和上下文
- 输出：详细的关系描述

## 关系类型

- **TRIGGERS**: 触发关系
- **CAUSES**: 因果关系  
- **DETECTS**: 检测关系
- **PERFORMS**: 执行关系
- **USES**: 使用关系
- **AFFECTS**: 影响关系
- **RECOVERS**: 恢复关系
- **MONITORS**: 监控关系

## 注意事项

1. 需要有效的DeepSeek API密钥（已内置您的API密钥）
2. 网络连接正常
3. 文本长度建议不超过2000字符
4. 处理时间取决于文本复杂度和API响应速度

## 自定义配置

可以修改脚本中的以下参数：
- `model`: 使用的LLM模型（默认：gpt-3.5-turbo）
- `max_tokens`: 最大输出token数
- `temperature`: 生成随机性（0-1）

## 错误处理

脚本包含完整的错误处理机制：
- API调用失败自动重试
- JSON解析失败返回空结果
- 详细的错误信息输出

## 快速开始

如果您想直接运行演示，可以使用：

```bash
python run_demo.py
```

这个脚本已经配置好您的DeepSeek API密钥，可以直接运行。
