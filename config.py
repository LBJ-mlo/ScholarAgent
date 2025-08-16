# -*- coding: utf-8 -*-
"""
配置文件
"""

# DeepSeek API配置
DEEPSEEK_API_KEY = "sk-d005b01ce325422eb59daa1cd5355144"
DEEPSEEK_API_BASE = "https://api.deepseek.com/v1"
DEEPSEEK_MODEL = "deepseek-chat"

# 幻觉检测配置
DETECTION_THRESHOLDS = {
    'high_confidence': 0.8,
    'medium_confidence': 0.6,
    'low_confidence': 0.4
}

# 检测维度权重
DETECTION_WEIGHTS = {
    'accuracy': 0.35,
    'consistency': 0.35,
    'reasoning': 0.25,
    'completeness': 0.05
}

# 提示词模板
PROMPT_TEMPLATES = {
    'entity_extraction': """
请从以下文本中提取关键实体，包括系统、服务、工具、时间、问题等：

文本：{text}

请以JSON格式输出：
{{
    "systems": ["系统1", "系统2"],
    "services": ["服务1", "服务2"],
    "tools": ["工具1", "工具2"],
    "time_periods": ["时间段1", "时间段2"],
    "problems": ["问题1", "问题2"],
    "actions": ["动作1", "动作2"]
}}
""",
    
    'knowledge_generation': """
基于以下原始案例描述和实体组合，生成详细的知识描述：

原始案例：{original_text}

实体组合：{entity_combination}

请生成描述这些实体之间关系的知识，要求：
1. 基于原始案例的合理推理
2. 描述准确且符合技术逻辑
3. 允许合理的因果推断
4. 避免添加原始案例中不存在的信息
""",
    
    'factual_consistency': """
请检查以下生成的知识是否与原始案例描述一致：

原始案例：{original_text}

生成知识：{generated_knowledge}

请分析：
1. 生成知识中的事实是否与原始案例一致？
2. 是否存在与原始案例冲突的信息？
3. 推理是否基于原始案例的合理推断？

请给出0-1的评分和详细分析。
""",
    
    'reasoning_quality': """
请评估以下推理的合理性：

原始案例：{original_text}

生成知识：{generated_knowledge}

请分析：
1. 推理是否有原始信息支持？
2. 因果链是否逻辑合理？
3. 是否符合技术领域的常识？
4. 是否存在过度推断？

请给出0-1的评分和详细分析。
""",
    
    'information_support': """
请评估以下生成知识的信息支持度：

原始案例：{original_text}

生成知识：{generated_knowledge}

请分析：
1. 生成知识中的每个断言是否有原始信息支持？
2. 推理距离是否合理？
3. 是否存在缺乏支持的信息？

请给出0-1的评分和详细分析。
"""
}

# 输出配置
OUTPUT_CONFIG = {
    'save_results': True,
    'output_format': 'json',
    'log_level': 'INFO'
}
