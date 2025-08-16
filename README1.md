# LLM幻觉检测系统

## 项目简介

这是一个专门用于检测LLM生成知识中幻觉的系统。该模块基于DeepSeek API，通过简化的评估标准来快速判断生成内容是否基于原始案例，是否存在根本性错误。

## 核心判断标准

**如果生成文本是基于领域知识和原始文本的合理推断，就是好的生成文本。**

- 基于原始案例的合理推理不应被视为幻觉
- 只有与原始案例存在明显冲突的信息才应该扣分
- 符合领域常识的推断是高质量的推理

## 项目结构

```
huanjue/
├── prompts.py                    # 所有Prompt模板
├── hallucination_detector.py     # 主要检测逻辑
├── main.py                       # 调用入口
├── entity_extractor.py           # API调用模块
├── config.py                     # 配置文件
├── requirements.txt              # 依赖文件
└── README.md                     # 项目说明
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 1. 直接运行示例

```bash
py main.py
```

### 2. 检测自定义文本

```python
from main import detect_custom_text

# 检测自定义文本
result = detect_custom_text(
    original_text="你的原始案例文本",
    generated_knowledge="生成的知识文本",
    save_filename="custom_result.json"  # 可选
)
```

### 3. 在代码中使用

```python
from hallucination_detector import HallucinationDetector

# 初始化检测器
detector = HallucinationDetector()

# 执行检测
result = detector.detect_hallucination(original_text, generated_knowledge)

# 打印结果
detector.print_result(result)

# 保存结果
detector.save_result(result, "my_result.json")
```

## 检测维度说明

### 1. 事实一致性检测
- **检测目标**: 生成内容是否与原始案例的事实一致
- **核心判断**: 基于原始案例的合理推断应该给予高分
- **评估标准**: 
  - 0.8-1.0: 完全一致，无冲突，或基于原始案例的合理推断
  - 0.6-0.7: 基本一致，存在合理推断
  - 0.4-0.5: 部分一致，存在推断
  - 0.0-0.3: 存在事实冲突

### 2. 推理质量检测
- **检测目标**: 推理是否基于原始信息和领域知识
- **核心判断**: 基于领域知识和原始文本的合理推断是高质量的推理
- **评估标准**:
  - 0.8-1.0: 推理完全基于原始信息和领域知识
  - 0.6-0.7: 推理基本合理，基于原始信息进行推断
  - 0.4-0.5: 推理部分合理，存在推断
  - 0.0-0.3: 推理缺乏支持，过度推断

### 3. 根本性错误检测
- **检测目标**: 是否存在技术性、逻辑性根本错误
- **核心判断**: 基于领域知识的合理推断不构成根本性错误
- **评估标准**:
  - 0.8-1.0: 无根本性错误，或基于领域知识的合理推断
  - 0.0-0.3: 存在根本性错误

## 判断逻辑

系统采用**基于三个维度分数的直接判断**，要求所有维度都达到相应阈值：

### 高质量知识 (≥0.8)
- 要求：三个维度分数都 ≥ 0.8
- 状态：`no_hallucination`
- 建议：高质量知识，三个维度均表现优秀

### 良好质量 (≥0.7)
- 要求：三个维度分数都 ≥ 0.7
- 状态：`likely_no_hallucination`
- 建议：质量良好，三个维度均表现良好

### 潜在问题 (≥0.6)
- 要求：三个维度分数都 ≥ 0.6
- 状态：`potential_hallucination`
- 建议：存在潜在问题，需要人工复核

### 质量不确定 (≥0.5)
- 要求：三个维度分数都 ≥ 0.5
- 状态：`uncertain_hallucination`
- 建议：质量不确定，建议重新生成

### 可能存在幻觉 (<0.5)
- 要求：任一维度分数 < 0.5
- 状态：`likely_hallucination`
- 建议：可能存在幻觉，建议重新生成

## 输出结果

检测结果包含以下信息：

```json
{
  "overall_score": 0.85,
  "category": "high_confidence",
  "hallucination_status": "no_hallucination",
  "recommendation": "高质量知识，三个维度均表现优秀",
  "detailed_scores": {
    "factual_consistency": 0.9,
    "reasoning_quality": 0.8,
    "fundamental_errors": 0.9
  },
  "detailed_analysis": {
    "factual_consistency": "详细分析...",
    "reasoning_quality": "详细分析...",
    "fundamental_errors": "详细分析..."
  },
  "weights_used": {
    "factual_consistency": 0.3,
    "reasoning_quality": 0.3,
    "fundamental_errors": 0.4
  },
  "judgment_criteria": {
    "method": "direct_dimension_judgment",
    "description": "基于三个维度分数的直接判断，要求所有维度都达到相应阈值"
  }
}
```

## 幻觉状态分类

- **no_hallucination**: 无幻觉，三个维度均表现优秀
- **likely_no_hallucination**: 可能无幻觉，三个维度均表现良好
- **potential_hallucination**: 潜在幻觉，需要人工复核
- **uncertain_hallucination**: 质量不确定，建议重新生成
- **likely_hallucination**: 可能存在幻觉，建议重新生成

## 配置说明

在 `config.py` 中配置DeepSeek API：

```python
DEEPSEEK_API_KEY = "your_api_key_here"
DEEPSEEK_API_BASE = "https://api.deepseek.com/v1"
DEEPSEEK_MODEL = "deepseek-chat"
```

## 适用场景

- 需要严格判断生成内容是否基于原始案例
- 要求所有维度都达到高质量标准
- 不允许单一维度表现优秀而其他维度表现差的情况
- 对检测结果有明确的质量要求

## 注意事项

1. 确保DeepSeek API密钥配置正确
2. 网络连接稳定，避免API调用超时
3. 检测结果仅供参考，重要决策需要人工复核
4. 新的判断逻辑更加严格，要求所有维度都达到相应标准
5. 加权分数仅作为参考，实际判断基于三个维度的直接比较

## 技术栈

- Python 3.7+
- DeepSeek API
- requests
- numpy
