#!/usr/bin/env python3
"""
批量关系抽取脚本
处理包含多个text字段的JSON数据

使用方法:
1. 基本使用: py -u batch_relation_extractor.py
2. 指定数据文件: py -u batch_relation_extractor.py my_data.json
3. 指定保存间隔: py -u batch_relation_extractor.py my_data.json 10
4. 从中间结果恢复: py -u batch_relation_extractor.py my_data.json batch_results_partial_15_of_50.json

功能特点:
- 每处理N个文本自动保存中间结果
- 支持从中间结果恢复处理
- 实时显示处理进度
- 生成详细的处理报告
"""

import asyncio
import json
import os
import sys
from typing import Dict, Any, List
from standalone_relation_extractor import StandaloneRelationExtractor

class BatchRelationExtractor:
    """批量关系抽取器"""
    
    def __init__(self, api_key: str, api_type: str = "deepseek"):
        """初始化批量抽取器"""
        self.extractor = StandaloneRelationExtractor(api_key, api_type)
        self.results = []
    
    async def process_single_text(self, text: str, index: int) -> Dict[str, Any]:
        """处理单个文本"""
        print(f"\n📝 处理第 {index + 1} 个文本...")
        print(f"文本长度: {len(text)} 字符")
        print(f"文本预览: {text[:100]}...")
        
        try:
            result = await self.extractor.extract_and_describe_relations(text)
            result["text_index"] = index
            result["text_preview"] = text[:200] + "..." if len(text) > 200 else text
            
            if result["success"]:
                print(f"✅ 第 {index + 1} 个文本处理成功")
                print(f"   实体数量: {result['metadata']['total_entities']}")
                print(f"   关系数量: {result['metadata']['total_relations']}")
                print(f"   描述数量: {result['metadata']['descriptions_generated']}")
            else:
                print(f"❌ 第 {index + 1} 个文本处理失败: {result['error']}")
            
            return result
            
        except Exception as e:
            print(f"❌ 第 {index + 1} 个文本处理异常: {e}")
            return {
                "success": False,
                "error": str(e),
                "text_index": index,
                "text_preview": text[:200] + "..." if len(text) > 200 else text
            }
    
    async def process_batch(self, data: List[Dict[str, str]], save_interval: int = 5) -> Dict[str, Any]:
        """批量处理数据"""
        print(f"🚀 开始批量处理 {len(data)} 个文本...")
        print(f"💾 每处理 {save_interval} 个文本保存一次结果")
        
        results = []
        success_count = 0
        total_entities = 0
        total_relations = 0
        total_descriptions = 0
        
        for i, item in enumerate(data):
            if "text" not in item:
                print(f"⚠️ 第 {i + 1} 个数据项缺少 'text' 字段，跳过")
                continue
            
            text = item["text"]
            if not text or not text.strip():
                print(f"⚠️ 第 {i + 1} 个文本为空，跳过")
                continue
            
            result = await self.process_single_text(text, i)
            results.append(result)
            
            if result["success"]:
                success_count += 1
                total_entities += result['metadata']['total_entities']
                total_relations += result['metadata']['total_relations']
                total_descriptions += result['metadata']['descriptions_generated']
            
            # 每处理指定数量的文本就保存一次
            if (i + 1) % save_interval == 0:
                print(f"\n💾 已处理 {i + 1} 个文本，保存中间结果...")
                temp_summary = {
                    "total_texts": len(data),
                    "processed_texts": len(results),
                    "success_count": success_count,
                    "failure_count": len(results) - success_count,
                    "total_entities": total_entities,
                    "total_relations": total_relations,
                    "total_descriptions": total_descriptions,
                    "success_rate": success_count / len(results) if results else 0,
                    "progress": f"{i + 1}/{len(data)}"
                }
                
                temp_result = {
                    "summary": temp_summary,
                    "results": results,
                    "is_partial": True
                }
                
                # 保存中间结果
                temp_filename = f"batch_results_partial_{i + 1}_of_{len(data)}.json"
                self.save_results(temp_result, temp_filename)
                print(f"✅ 中间结果已保存到 {temp_filename}")
        
        # 生成最终汇总报告
        summary = {
            "total_texts": len(data),
            "processed_texts": len(results),
            "success_count": success_count,
            "failure_count": len(results) - success_count,
            "total_entities": total_entities,
            "total_relations": total_relations,
            "total_descriptions": total_descriptions,
            "success_rate": success_count / len(results) if results else 0,
            "progress": f"{len(data)}/{len(data)}"
        }
        
        return {
            "summary": summary,
            "results": results,
            "is_partial": False
        }
    
    def save_results(self, batch_result: Dict[str, Any], output_file: str = "batch_relation_results.json"):
        """保存结果到文件"""
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(batch_result, f, ensure_ascii=False, indent=2)
            print(f"✅ 结果已保存到 {output_file}")
        except Exception as e:
            print(f"❌ 保存结果失败: {e}")

    def load_partial_results(self, partial_file: str) -> tuple:
        """加载部分结果，用于恢复处理"""
        try:
            with open(partial_file, "r", encoding="utf-8") as f:
                partial_data = json.load(f)
            
            if partial_data.get("is_partial", False):
                results = partial_data.get("results", [])
                processed_count = len(results)
                print(f"✅ 从 {partial_file} 加载了 {processed_count} 个已处理的结果")
                return results, processed_count
            else:
                print("❌ 该文件不是部分结果文件")
                return [], 0
                
        except Exception as e:
            print(f"❌ 加载部分结果失败: {e}")
            return [], 0

    async def resume_processing(self, data: List[Dict[str, str]], partial_file: str, save_interval: int = 5) -> Dict[str, Any]:
        """从部分结果恢复处理"""
        print(f"🔄 从部分结果恢复处理...")
        
        # 加载已处理的结果
        existing_results, processed_count = self.load_partial_results(partial_file)
        
        if processed_count == 0:
            print("❌ 无法恢复，从头开始处理")
            return await self.process_batch(data, save_interval)
        
        print(f"📊 已处理: {processed_count}/{len(data)} 个文本")
        
        # 继续处理剩余文本
        results = existing_results.copy()
        success_count = sum(1 for r in results if r.get("success", False))
        total_entities = sum(r.get('metadata', {}).get('total_entities', 0) for r in results if r.get("success", False))
        total_relations = sum(r.get('metadata', {}).get('total_relations', 0) for r in results if r.get("success", False))
        total_descriptions = sum(r.get('metadata', {}).get('descriptions_generated', 0) for r in results if r.get("success", False))
        
        for i in range(processed_count, len(data)):
            item = data[i]
            if "text" not in item:
                print(f"⚠️ 第 {i + 1} 个数据项缺少 'text' 字段，跳过")
                continue
            
            text = item["text"]
            if not text or not text.strip():
                print(f"⚠️ 第 {i + 1} 个文本为空，跳过")
                continue
            
            result = await self.process_single_text(text, i)
            results.append(result)
            
            if result["success"]:
                success_count += 1
                total_entities += result['metadata']['total_entities']
                total_relations += result['metadata']['total_relations']
                total_descriptions += result['metadata']['descriptions_generated']
            
            # 每处理指定数量的文本就保存一次
            if (i + 1) % save_interval == 0:
                print(f"\n💾 已处理 {i + 1} 个文本，保存中间结果...")
                temp_summary = {
                    "total_texts": len(data),
                    "processed_texts": len(results),
                    "success_count": success_count,
                    "failure_count": len(results) - success_count,
                    "total_entities": total_entities,
                    "total_relations": total_relations,
                    "total_descriptions": total_descriptions,
                    "success_rate": success_count / len(results) if results else 0,
                    "progress": f"{i + 1}/{len(data)}"
                }
                
                temp_result = {
                    "summary": temp_summary,
                    "results": results,
                    "is_partial": True
                }
                
                # 保存中间结果
                temp_filename = f"batch_results_partial_{i + 1}_of_{len(data)}.json"
                self.save_results(temp_result, temp_filename)
                print(f"✅ 中间结果已保存到 {temp_filename}")
        
        # 生成最终汇总报告
        summary = {
            "total_texts": len(data),
            "processed_texts": len(results),
            "success_count": success_count,
            "failure_count": len(results) - success_count,
            "total_entities": total_entities,
            "total_relations": total_relations,
            "total_descriptions": total_descriptions,
            "success_rate": success_count / len(results) if results else 0,
            "progress": f"{len(data)}/{len(data)}"
        }
        
        return {
            "summary": summary,
            "results": results,
            "is_partial": False
        }

