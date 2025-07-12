"""
ScholarAgent主程序入口

该模块提供了ScholarAgent的命令行界面和基本功能。
支持直接运行Agent进行论文检索、总结和问答。
"""

import os
import sys
import logging
from typing import Optional
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent.controller import create_scholar_agent, run_agent

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_environment():
    """检查环境配置"""
    # DeepSeek API Key已经硬编码在代码中，不需要环境变量
    print("✅ 环境配置检查通过 (使用DeepSeek API)")
    return True

def interactive_mode():
    """交互模式"""
    print("🤖 欢迎使用ScholarAgent！")
    print("📚 我是一个专业的科研论文分析助手")
    print("💡 您可以：")
    print("   - 搜索论文：'搜索论文 Segment Anything'")
    print("   - 总结论文：'总结论文 Segment Anything'")
    print("   - 回答问题：'论文的主要创新点是什么？'")
    print("   - 比较论文：'比较论文A和论文B'")
    print("   - 输入 'quit' 或 'exit' 退出")
    print("-" * 50)
    
    agent = create_scholar_agent()
    
    while True:
        try:
            user_input = input("\n🔍 请输入您的问题: ").strip()
            
            if user_input.lower() in ['quit', 'exit', '退出']:
                print("👋 感谢使用ScholarAgent，再见！")
                break
            
            if not user_input:
                continue
            
            print("\n🤔 正在处理您的问题...")
            result = agent.run(user_input)
            
            if result["success"]:
                print(f"\n✅ 回答：\n{result['answer']}")
                
                if result.get("tools_used"):
                    print(f"\n🔧 使用的工具：{', '.join(result['tools_used'])}")
            else:
                print(f"\n❌ 错误：{result['answer']}")
                
        except KeyboardInterrupt:
            print("\n\n👋 感谢使用ScholarAgent，再见！")
            break
        except Exception as e:
            logger.error(f"交互模式发生错误: {e}")
            print(f"\n❌ 发生错误: {str(e)}")

def demo_mode():
    """演示模式"""
    print("🎬 ScholarAgent演示模式")
    print("=" * 50)
    
    # 演示问题列表
    demo_questions = [
        "请搜索论文 Segment Anything",
        "请总结论文 Segment Anything 的研究贡献",
        "这篇论文的主要技术方法是什么？",
        "请生成这篇论文的关键信息点"
    ]
    
    agent = create_scholar_agent()
    
    for i, question in enumerate(demo_questions, 1):
        print(f"\n📝 演示 {i}: {question}")
        print("-" * 30)
        
        try:
            result = agent.run(question)
            
            if result["success"]:
                print(f"✅ 回答：\n{result['answer']}")
                
                if result.get("tools_used"):
                    print(f"🔧 使用的工具：{', '.join(result['tools_used'])}")
            else:
                print(f"❌ 错误：{result['answer']}")
                
        except Exception as e:
            logger.error(f"演示模式发生错误: {e}")
            print(f"❌ 发生错误: {str(e)}")
        
        print("\n" + "=" * 50)

def quick_search(paper_title: str):
    """快速搜索论文"""
    print(f"🔍 搜索论文: {paper_title}")
    result = run_agent(f"请搜索论文 {paper_title}")
    print(f"✅ 结果：\n{result}")

def quick_summarize(paper_title: str):
    """快速总结论文"""
    print(f"📝 总结论文: {paper_title}")
    result = run_agent(f"请总结论文 {paper_title} 的研究贡献")
    print(f"✅ 结果：\n{result}")

def main():
    """主函数"""
    print("🚀 ScholarAgent启动中...")
    
    # 检查环境配置
    if not check_environment():
        return
    
    # 解析命令行参数
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "demo":
            demo_mode()
        elif command == "search" and len(sys.argv) > 2:
            quick_search(sys.argv[2])
        elif command == "summarize" and len(sys.argv) > 2:
            quick_summarize(sys.argv[2])
        elif command == "help":
            print_help()
        else:
            print("❌ 无效的命令")
            print_help()
    else:
        # 默认进入交互模式
        interactive_mode()

def print_help():
    """打印帮助信息"""
    help_text = """
ScholarAgent 使用说明：

1. 交互模式（默认）：
   python app.py

2. 演示模式：
   python app.py demo

3. 快速搜索论文：
   python app.py search "论文标题"

4. 快速总结论文：
   python app.py summarize "论文标题"

5. 显示帮助：
   python app.py help

环境配置：
- 在.env文件中设置 OPENAI_API_KEY=your_api_key
- 或者直接在环境中设置 OPENAI_API_KEY

示例：
   python app.py search "Segment Anything"
   python app.py summarize "Attention Is All You Need"
"""
    print(help_text)

if __name__ == "__main__":
    main() 