"""
ScholarAgent Streamlit界面

该模块提供了ScholarAgent的Web界面，基于Streamlit构建。
支持论文搜索、总结、问答等功能的可视化交互。
"""

import streamlit as st
import os
import sys
from typing import List, Dict, Any
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.controller import create_scholar_agent

# 页面配置
st.set_page_config(
    page_title="ScholarAgent - 科研论文分析助手",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .assistant-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    .error-message {
        background-color: #ffebee;
        border-left: 4px solid #f44336;
    }
    .tool-info {
        background-color: #e8f5e8;
        border-left: 4px solid #4caf50;
        padding: 0.5rem;
        border-radius: 0.3rem;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """初始化会话状态"""
    if "agent" not in st.session_state:
        st.session_state.agent = None
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []
    if "current_paper_info" not in st.session_state:
        st.session_state.current_paper_info = None

def check_environment():
    """检查环境配置"""
    # DeepSeek API Key已经硬编码在代码中，不需要环境变量
    st.success("✅ 环境配置检查通过 (使用DeepSeek API)")
    return True

def create_agent():
    """创建Agent实例"""
    if st.session_state.agent is None:
        with st.spinner("正在初始化ScholarAgent..."):
            st.session_state.agent = create_scholar_agent()
        st.success("✅ ScholarAgent初始化完成！")

def display_header():
    """显示页面头部"""
    st.markdown('<h1 class="main-header">🤖 ScholarAgent</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">专业的科研论文分析助手 | 基于LangChain + ReAct Agent</p>', unsafe_allow_html=True)

def display_sidebar():
    """显示侧边栏"""
    with st.sidebar:
        st.header("🔧 控制面板")
        
        # Agent信息
        if st.session_state.agent:
            agent_info = st.session_state.agent.get_agent_info()
            st.subheader("Agent信息")
            st.write(f"模型: {agent_info['model_name']}")
            st.write(f"对话次数: {agent_info['conversation_count']}")
            st.write(f"可用工具: {', '.join(agent_info['available_tools'])}")
        
        # 快速操作
        st.subheader("⚡ 快速操作")
        
        if st.button("🔄 重新初始化Agent"):
            st.session_state.agent = None
            st.session_state.conversation_history = []
            st.session_state.current_paper_info = None
            st.rerun()
        
        if st.button("🗑️ 清空对话历史"):
            if st.session_state.agent:
                st.session_state.agent.clear_conversation_history()
            st.session_state.conversation_history = []
            st.rerun()
        
        # 示例问题
        st.subheader("💡 示例问题")
        example_questions = [
            "请搜索论文 Segment Anything",
            "请总结论文 Attention Is All You Need 的研究贡献",
            "这篇论文的主要技术方法是什么？",
            "请生成这篇论文的关键信息点",
            "比较论文A和论文B的异同点"
        ]
        
        for question in example_questions:
            if st.button(question, key=f"example_{question}"):
                st.session_state.user_input = question
                st.rerun()

def display_conversation_history():
    """显示对话历史"""
    if st.session_state.conversation_history:
        st.subheader("💬 对话历史")
        
        for i, message in enumerate(st.session_state.conversation_history):
            if message["role"] == "user":
                st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>👤 用户 ({message.get('timestamp', '')}):</strong><br>
                    {message['content']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message assistant-message">
                    <strong>🤖 ScholarAgent ({message.get('timestamp', '')}):</strong><br>
                    {message['content']}
                </div>
                """, unsafe_allow_html=True)
                
                # 显示使用的工具
                if message.get("tools_used"):
                    tools_text = ", ".join(message["tools_used"])
                    st.markdown(f"""
                    <div class="tool-info">
                        🔧 使用的工具: {tools_text}
                    </div>
                    """, unsafe_allow_html=True)

def handle_user_input():
    """处理用户输入"""
    st.subheader("🔍 与ScholarAgent对话")
    
    # 用户输入
    user_input = st.text_area(
        "请输入您的问题或指令:",
        value=st.session_state.get("user_input", ""),
        height=100,
        placeholder="例如：请搜索论文 Segment Anything"
    )
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        if st.button("🚀 发送", type="primary"):
            if user_input.strip():
                process_user_input(user_input.strip())
    
    with col2:
        if st.button("📝 示例问题"):
            st.session_state.user_input = "请搜索论文 Segment Anything"
            st.rerun()

def process_user_input(user_input: str):
    """处理用户输入"""
    if not st.session_state.agent:
        st.error("Agent未初始化，请检查环境配置")
        return
    
    # 显示处理状态
    with st.spinner("🤔 ScholarAgent正在思考..."):
        try:
            # 执行Agent
            result = st.session_state.agent.run(user_input)
            
            # 更新对话历史
            if result["success"]:
                # 记录用户输入
                st.session_state.conversation_history.append({
                    "role": "user",
                    "content": user_input,
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                })
                
                # 记录Agent回答
                st.session_state.conversation_history.append({
                    "role": "assistant",
                    "content": result["answer"],
                    "timestamp": datetime.now().strftime("%H:%M:%S"),
                    "tools_used": result.get("tools_used", [])
                })
                
                # 清空输入
                st.session_state.user_input = ""
                
                # 重新运行页面
                st.rerun()
            else:
                st.error(f"❌ 处理失败: {result['answer']}")
                
        except Exception as e:
            st.error(f"❌ 发生错误: {str(e)}")

def display_features():
    """显示功能特性"""
    st.subheader("✨ 功能特性")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **🔍 论文搜索**
        - 按标题搜索
        - 按作者搜索
        - 按关键词搜索
        - 支持Arxiv API
        """)
    
    with col2:
        st.markdown("""
        **📝 智能总结**
        - 研究贡献总结
        - 技术方法分析
        - 创新点提取
        - 关键信息生成
        """)
    
    with col3:
        st.markdown("""
        **💬 智能问答**
        - 基于论文内容回答
        - 多轮对话支持
        - 上下文理解
        - 论文比较分析
        """)

def main():
    """主函数"""
    # 初始化
    initialize_session_state()
    
    # 检查环境
    if not check_environment():
        st.stop()
    
    # 显示头部
    display_header()
    
    # 创建Agent
    create_agent()
    
    # 显示侧边栏
    display_sidebar()
    
    # 主界面
    tab1, tab2, tab3 = st.tabs(["💬 对话", "📊 功能", "ℹ️ 关于"])
    
    with tab1:
        # 显示对话历史
        display_conversation_history()
        
        # 处理用户输入
        handle_user_input()
    
    with tab2:
        display_features()
        
        st.subheader("🛠️ 技术架构")
        st.markdown("""
        - **框架**: LangChain + ReAct Agent
        - **LLM**: OpenAI GPT-4
        - **工具**: Arxiv API, 自定义总结工具
        - **界面**: Streamlit
        - **语言**: Python
        """)
    
    with tab3:
        st.subheader("📖 关于ScholarAgent")
        st.markdown("""
        ScholarAgent是一个基于大语言模型的科研论文分析助手，采用ReAct推理策略，
        能够自主规划任务执行流程，调用各种工具完成论文检索、总结和问答任务。
        
        **主要特点:**
        - 🤖 基于LangChain的ReAct Agent架构
        - 🔍 集成Arxiv API进行论文检索
        - 📝 智能总结和分析论文内容
        - 💬 支持多轮对话和上下文理解
        - 🛠️ 模块化设计，易于扩展
        
        **适用场景:**
        - 科研人员快速了解论文内容
        - 学生进行文献调研
        - 研究人员比较分析不同论文
        - 学术写作辅助
        """)

if __name__ == "__main__":
    main() 