"""
Arxiv搜索服务模块

该模块封装了与Arxiv API的交互，提供论文检索功能。
支持按标题、作者、关键词等条件搜索论文。
"""

import arxiv
import logging
from typing import List, Dict, Optional
from dataclasses import dataclass

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class PaperInfo:
    """论文信息数据类"""
    title: str
    authors: List[str]
    abstract: str
    arxiv_id: str
    published_date: str
    categories: List[str]
    pdf_url: str

class ArxivSearchService:
    """Arxiv搜索服务类"""
    
    def __init__(self, max_results: int = 5):
        """
        初始化Arxiv搜索服务
        
        Args:
            max_results: 最大返回结果数量，默认5篇
        """
        self.max_results = max_results
        self.client = arxiv.Client(
            page_size=100,
            delay_seconds=3,
            num_retries=3
        )
    
    def search_by_title(self, title: str) -> List[PaperInfo]:
        """
        按标题搜索论文
        
        Args:
            title: 论文标题关键词
            
        Returns:
            List[PaperInfo]: 论文信息列表
        """
        try:
            # 构建搜索查询
            query = f"ti:\"{title}\""
            search = arxiv.Search(
                query=query,
                max_results=self.max_results,
                sort_by=arxiv.SortCriterion.Relevance
            )
            
            results = list(self.client.results(search))
            return [self._convert_to_paper_info(result) for result in results]
            
        except Exception as e:
            logger.error(f"搜索论文时发生错误: {e}")
            return []
    
    def search_by_keywords(self, keywords: str) -> List[PaperInfo]:
        """
        按关键词搜索论文
        
        Args:
            keywords: 搜索关键词
            
        Returns:
            List[PaperInfo]: 论文信息列表
        """
        try:
            search = arxiv.Search(
                query=keywords,
                max_results=self.max_results,
                sort_by=arxiv.SortCriterion.Relevance
            )
            
            results = list(self.client.results(search))
            return [self._convert_to_paper_info(result) for result in results]
            
        except Exception as e:
            logger.error(f"按关键词搜索时发生错误: {e}")
            return []
    
    def search_by_author(self, author: str) -> List[PaperInfo]:
        """
        按作者搜索论文
        
        Args:
            author: 作者姓名
            
        Returns:
            List[PaperInfo]: 论文信息列表
        """
        try:
            query = f"au:\"{author}\""
            search = arxiv.Search(
                query=query,
                max_results=self.max_results,
                sort_by=arxiv.SortCriterion.SubmittedDate
            )
            
            results = list(self.client.results(search))
            return [self._convert_to_paper_info(result) for result in results]
            
        except Exception as e:
            logger.error(f"按作者搜索时发生错误: {e}")
            return []
    
    def get_paper_by_id(self, arxiv_id: str) -> Optional[PaperInfo]:
        """
        根据Arxiv ID获取论文详情
        
        Args:
            arxiv_id: Arxiv论文ID
            
        Returns:
            Optional[PaperInfo]: 论文信息，如果未找到则返回None
        """
        try:
            search = arxiv.Search(id_list=[arxiv_id])
            results = list(self.client.results(search))
            
            if results:
                return self._convert_to_paper_info(results[0])
            return None
            
        except Exception as e:
            logger.error(f"获取论文详情时发生错误: {e}")
            return None
    
    def _convert_to_paper_info(self, result) -> PaperInfo:
        """
        将arxiv搜索结果转换为PaperInfo对象
        
        Args:
            result: arxiv搜索结果对象
            
        Returns:
            PaperInfo: 论文信息对象
        """
        return PaperInfo(
            title=result.title,
            authors=[author.name for author in result.authors],
            abstract=result.summary,
            arxiv_id=result.entry_id.split('/')[-1],
            published_date=result.published.strftime('%Y-%m-%d') if result.published else '',
            categories=result.categories,
            pdf_url=result.pdf_url
        )
    
    def format_paper_info(self, paper: PaperInfo) -> str:
        """
        格式化论文信息为可读字符串
        
        Args:
            paper: 论文信息对象
            
        Returns:
            str: 格式化后的论文信息
        """
        return f"""
标题: {paper.title}
作者: {', '.join(paper.authors)}
Arxiv ID: {paper.arxiv_id}
发布日期: {paper.published_date}
分类: {', '.join(paper.categories)}
摘要: {paper.abstract}
PDF链接: {paper.pdf_url}
"""

# 创建全局实例
arxiv_service = ArxivSearchService() 