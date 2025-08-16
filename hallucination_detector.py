# -*- coding: utf-8 -*-
"""
幻觉检测器 - 主要检测逻辑
"""

import re
import json
import logging
from typing import Dict, Any
from entity_extractor import EntityExtractor
from prompts import FACTUAL_CONSISTENCY_PROMPT, REASONING_QUALITY_PROMPT, FUNDAMENTAL_ERRORS_PROMPT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HallucinationDetector:
    """幻觉检测器"""
    
    def __init__(self):
        self.entity_extractor = EntityExtractor()
        
        # 检测维度权重（仅用于显示，不用于计算）
        self.weights = {
            'factual_consistency': 0.25,    # 事实一致性
            'reasoning_quality': 0.25,      # 推理质量
            'fundamental_errors': 0.5      # 根本性错误
        }
    
    def detect_hallucination(self, original_text: str, generated_knowledge: str) -> Dict[str, Any]:
        """
        检测生成知识中的幻觉
        
        Args:
            original_text: 原始案例文本
            generated_knowledge: 生成的知识文本
            
        Returns:
            检测结果字典
        """
        logger.info("开始幻觉检测...")
        
        # 1. 事实一致性检测
        factual_result = self._check_factual_consistency(original_text, generated_knowledge)
        
        # 2. 推理质量检测
        reasoning_result = self._check_reasoning_quality(original_text, generated_knowledge)
        
        # 3. 根本性错误检测
        error_result = self._check_fundamental_errors(original_text, generated_knowledge)
        
        # 4. 综合评估
        overall_result = self._synthesize_results(factual_result, reasoning_result, error_result)
        
        return overall_result
    
    def _check_factual_consistency(self, original_text: str, generated_knowledge: str) -> Dict[str, Any]:
        """检查事实一致性"""
        try:
            prompt = FACTUAL_CONSISTENCY_PROMPT.format(
                original_text=original_text,
                generated_knowledge=generated_knowledge
            )
            
            response = self.entity_extractor.call_deepseek_api(prompt)
            score = self._extract_score_from_response(response)
            
            return {
                'score': score,
                'analysis': response,
                'dimension': 'factual_consistency'
            }
            
        except Exception as e:
            logger.error(f"事实一致性检测异常: {str(e)}")
            return {
                'score': 0.5,
                'analysis': f"检测异常: {str(e)}",
                'dimension': 'factual_consistency'
            }
    
    def _check_reasoning_quality(self, original_text: str, generated_knowledge: str) -> Dict[str, Any]:
        """检查推理质量"""
        try:
            prompt = REASONING_QUALITY_PROMPT.format(
                original_text=original_text,
                generated_knowledge=generated_knowledge
            )
            
            response = self.entity_extractor.call_deepseek_api(prompt)
            score = self._extract_score_from_response(response)
            
            return {
                'score': score,
                'analysis': response,
                'dimension': 'reasoning_quality'
            }
            
        except Exception as e:
            logger.error(f"推理质量检测异常: {str(e)}")
            return {
                'score': 0.5,
                'analysis': f"检测异常: {str(e)}",
                'dimension': 'reasoning_quality'
            }
    
    def _check_fundamental_errors(self, original_text: str, generated_knowledge: str) -> Dict[str, Any]:
        """检查根本性错误"""
        try:
            prompt = FUNDAMENTAL_ERRORS_PROMPT.format(
                original_text=original_text,
                generated_knowledge=generated_knowledge
            )
            
            response = self.entity_extractor.call_deepseek_api(prompt)
            score = self._extract_score_from_response(response)
            
            return {
                'score': score,
                'analysis': response,
                'dimension': 'fundamental_errors'
            }
            
        except Exception as e:
            logger.error(f"根本性错误检测异常: {str(e)}")
            return {
                'score': 0.5,
                'analysis': f"检测异常: {str(e)}",
                'dimension': 'fundamental_errors'
            }
    
    def _extract_score_from_response(self, response: str) -> float:
        """从API响应中提取评分"""
        try:
            # 使用统一的格式提取评分
            score_pattern = r'### 评分：\s*\n([0-9]*\.?[0-9]+)'
            match = re.search(score_pattern, response)
            
            if match:
                score = float(match.group(1))
                return min(max(score, 0.0), 1.0)
            
            # 备用模式：查找任何0-1之间的数字
            fallback_pattern = r'\b([0-9]\.[0-9]|0\.[0-9]+|1\.0)\b'
            fallback_match = re.search(fallback_pattern, response)
            if fallback_match:
                score = float(fallback_match.group(1))
                logger.info(f"使用备用模式提取评分: {score}")
                return min(max(score, 0.0), 1.0)
            
            # 如果都没有找到，返回默认值
            logger.warning("无法从响应中提取评分，使用默认值0.5")
            return 0.5
            
        except Exception as e:
            logger.error(f"评分提取异常: {str(e)}")
            return 0.5
    
    def _synthesize_results(self, factual_result: Dict, reasoning_result: Dict, error_result: Dict) -> Dict[str, Any]:
        """综合评估结果 - 基于三个维度分数的直接判断"""
        factual_score = factual_result['score']
        reasoning_score = reasoning_result['score']
        error_score = error_result['score']
        
        # 基于三个维度分数的直接判断
        if factual_score >= 0.8 and reasoning_score >= 0.8 and error_score >= 0.8:
            category = 'high_confidence'
            hallucination_status = 'no_hallucination'
            recommendation = '高质量知识，三个维度均表现优秀'
        elif factual_score >= 0.7 and reasoning_score >= 0.7 and error_score >= 0.7:
            category = 'medium_confidence'
            hallucination_status = 'likely_no_hallucination'
            recommendation = '质量良好，三个维度均表现良好'
        elif factual_score >= 0.6 and reasoning_score >= 0.6 and error_score >= 0.6:
            category = 'low_confidence'
            hallucination_status = 'potential_hallucination'
            recommendation = '存在潜在问题，需要人工复核'
        elif factual_score >= 0.5 and reasoning_score >= 0.5 and error_score >= 0.5:
            category = 'uncertain'
            hallucination_status = 'uncertain_hallucination'
            recommendation = '质量不确定，建议重新生成'
        else:
            category = 'high_uncertainty'
            hallucination_status = 'likely_hallucination'
            recommendation = '可能存在幻觉，建议重新生成'
        
        # 计算加权总分（仅用于参考，不用于判断）
        weighted_score = (
            factual_score * self.weights['factual_consistency'] +
            reasoning_score * self.weights['reasoning_quality'] +
            error_score * self.weights['fundamental_errors']
        )
        
        return {
            'overall_score': weighted_score,  # 保留加权分数作为参考
            'category': category,
            'hallucination_status': hallucination_status,
            'recommendation': recommendation,
            'detailed_scores': {
                'factual_consistency': factual_score,
                'reasoning_quality': reasoning_score,
                'fundamental_errors': error_score
            },
            'detailed_analysis': {
                'factual_consistency': factual_result['analysis'],
                'reasoning_quality': reasoning_result['analysis'],
                'fundamental_errors': error_result['analysis']
            },
            'weights_used': self.weights,
            'judgment_criteria': {
                'method': 'direct_dimension_judgment',
                'description': '基于三个维度分数的直接判断，要求所有维度都达到相应阈值'
            }
        }
    
    def save_result(self, result: Dict[str, Any], filename: str = 'hallucination_detection_result.json'):
        """保存检测结果到文件"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            logger.info(f"检测结果已保存到: {filename}")
        except Exception as e:
            logger.error(f"保存结果失败: {str(e)}")
    
    def print_result(self, result: Dict[str, Any]):
        """打印检测结果"""
        print("\n" + "="*60)
        print("幻觉检测结果")
        print("="*60)
        print(f"综合评分(参考): {result['overall_score']:.3f}")
        print(f"置信度类别: {result['category']}")
        print(f"幻觉状态: {result['hallucination_status']}")
        print(f"建议: {result['recommendation']}")
        
        print("\n详细评分:")
        print("-"*30)
        for dimension, score in result['detailed_scores'].items():
            print(f"{dimension}: {score:.3f}")
        
        print("\n判断标准:")
        print("-"*30)
        print(f"方法: {result['judgment_criteria']['method']}")
        print(f"说明: {result['judgment_criteria']['description']}")
        
        print("\n权重配置(仅用于参考):")
        print("-"*30)
        for dimension, weight in result['weights_used'].items():
            print(f"{dimension}: {weight}")
        
        print("\n详细分析:")
        print("-"*30)
        for dimension, analysis in result['detailed_analysis'].items():
            print(f"\n{dimension}:")
            print(analysis[:300] + "..." if len(analysis) > 300 else analysis)
