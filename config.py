#!/usr/bin/env python3
"""
ScholarAgent 配置管理模块

该模块负责管理应用的配置信息，包括API密钥、模型参数等。
支持从环境变量和配置文件读取配置。
"""

import os
import logging
from typing import Optional
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

logger = logging.getLogger(__name__)

class Config:
    """配置管理类"""
    
    def __init__(self):
        """初始化配置"""
        self._load_config()
    
    def _load_config(self):
        """加载配置"""
        # DeepSeek API配置
        self.deepseek_api_key = self._get_env_var("DEEPSEEK_API_KEY")
        self.deepseek_base_url = self._get_env_var("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
        self.deepseek_model = self._get_env_var("DEEPSEEK_MODEL", "deepseek-chat")
        
        # OpenAI API配置（可选）
        self.openai_api_key = self._get_env_var("OPENAI_API_KEY")
        self.openai_base_url = self._get_env_var("OPENAI_BASE_URL", "https://api.openai.com/v1")
        self.openai_model = self._get_env_var("OPENAI_MODEL", "gpt-4")
        
        # 应用配置
        self.temperature = float(self._get_env_var("TEMPERATURE", "0.3") or "0.3")
        self.max_iterations = int(self._get_env_var("MAX_ITERATIONS", "10") or "10")
        verbose_str = self._get_env_var("VERBOSE", "true") or "true"
        self.verbose = verbose_str.lower() == "true"
        
        # 验证必要的配置
        self._validate_config()
    
    def _get_env_var(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """获取环境变量"""
        value = os.getenv(key, default)
        if key.endswith("_API_KEY") and not value:
            logger.warning(f"未设置 {key}，请检查环境变量配置")
        return value
    
    def _validate_config(self):
        """验证配置"""
        if not self.deepseek_api_key:
            logger.error("未设置 DEEPSEEK_API_KEY，请检查环境变量配置")
            raise ValueError("DEEPSEEK_API_KEY 是必需的配置项")
    
    def get_llm_config(self, provider: str = "deepseek") -> dict:
        """
        获取LLM配置
        
        Args:
            provider: 提供商 ("deepseek" 或 "openai")
            
        Returns:
            dict: LLM配置字典
        """
        if provider.lower() == "deepseek":
            return {
                "model": self.deepseek_model,
                "base_url": self.deepseek_base_url,
                "api_key": self.deepseek_api_key,
                "temperature": self.temperature
            }
        elif provider.lower() == "openai":
            if not self.openai_api_key:
                raise ValueError("未设置 OPENAI_API_KEY")
            return {
                "model": self.openai_model,
                "base_url": self.openai_base_url,
                "api_key": self.openai_api_key,
                "temperature": self.temperature
            }
        else:
            raise ValueError(f"不支持的提供商: {provider}")
    
    def get_agent_config(self) -> dict:
        """
        获取Agent配置
        
        Returns:
            dict: Agent配置字典
        """
        return {
            "max_iterations": self.max_iterations,
            "verbose": self.verbose,
            "temperature": self.temperature
        }

# 全局配置实例
config = Config() 