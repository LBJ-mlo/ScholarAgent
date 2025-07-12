"""
LangChain工具模块

该模块定义了ScholarAgent可以使用的各种工具，
包括论文搜索、总结、问答等功能。
"""

import logging
from typing import List, Dict, Any, Optional
from langchain.tools import Tool
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

from ..config import config

from services.search import arxiv_service, PaperInfo
from services.summarize import summarize_service

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ScholarTools:
    """ScholarAgent工具集合类"""
    
    def __init__(self, model_name: str = "deepseek-chat"):
        """
        初始化工具集合
        
        Args:
            model_name: 使用的LLM模型名称
        """
        self.model_name = model_name
        llm_config = config.get_llm_config("deepseek")
        self.llm = ChatOpenAI(
            model=model_name, 
            temperature=0.3,
            base_url=llm_config["base_url"],
            api_key=llm_config["api_key"]
        )
    
    def search_arxiv_tool(self, query: str) -> str:
        """
        Arxiv论文搜索工具
        
        Args:
            query: 搜索查询，格式为 "类型:关键词"
            
        Returns:
            str: 搜索结果
        """
        try:
            # 解析查询格式
            if ":" in query:
                search_type, keywords = query.split(":", 1)
                search_type = search_type.strip().lower()
                keywords = keywords.strip()
            else:
                # 默认按关键词搜索
                search_type = "keywords"
                keywords = query.strip()
            
            # 根据搜索类型调用相应方法
            if search_type == "title":
                results = arxiv_service.search_by_title(keywords)
            elif search_type == "author":
                results = arxiv_service.search_by_author(keywords)
            else:
                results = arxiv_service.search_by_keywords(keywords)
            
            if not results:
                return f"未找到与'{keywords}'相关的论文。"
            
            # 格式化结果
            formatted_results = []
            for i, paper in enumerate(results, 1):
                formatted_results.append(f"论文{i}:\n{arxiv_service.format_paper_info(paper)}")
            
            return "\n\n".join(formatted_results)
            
        except Exception as e:
            logger.error(f"搜索论文时发生错误: {e}")
            return f"搜索失败: {str(e)}"
    
    def summarize_contributions_tool(self, paper_info: str) -> str:
        """
        总结论文研究贡献工具
        
        Args:
            paper_info: 论文信息（包含标题和摘要）
            
        Returns:
            str: 研究贡献总结
        """
        try:
            # 从论文信息中提取标题和摘要
            lines = paper_info.split('\n')
            title = ""
            abstract = ""
            
            for line in lines:
                if line.startswith("标题:"):
                    title = line.replace("标题:", "").strip()
                elif line.startswith("摘要:"):
                    abstract = line.replace("摘要:", "").strip()
            
            if not abstract:
                return "无法从提供的论文信息中提取摘要。"
            
            return summarize_service.summarize_research_contributions(abstract, title)
            
        except Exception as e:
            logger.error(f"总结研究贡献时发生错误: {e}")
            return f"总结失败: {str(e)}"
    
    def summarize_methods_tool(self, paper_info: str) -> str:
        """
        总结论文技术方法工具
        
        Args:
            paper_info: 论文信息（包含标题和摘要）
            
        Returns:
            str: 技术方法总结
        """
        try:
            # 从论文信息中提取标题和摘要
            lines = paper_info.split('\n')
            title = ""
            abstract = ""
            
            for line in lines:
                if line.startswith("标题:"):
                    title = line.replace("标题:", "").strip()
                elif line.startswith("摘要:"):
                    abstract = line.replace("摘要:", "").strip()
            
            if not abstract:
                return "无法从提供的论文信息中提取摘要。"
            
            return summarize_service.summarize_technical_methods(abstract, title)
            
        except Exception as e:
            logger.error(f"总结技术方法时发生错误: {e}")
            return f"总结失败: {str(e)}"
    
    def answer_question_tool(self, question: str, paper_info: str) -> str:
        """
        基于论文信息回答问题工具
        
        Args:
            question: 用户问题
            paper_info: 论文信息
            
        Returns:
            str: 问题回答
        """
        try:
            # 从论文信息中提取标题和摘要
            lines = paper_info.split('\n')
            title = ""
            abstract = ""
            
            for line in lines:
                if line.startswith("标题:"):
                    title = line.replace("标题:", "").strip()
                elif line.startswith("摘要:"):
                    abstract = line.replace("摘要:", "").strip()
            
            if not abstract:
                return "无法从提供的论文信息中提取摘要。"
            
            return summarize_service.answer_research_question(question, abstract, title)
            
        except Exception as e:
            logger.error(f"回答问题时发生错误: {e}")
            return f"回答失败: {str(e)}"
    
    def generate_key_points_tool(self, paper_info: str) -> str:
        """
        生成论文关键点工具
        
        Args:
            paper_info: 论文信息
            
        Returns:
            str: 关键点列表
        """
        try:
            # 从论文信息中提取标题和摘要
            lines = paper_info.split('\n')
            title = ""
            abstract = ""
            
            for line in lines:
                if line.startswith("标题:"):
                    title = line.replace("标题:", "").strip()
                elif line.startswith("摘要:"):
                    abstract = line.replace("摘要:", "").strip()
            
            if not abstract:
                return "无法从提供的论文信息中提取摘要。"
            
            key_points = summarize_service.generate_key_points(abstract, title)
            return "\n".join([f"• {point}" for point in key_points])
            
        except Exception as e:
            logger.error(f"生成关键点时发生错误: {e}")
            return f"生成失败: {str(e)}"
    
    def compare_papers_tool(self, paper1_info: str, paper2_info: str) -> str:
        """
        比较两篇论文工具
        
        Args:
            paper1_info: 第一篇论文信息
            paper2_info: 第二篇论文信息
            
        Returns:
            str: 比较分析结果
        """
        try:
            # 从论文信息中提取摘要
            def extract_abstract(paper_info: str) -> tuple:
                lines = paper_info.split('\n')
                title = ""
                abstract = ""
                
                for line in lines:
                    if line.startswith("标题:"):
                        title = line.replace("标题:", "").strip()
                    elif line.startswith("摘要:"):
                        abstract = line.replace("摘要:", "").strip()
                
                return title, abstract
            
            title1, abstract1 = extract_abstract(paper1_info)
            title2, abstract2 = extract_abstract(paper2_info)
            
            if not abstract1 or not abstract2:
                return "无法从提供的论文信息中提取摘要。"
            
            return summarize_service.compare_papers(abstract1, abstract2, title1, title2)
            
        except Exception as e:
            logger.error(f"比较论文时发生错误: {e}")
            return f"比较失败: {str(e)}"
    
    def get_available_tools(self) -> List[Tool]:
        """
        获取所有可用工具
        
        Returns:
            List[Tool]: 工具列表
        """
        tools = [
            Tool(
                name="search_arxiv",
                func=self.search_arxiv_tool,
                description="搜索Arxiv论文。输入格式：'类型:关键词'，其中类型可以是title（按标题）、author（按作者）、keywords（按关键词）。例如：'title:Segment Anything'"
            ),
            Tool(
                name="summarize_contributions",
                func=self.summarize_contributions_tool,
                description="总结论文的研究贡献。输入：包含标题和摘要的论文信息"
            ),
            Tool(
                name="summarize_methods",
                func=self.summarize_methods_tool,
                description="总结论文的技术方法。输入：包含标题和摘要的论文信息"
            ),
            Tool(
                name="answer_question",
                func=self.answer_question_tool,
                description="基于论文信息回答用户问题。输入：'问题|论文信息'，用|分隔问题和论文信息"
            ),
            Tool(
                name="generate_key_points",
                func=self.generate_key_points_tool,
                description="生成论文的关键信息点。输入：包含标题和摘要的论文信息"
            ),
            Tool(
                name="compare_papers",
                func=self.compare_papers_tool,
                description="比较两篇论文的异同点。输入：'论文1信息|论文2信息'，用|分隔两篇论文信息"
            )
        ]
        
        return tools

# 创建全局工具实例
scholar_tools = ScholarTools() 