async def load_data_from_file(file_path: str) -> List[Dict[str, str]]:
    """从文件加载数据"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        if isinstance(data, list):
            return data
        elif isinstance(data, dict) and "text" in data:
            return [data]
        else:
            print("❌ 数据格式不正确，应为包含text字段的对象列表")
            return []
            
    except FileNotFoundError:
        print(f"❌ 文件 {file_path} 不存在")
        return []
    except json.JSONDecodeError as e:
        print(f"❌ JSON解析失败: {e}")
        return []
    except Exception as e:
        print(f"❌ 加载数据失败: {e}")
        return []

async def main():
    """主函数"""
    print("🔧 批量关系抽取脚本启动...")
    
    # 检查命令行参数
    input_file = "input_data.json"  # 默认文件名
    save_interval = 5  # 默认每5个文本保存一次
    resume_file = None  # 恢复文件
    
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if len(sys.argv) > 2:
        try:
            save_interval = int(sys.argv[2])
        except ValueError:
            # 如果第二个参数不是数字，可能是恢复文件
            resume_file = sys.argv[2]
            save_interval = 5
    if len(sys.argv) > 3 and resume_file is None:
        try:
            save_interval = int(sys.argv[3])
        except ValueError:
            print("⚠️ 保存间隔参数必须是数字，使用默认值5")
    
    print(f"📁 输入文件: {input_file}")
    print(f"💾 保存间隔: 每 {save_interval} 个文本保存一次")
    if resume_file:
        print(f"🔄 恢复文件: {resume_file}")
    
    # 检查输入文件
    if not os.path.exists(input_file):
        print(f"❌ 输入文件 {input_file} 不存在")
        print("💡 请创建包含以下格式的JSON文件：")
        print("""
