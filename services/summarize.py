"""
LLM总结服务模块

该模块使用大语言模型对论文摘要进行智能总结和分析。
支持多种总结模式：研究贡献总结、技术方法总结、创新点分析等。
"""

import logging
from typing import List, Dict, Optional
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

from ..config import config

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SummarizeService:
    """LLM总结服务类"""
    
    def __init__(self, model_name: str = "deepseek-chat", temperature: float = 0.3):
        """
        初始化总结服务
        
        Args:
            model_name: 使用的LLM模型名称
            temperature: 生成温度参数
        """
        self.model_name = model_name
        self.temperature = temperature
        llm_config = config.get_llm_config("deepseek")
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            base_url=llm_config["base_url"],
            api_key=llm_config["api_key"]
        )
    
    def summarize_research_contributions(self, abstract: str, title: str = "") -> str:
        """
        总结论文的研究贡献
        
        Args:
            abstract: 论文摘要
            title: 论文标题（可选）
            
        Returns:
            str: 研究贡献总结
        """
        system_prompt = """你是一个专业的科研论文分析专家。请分析给定的论文摘要，总结该论文的主要研究贡献。

请从以下角度进行分析：
1. 研究问题：该论文要解决什么问题？
2. 主要贡献：论文提出了什么新的方法、技术或见解？
3. 创新点：相比现有工作，该论文的创新之处在哪里？
4. 技术方法：论文采用了什么技术方法？
5. 实验结果：论文的主要实验结果或结论是什么？

请用中文回答，结构清晰，重点突出。"""
        
        user_prompt = f"""
论文标题: {title}
论文摘要: {abstract}

请总结该论文的研究贡献。
"""
        
        try:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            
            response = self.llm.invoke(messages)
            return response.content
            
        except Exception as e:
            logger.error(f"总结研究贡献时发生错误: {e}")
            return f"总结失败: {str(e)}"
    
    def summarize_technical_methods(self, abstract: str, title: str = "") -> str:
        """
        总结论文的技术方法
        
        Args:
            abstract: 论文摘要
            title: 论文标题（可选）
            
        Returns:
            str: 技术方法总结
        """
        system_prompt = """你是一个机器学习和技术专家。请分析给定的论文摘要，总结该论文的技术方法。

请从以下角度进行分析：
1. 技术框架：论文使用了什么技术框架或架构？
2. 算法方法：论文提出了什么算法或方法？
3. 实现细节：论文的技术实现有什么特点？
4. 技术优势：该技术方法相比传统方法有什么优势？
5. 应用场景：该技术方法适用于什么场景？

请用中文回答，技术细节要准确，结构清晰。"""
        
        user_prompt = f"""
论文标题: {title}
论文摘要: {abstract}

请总结该论文的技术方法。
"""
        
        try:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            
            response = self.llm.invoke(messages)
            return response.content
            
        except Exception as e:
            logger.error(f"总结技术方法时发生错误: {e}")
            return f"总结失败: {str(e)}"
    
    def answer_research_question(self, question: str, abstract: str, title: str = "") -> str:
        """
        基于论文摘要回答研究问题
        
        Args:
            question: 用户提出的问题
            abstract: 论文摘要
            title: 论文标题（可选）
            
        Returns:
            str: 问题回答
        """
        system_prompt = """你是一个专业的科研论文问答专家。请基于给定的论文摘要，回答用户提出的问题。

回答要求：
1. 基于论文摘要中的信息进行回答
2. 如果摘要中没有相关信息，请明确说明
3. 回答要准确、客观、专业
4. 用中文回答，语言清晰易懂

请确保回答基于论文内容，不要添加论文中没有的信息。"""
        
        user_prompt = f"""
论文标题: {title}
论文摘要: {abstract}

用户问题: {question}

请基于论文摘要回答上述问题。
"""
        
        try:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            
            response = self.llm.invoke(messages)
            return response.content
            
        except Exception as e:
            logger.error(f"回答问题时发生错误: {e}")
            return f"回答失败: {str(e)}"
    
    def compare_papers(self, abstract1: str, abstract2: str, title1: str = "", title2: str = "") -> str:
        """
        比较两篇论文
        
        Args:
            abstract1: 第一篇论文摘要
            abstract2: 第二篇论文摘要
            title1: 第一篇论文标题（可选）
            title2: 第二篇论文标题（可选）
            
        Returns:
            str: 论文比较分析
        """
        system_prompt = """你是一个专业的论文比较分析专家。请比较分析两篇论文的异同点。

请从以下角度进行比较：
1. 研究问题：两篇论文要解决的问题是否相同？
2. 技术方法：两篇论文采用的技术方法有什么不同？
3. 创新点：两篇论文的创新之处各是什么？
4. 优缺点：两篇论文各自的优缺点是什么？
5. 应用场景：两篇论文的应用场景有什么不同？

请用中文回答，客观公正，结构清晰。"""
        
        user_prompt = f"""
论文A标题: {title1}
论文A摘要: {abstract1}

论文B标题: {title2}
论文B摘要: {abstract2}

请比较分析这两篇论文的异同点。
"""
        
        try:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            
            response = self.llm.invoke(messages)
            return response.content
            
        except Exception as e:
            logger.error(f"比较论文时发生错误: {e}")
            return f"比较失败: {str(e)}"
    
    def generate_key_points(self, abstract: str, title: str = "") -> List[str]:
        """
        生成论文关键点列表
        
        Args:
            abstract: 论文摘要
            title: 论文标题（可选）
            
        Returns:
            List[str]: 关键点列表
        """
        system_prompt = """你是一个论文分析专家。请从给定的论文摘要中提取关键信息点。

请提取以下类型的关键点：
1. 研究问题
2. 主要方法
3. 创新点
4. 实验结果
5. 应用价值

每个关键点用一句话概括，用中文表达。"""
        
        user_prompt = f"""
论文标题: {title}
论文摘要: {abstract}

请提取该论文的关键信息点，以列表形式返回。
"""
        
        try:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            
            response = self.llm.invoke(messages)
            # 将响应按行分割，过滤空行
            key_points = [point.strip() for point in response.content.split('\n') if point.strip()]
            return key_points
            
        except Exception as e:
            logger.error(f"生成关键点时发生错误: {e}")
            return [f"生成失败: {str(e)}"]

# 创建全局实例
summarize_service = SummarizeService() 