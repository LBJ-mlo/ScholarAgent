"""
ReAct Agent控制器模块

该模块实现了ScholarAgent的核心逻辑，基于LangChain的ReAct Agent框架。
支持多轮对话、工具调用、任务规划等功能。
"""

import logging
import os
from typing import List, Dict, Any, Optional
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import BaseMessage, HumanMessage, AIMessage
from langchain.memory import ConversationBufferMemory

from ..config import config
from .tools import scholar_tools
from .prompts import REACT_SYSTEM_PROMPT

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ScholarAgent:
    """ScholarAgent主控制器类"""
    
    def __init__(self, model_name: str = "deepseek-chat", temperature: float = 0.3):
        """
        初始化ScholarAgent
        
        Args:
            model_name: 使用的LLM模型名称
            temperature: 生成温度参数
        """
        self.model_name = model_name
        self.temperature = temperature
        
        # 初始化LLM
        llm_config = config.get_llm_config("deepseek")
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            base_url=llm_config["base_url"],
            api_key=llm_config["api_key"]
        )
        
        # 获取工具
        self.tools = scholar_tools.get_available_tools()
        
        # 初始化记忆
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # 存储搜索到的论文信息
        self.paper_cache: Dict[str, Dict[str, Any]] = {}
        
        # 创建ReAct Agent
        self.agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self._create_agent_prompt()
        )
        
        # 创建Agent执行器
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=10
        )
        
        # 对话历史
        self.conversation_history: List[Dict[str, Any]] = []
    
    def _create_agent_prompt(self):
        """创建Agent提示词"""
        from langchain.prompts import PromptTemplate
        
        template = f"""{REACT_SYSTEM_PROMPT}

{{chat_history}}

问题: {{input}}
思考: {{agent_scratchpad}}"""

        return PromptTemplate(
            input_variables=["tools", "tool_names", "chat_history", "input", "agent_scratchpad"],
            template=template
        )
    
    def run(self, user_input: str) -> Dict[str, Any]:
        """
        运行Agent处理用户输入
        
        Args:
            user_input: 用户输入的问题或指令
            
        Returns:
            Dict[str, Any]: 包含回答和元信息的字典
        """
        try:
            logger.info(f"处理用户输入: {user_input}")
            
            # 记录用户输入
            self.conversation_history.append({
                "role": "user",
                "content": user_input,
                "timestamp": self._get_timestamp()
            })
            
            # 增强用户输入，添加上下文信息
            enhanced_input = self._enhance_input_with_context(user_input)
            
            # 执行Agent
            result = self.agent_executor.invoke({
                "input": enhanced_input
            })
            
            # 提取回答
            answer = result.get("output", "抱歉，我无法处理您的请求。")
            
            # 缓存论文信息（如果搜索结果包含论文信息）
            self._cache_paper_info(result)
            
            # 自动补全论文arXiv ID和PDF链接
            if any(x in user_input for x in ["论文", "这篇论文", "该论文"]):
                if self.paper_cache:
                    last_paper = list(self.paper_cache.values())[-1]
                    arxiv_id = last_paper.get('arxiv_id', '')
                    pdf_url = last_paper.get('pdf_url', '')
                    if arxiv_id or pdf_url:
                        answer += f"\n\narXiv ID: {arxiv_id}\nPDF链接: {pdf_url}"
            
            # 记录Agent回答
            self.conversation_history.append({
                "role": "assistant",
                "content": answer,
                "timestamp": self._get_timestamp()
            })
            
            return {
                "answer": answer,
                "success": True,
                "conversation_history": self.conversation_history,
                "tools_used": self._extract_tools_used(result)
            }
            
        except Exception as e:
            logger.error(f"Agent执行时发生错误: {e}")
            error_message = f"处理您的请求时遇到错误: {str(e)}"
            
            # 记录错误
            self.conversation_history.append({
                "role": "assistant",
                "content": error_message,
                "timestamp": self._get_timestamp(),
                "error": True
            })
            
            return {
                "answer": error_message,
                "success": False,
                "conversation_history": self.conversation_history,
                "error": str(e)
            }
    
    def search_paper(self, query: str) -> Dict[str, Any]:
        """
        搜索论文的便捷方法
        
        Args:
            query: 搜索查询
            
        Returns:
            Dict[str, Any]: 搜索结果
        """
        return self.run(f"请搜索论文：{query}")
    
    def summarize_paper(self, paper_title: str) -> Dict[str, Any]:
        """
        总结论文的便捷方法
        
        Args:
            paper_title: 论文标题
            
        Returns:
            Dict[str, Any]: 总结结果
        """
        return self.run(f"请总结论文'{paper_title}'的研究贡献")
    
    def answer_question(self, question: str, paper_title: str = "") -> Dict[str, Any]:
        """
        回答问题的便捷方法
        
        Args:
            question: 用户问题
            paper_title: 论文标题（可选）
            
        Returns:
            Dict[str, Any]: 回答结果
        """
        if paper_title:
            return self.run(f"关于论文'{paper_title}'，请回答：{question}")
        else:
            return self.run(f"请回答：{question}")
    
    def compare_papers(self, paper1: str, paper2: str) -> Dict[str, Any]:
        """
        比较论文的便捷方法
        
        Args:
            paper1: 第一篇论文标题
            paper2: 第二篇论文标题
            
        Returns:
            Dict[str, Any]: 比较结果
        """
        return self.run(f"请比较论文'{paper1}'和'{paper2}'的异同点")
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """
        获取对话历史
        
        Returns:
            List[Dict[str, Any]]: 对话历史列表
        """
        return self.conversation_history
    
    def clear_conversation_history(self):
        """清空对话历史"""
        self.conversation_history = []
        self.memory.clear()
    
    def _extract_tools_used(self, result: Dict[str, Any]) -> List[str]:
        """
        从结果中提取使用的工具
        
        Args:
            result: Agent执行结果
            
        Returns:
            List[str]: 使用的工具列表
        """
        tools_used = []
        if "intermediate_steps" in result:
            for step in result["intermediate_steps"]:
                if len(step) >= 2:
                    tool_name = step[0].tool if hasattr(step[0], 'tool') else str(step[0])
                    tools_used.append(tool_name)
        return tools_used
    
    def _get_timestamp(self) -> str:
        """获取当前时间戳"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def _enhance_input_with_context(self, user_input: str) -> str:
        """
        增强用户输入，添加上下文信息
        
        Args:
            user_input: 原始用户输入
            
        Returns:
            str: 增强后的输入
        """
        # 如果缓存中有论文信息，添加到上下文中
        if self.paper_cache:
            context_info = "\n\n当前会话中已搜索的论文信息：\n"
            for paper_id, paper_info in self.paper_cache.items():
                context_info += f"- {paper_info.get('title', '未知标题')} (作者: {paper_info.get('authors', '未知作者')})\n"
            
            enhanced_input = f"{user_input}\n{context_info}"
            return enhanced_input
        
        return user_input
    
    def _cache_paper_info(self, result: Dict[str, Any]):
        """
        缓存搜索结果中的论文信息
        
        Args:
            result: Agent执行结果
        """
        try:
            # 检查是否有中间步骤包含搜索结果
            if "intermediate_steps" in result:
                for step in result["intermediate_steps"]:
                    if len(step) >= 2:
                        tool_name = step[0].tool if hasattr(step[0], 'tool') else str(step[0])
                        tool_output = step[1]
                        
                        # 如果是Arxiv搜索工具的输出，解析并缓存论文信息
                        if "search_arxiv" in tool_name and tool_output:
                            self._parse_and_cache_papers(tool_output)
        except Exception as e:
            logger.warning(f"缓存论文信息时出错: {e}")
    
    def _parse_and_cache_papers(self, search_output: str):
        """
        解析搜索结果并缓存论文信息
        
        Args:
            search_output: 搜索输出文本
        """
        try:
            # 简单的解析逻辑，提取论文标题和作者
            lines = search_output.split('\n')
            current_paper = {}
            
            for line in lines:
                line = line.strip()
                if line.startswith('标题:'):
                    if current_paper:
                        # 保存前一篇论文
                        paper_id = current_paper.get('title', 'unknown')
                        self.paper_cache[paper_id] = current_paper.copy()
                    # 开始新论文
                    current_paper = {'title': line.replace('标题:', '').strip()}
                elif line.startswith('作者:') and current_paper:
                    current_paper['authors'] = line.replace('作者:', '').strip()
                elif line.startswith('Arxiv ID:') and current_paper:
                    arxiv_id = line.replace('Arxiv ID:', '').strip()
                    current_paper['arxiv_id'] = arxiv_id
                    current_paper['pdf_url'] = f"http://arxiv.org/pdf/{arxiv_id}"
                elif line.startswith('摘要:') and current_paper:
                    current_paper['abstract'] = line.replace('摘要:', '').strip()
            # 保存最后一篇论文
            if current_paper:
                paper_id = current_paper.get('title', 'unknown')
                self.paper_cache[paper_id] = current_paper.copy()
        except Exception as e:
            logger.warning(f"解析论文信息时出错: {e}")
    
    def get_cached_papers(self) -> Dict[str, Dict[str, Any]]:
        """
        获取缓存的论文信息
        
        Returns:
            Dict[str, Dict[str, Any]]: 缓存的论文信息
        """
        return self.paper_cache.copy()
    
    def clear_paper_cache(self):
        """清空论文缓存"""
        self.paper_cache.clear()
    
    def get_agent_info(self) -> Dict[str, Any]:
        """
        获取Agent信息
        
        Returns:
            Dict[str, Any]: Agent信息
        """
        return {
            "model_name": self.model_name,
            "temperature": self.temperature,
            "available_tools": [tool.name for tool in self.tools],
            "conversation_count": len(self.conversation_history)
        }

# 创建全局Agent实例
def create_scholar_agent(model_name: str = "deepseek-chat", temperature: float = 0.3) -> ScholarAgent:
    """
    创建ScholarAgent实例
    
    Args:
        model_name: 使用的LLM模型名称
        temperature: 生成温度参数
        
    Returns:
        ScholarAgent: Agent实例
    """
    return ScholarAgent(model_name=model_name, temperature=temperature)

# 便捷函数
def run_agent(user_input: str, model_name: str = "deepseek-chat") -> str:
    """
    便捷函数：运行Agent并返回回答
    
    Args:
        user_input: 用户输入
        model_name: 使用的模型名称
        
    Returns:
        str: Agent回答
    """
    agent = create_scholar_agent(model_name)
    result = agent.run(user_input)
    return result["answer"] 