[
    {"text": "案例描述1"},
    {"text": "案例描述2"},
    {"text": "案例描述3"}
]
        """)
        return
    
    # 加载数据
    print(f"📂 从文件 {input_file} 加载数据...")
    data = await load_data_from_file(input_file)
    
    if not data:
        print("❌ 没有有效数据，程序退出")
        return
    
    print(f"✅ 成功加载 {len(data)} 个数据项")
    
    # 设置API密钥
    api_key = os.getenv("DEEPSEEK_API_KEY", "sk-5783900819b04bee9bc177f7db24edac")
    if not api_key:
        print("❌ 请设置DEEPSEEK_API_KEY环境变量")
        return
    
    print(f"✅ API密钥已设置: {api_key[:10]}...")
    
    # 创建批量处理器
    batch_processor = BatchRelationExtractor(api_key, api_type="deepseek")
    
    # 批量处理
    if resume_file and os.path.exists(resume_file):
        print(f"🔄 从 {resume_file} 恢复处理...")
        batch_result = await batch_processor.resume_processing(data, resume_file, save_interval)
    else:
        print("🚀 开始新的批量处理...")
        batch_result = await batch_processor.process_batch(data, save_interval)
    
    # 显示汇总结果
    summary = batch_result["summary"]
    print(f"\n=== 批量处理汇总 ===")
    print(f"总文本数: {summary['total_texts']}")
    print(f"处理文本数: {summary['processed_texts']}")
    print(f"成功数: {summary['success_count']}")
    print(f"失败数: {summary['failure_count']}")
    print(f"成功率: {summary['success_rate']:.2%}")
    print(f"总实体数: {summary['total_entities']}")
    print(f"总关系数: {summary['total_relations']}")
    print(f"总描述数: {summary['total_descriptions']}")
    
    # 保存结果
    output_file = f"batch_results_{len(data)}_texts.json"
    batch_processor.save_results(batch_result, output_file)
    
    # 显示部分成功结果
    successful_results = [r for r in batch_result["results"] if r["success"]]
    if successful_results:
        print(f"\n=== 成功处理的文本示例 ===")
        for i, result in enumerate(successful_results[:3], 1):
            print(f"{i}. 文本 {result['text_index'] + 1}:")
            print(f"   实体: {result['metadata']['total_entities']} 个")
            print(f"   关系: {result['metadata']['total_relations']} 个")
            print(f"   描述: {result['metadata']['descriptions_generated']} 个")
            print()

if __name__ == "__main__":
    asyncio.run(main())
