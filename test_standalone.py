#!/usr/bin/env python3
"""
测试独立关系抽取脚本
"""

import asyncio
import os
import sys

print("🚀 脚本开始执行...")
print(f"Python版本: {sys.version}")
print(f"当前工作目录: {os.getcwd()}")

try:
    from standalone_relation_extractor import StandaloneRelationExtractor
    print("✅ 成功导入 StandaloneRelationExtractor")
except ImportError as e:
    print(f"❌ 导入失败: {e}")
    sys.exit(1)

async def test_basic_functionality():
    """测试基本功能"""
    print("=== 测试独立关系抽取脚本 ===")
    
    # 检查API密钥
    api_key = os.getenv("DEEPSEEK_API_KEY", "sk-5783900819b04bee9bc177f7db24edac")
    if not api_key:
        print("❌ 错误：请设置DEEPSEEK_API_KEY环境变量")
        return False
    
    # 创建抽取器
    extractor = StandaloneRelationExtractor(api_key, api_type="deepseek")
    
    # 测试文本
    test_text = "UDM服务不可用告警触发了运维工程师的响应。运维工程师使用华为5G云管理平台检测到UDM实例异常。"
    
    print("📝 测试文本：")
    print(test_text)
    print()
    
    try:
        # 测试实体抽取
        print("🔍 测试实体抽取...")
        entities = await extractor.extract_entities(test_text)
        print(f"✅ 抽取到 {sum(len(v) for v in entities.values())} 个实体")
        for entity_type, entity_list in entities.items():
            if entity_list:
                print(f"   {entity_type}: {entity_list}")
        print()
        
        # 测试关系抽取
        print("🔗 测试关系抽取...")
        relations = await extractor.extract_relations(test_text, entities)
        print(f"✅ 识别到 {len(relations)} 个关系")
        for relation in relations:
            print(f"   {relation['source']} --{relation['relation_type']}--> {relation['target']}")
        print()
        
        # 测试描述生成
        print("📝 测试描述生成...")
        descriptions = await extractor.generate_relation_descriptions(relations, test_text)
        print(f"✅ 生成了 {len(descriptions)} 个关系描述")
        for desc in descriptions:
            print(f"   {desc['detailed_description']}")
        print()
        
        # 测试完整流程
        print("🚀 测试完整流程...")
        result = await extractor.extract_and_describe_relations(test_text)
        
        if result["success"]:
            print("✅ 完整流程测试成功！")
            print(f"   实体数量: {result['metadata']['total_entities']}")
            print(f"   关系数量: {result['metadata']['total_relations']}")
            print(f"   描述数量: {result['metadata']['descriptions_generated']}")
            return True
        else:
            print(f"❌ 完整流程测试失败: {result['error']}")
            return False
            
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")
        return False

async def test_custom_text():
    """测试自定义文本"""
    print("\n=== 测试自定义文本 ===")
    
    api_key = os.getenv("DEEPSEEK_API_KEY", "sk-5783900819b04bee9bc177f7db24edac")
    if not api_key:
        print("❌ 错误：请设置DEEPSEEK_API_KEY环境变量")
        return False
    
    extractor = StandaloneRelationExtractor(api_key, api_type="deepseek")
    
    # 自定义测试文本
    custom_text = """
    5G核心网元AMF告警系统检测到服务异常。运维工程师小王立即登录华为5G云管理平台进行故障排查。
    通过日志分析发现AMF实例内存使用率过高，导致服务响应缓慢。小王重启了AMF实例，服务恢复正常。
    监控系统持续观察网络性能指标，确保系统稳定运行。
    """
    
    print("📝 自定义文本：")
    print(custom_text.strip())
    print()
    
    try:
        result = await extractor.extract_and_describe_relations(custom_text)
        
        if result["success"]:
            print("✅ 自定义文本测试成功！")
            print(f"   实体数量: {result['metadata']['total_entities']}")
            print(f"   关系数量: {result['metadata']['total_relations']}")
            print(f"   描述数量: {result['metadata']['descriptions_generated']}")
            
            # 显示部分描述
            sentences = result["relation_descriptions"]["sentences"]
            print("\n📋 生成的描述句子（前3个）：")
            for i, sentence in enumerate(sentences[:3], 1):
                print(f"   {i}. {sentence}")
            
            return True
        else:
            print(f"❌ 自定义文本测试失败: {result['error']}")
            return False
            
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")
        return False

async def main():
    """主测试函数"""
    print("🧪 开始测试独立关系抽取脚本...")
    print()
    
    # 测试基本功能
    basic_success = await test_basic_functionality()
    
    # 测试自定义文本
    custom_success = await test_custom_text()
    
    # 总结
    print("\n=== 测试总结 ===")
    if basic_success and custom_success:
        print("🎉 所有测试通过！脚本可以正常使用。")
        print("\n💡 使用建议：")
        print("   1. 设置OPENAI_API_KEY环境变量")
        print("   2. 运行 python standalone_relation_extractor.py")
        print("   3. 修改脚本中的example_text进行自定义测试")
    else:
        print("❌ 部分测试失败，请检查配置和网络连接。")
    
    print("\n📚 更多信息请查看 README_standalone.md")

if __name__ == "__main__":
    asyncio.run(main())
