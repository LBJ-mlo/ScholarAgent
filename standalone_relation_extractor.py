#!/usr/bin/env python3
"""
独立的关系抽取和描述生成脚本
可以直接运行，无需依赖其他文件
支持OpenAI和DeepSeek API
"""

import asyncio
import json
import os
from typing import Dict, Any, List
import openai

class StandaloneRelationExtractor:
    """独立的关系抽取器"""
    
    def __init__(self, api_key: str = "", api_type: str = "deepseek"):
        """
        初始化抽取器
        api_key: API密钥
        api_type: API类型 ("openai" 或 "deepseek")
        """
        self.api_type = api_type
        
        if api_type == "deepseek":
            # DeepSeek API配置
            self.client = openai.AsyncOpenAI(
                api_key=api_key,
                base_url="https://api.deepseek.com/v1"
            )
            self.model = "deepseek-chat"
        else:
            # OpenAI API配置
            self.client = openai.AsyncOpenAI(api_key=api_key)
            self.model = "gpt-3.5-turbo"
    
    async def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """抽取实体"""
        prompt = f"""
请从以下文本中抽取关键实体，按以下类型分类：

实体类型：
- 网络元素：网络设备、服务、实例等
- 告警：告警名称、级别、时间等
- 人员：工程师、团队等
- 工具：平台、系统、工具等
- 业务：业务功能、服务等
- 原因：故障原因、问题等
- 动作：处理动作、操作等
- 状态：运行状态、结果等

文本内容：
{text}

请以JSON格式返回，格式如下：
{{
    "网络元素": ["实体1", "实体2"],
    "告警": ["实体1", "实体2"],
    "人员": ["实体1", "实体2"],
    "工具": ["实体1", "实体2"],
    "业务": ["实体1", "实体2"],
    "原因": ["实体1", "实体2"],
    "动作": ["实体1", "实体2"],
    "状态": ["实体1", "实体2"]
}}
"""
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000,
                temperature=0.7
            )
            
            result = response.choices[0].message.content.strip()
            print(f"🔍 API返回的原始内容: {result[:200]}...")
            
            # 清理Markdown代码块标记
            if result.startswith("```json"):
                result = result[7:]  # 移除 ```json
            if result.startswith("```"):
                result = result[3:]   # 移除 ```
            if result.endswith("```"):
                result = result[:-3]  # 移除结尾的 ```
            
            result = result.strip()
            print(f"🔧 清理后的内容: {result[:200]}...")
            
            try:
                entities = json.loads(result)
                return entities
            except json.JSONDecodeError as e:
                print(f"❌ JSON解析失败: {e}")
                print(f"📝 完整返回内容: {result}")
                return {}
                
        except Exception as e:
            print(f"实体抽取失败: {e}")
            return {}
    
    async def extract_relations(self, text: str, entities: Dict[str, List[str]]) -> List[Dict[str, str]]:
        """抽取关系"""
        all_entities = []
        for entity_list in entities.values():
            all_entities.extend(entity_list)
        
        prompt = f"""
请从以下文本中识别实体间的关系。

文本内容：
{text}

实体列表：
{all_entities}

关系类型：
- TRIGGERS: 触发关系
- CAUSES: 因果关系
- DETECTS: 检测关系
- PERFORMS: 执行关系
- USES: 使用关系
- AFFECTS: 影响关系
- RECOVERS: 恢复关系
- MONITORS: 监控关系

请以JSON格式返回关系列表，格式如下：
[
    {{
        "source": "源实体",
        "target": "目标实体",
        "relation_type": "关系类型"
    }}
]
"""
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000,
                temperature=0.7
            )
            
            result = response.choices[0].message.content.strip()
            print(f"🔍 关系抽取API返回的原始内容: {result[:200]}...")
            
            # 清理Markdown代码块标记
            if result.startswith("```json"):
                result = result[7:]  # 移除 ```json
            if result.startswith("```"):
                result = result[3:]   # 移除 ```
            if result.endswith("```"):
                result = result[:-3]  # 移除结尾的 ```
            
            result = result.strip()
            print(f"🔧 关系抽取清理后的内容: {result[:200]}...")
            
            try:
                relations = json.loads(result)
                return relations if isinstance(relations, list) else []
            except json.JSONDecodeError as e:
                print(f"❌ 关系抽取JSON解析失败: {e}")
                print(f"📝 完整返回内容: {result}")
                return []
                
        except Exception as e:
            print(f"关系抽取失败: {e}")
            return []
    
    async def generate_relation_descriptions(
        self, 
        relations: List[Dict[str, str]], 
        context: str = ""
    ) -> List[Dict[str, Any]]:
        """生成关系描述"""
        descriptions = []
        
        for relation in relations:
            source = relation.get("source", "")
            target = relation.get("target", "")
            relation_type = relation.get("relation_type", "")
            
            if not all([source, target, relation_type]):
                continue
            
            # 生成详细描述
            detailed_desc = await self._generate_detailed_description(
                source, target, relation_type, context
            )
            
            # 生成表达变体
            variations = await self._generate_description_variations(
                source, target, relation_type, context
            )
            
            descriptions.append({
                "source": source,
                "target": target,
                "relation_type": relation_type,
                "detailed_description": detailed_desc,
                "variations": variations,
                "all_descriptions": [detailed_desc] + variations
            })
        
        return descriptions
    
    async def _generate_detailed_description(
        self, 
        source: str, 
        target: str, 
        relation_type: str, 
        context: str
    ) -> str:
        """使用LLM生成详细的关系描述"""
        prompt = f"""
请为以下实体关系生成一个详细、完整的自然语言描述句子。

源实体：{source}
目标实体：{target}
关系类型：{relation_type}
上下文：{context}

要求：
1. 生成一个完整的句子
2. 包含技术细节和具体描述
3. 语言自然流畅
4. 体现实体间的具体关系

请直接返回描述句子，不要包含其他内容。
"""
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"生成详细描述失败: {e}")
            return f"{source}与{target}之间存在{relation_type}关系"
    
    async def _generate_description_variations(
        self, 
        source: str, 
        target: str, 
        relation_type: str, 
        context: str
    ) -> List[str]:
        """生成多种表达方式"""
        prompt = f"""
请为以下实体关系生成3-5种不同的自然语言表达方式。

源实体：{source}
目标实体：{target}
关系类型：{relation_type}
上下文：{context}

要求：
1. 每种表达都是完整的句子
2. 表达方式要多样化
3. 包含不同的句式结构
4. 语言自然流畅

请以JSON数组格式返回，例如：
["描述1", "描述2", "描述3"]
"""
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
                temperature=0.8
            )
            
            result = response.choices[0].message.content.strip()
            try:
                variations = json.loads(result)
                return variations if isinstance(variations, list) else []
            except json.JSONDecodeError:
                return []
                
        except Exception as e:
            print(f"生成表达变体失败: {e}")
            return []
    
    def format_descriptions_for_output(
        self, 
        descriptions: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """格式化输出结果"""
        all_sentences = []
        
        for desc in descriptions:
            all_sentences.append(desc['detailed_description'])
            all_sentences.extend(desc.get('variations', []))
        
        # 去重
        unique_sentences = list(set(all_sentences))
        
        return {
            "summary": {
                "total_relations": len(descriptions),
                "total_sentences": len(unique_sentences),
                "relation_types": list(set(d['relation_type'] for d in descriptions))
            },
            "sentences": unique_sentences,
            "detailed_relations": descriptions
        }
    
    async def extract_and_describe_relations(self, text: str) -> Dict[str, Any]:
        """抽取实体关系并生成描述"""
        try:
            print("开始抽取实体...")
            entities = await self.extract_entities(text)
            
            print("开始抽取关系...")
            relations = await self.extract_relations(text, entities)
            
            print("开始生成关系描述...")
            descriptions = await self.generate_relation_descriptions(relations, text)
            
            print("格式化输出结果...")
            result = self.format_descriptions_for_output(descriptions)
            
            return {
                "success": True,
                "original_text": text[:200] + "..." if len(text) > 200 else text,
                "entities": entities,
                "relations": relations,
                "relation_descriptions": result,
                "metadata": {
                    "total_entities": sum(len(v) for v in entities.values()),
                    "total_relations": len(relations),
                    "descriptions_generated": len(result.get("sentences", []))
                }
            }
            
        except Exception as e:
            print(f"处理失败: {e}")
            return {
                "success": False,
                "error": str(e)
            }

async def main():
    """主函数"""
    print("🔧 开始初始化...")
    
    # 使用DeepSeek API密钥
    api_key = "sk-5783900819b04bee9bc177f7db24edac"
    
    if not api_key:
        print("请设置API密钥")
        return
    
    print(f"✅ API密钥已设置: {api_key[:10]}...")
    
    # 创建抽取器（使用DeepSeek API）
    print("🔧 创建抽取器...")
    extractor = StandaloneRelationExtractor(api_key, api_type="deepseek")
    print(f"✅ 抽取器创建成功，使用模型: {extractor.model}")
    
    # 示例文本
    example_text = """
    UDM服务不可用告警触发了运维工程师的响应。运维工程师使用华为5G云管理平台检测到UDM实例异常。
    数据库连接中断导致了UDM服务失败。运维工程师重启了UDM实例，恢复了服务正常运行。
    监控系统持续监控网络状态，确保服务稳定性。
    """
    print(f"📝 示例文本长度: {len(example_text)} 字符")
    
    print("开始处理示例文本...")
    print(f"使用API类型: {extractor.api_type}")
    print(f"使用模型: {extractor.model}")
    
    result = await extractor.extract_and_describe_relations(example_text)
    
    if result["success"]:
        print("处理成功！")
        print(f"抽取到 {result['metadata']['total_entities']} 个实体")
        print(f"识别到 {result['metadata']['total_relations']} 个关系")
        print(f"生成了 {result['metadata']['descriptions_generated']} 个描述句子")
        
        # 保存结果
        with open("relation_extraction_result.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print("结果已保存到 relation_extraction_result.json")
        
        # 显示部分结果
        print("\n=== 生成的描述句子 ===")
        sentences = result["relation_descriptions"]["sentences"]
        for i, sentence in enumerate(sentences[:5], 1):
            print(f"{i}. {sentence}")
        
        if len(sentences) > 5:
            print(f"... 还有 {len(sentences) - 5} 个描述")
    
    else:
        print(f"处理失败: {result['error']}")

if __name__ == "__main__":
    asyncio.run(main())
