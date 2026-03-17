# 研究想法评分模块

from typing import List, Dict

import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import PROMPT_SCORE_PATH
from utils import read_file, call_llm, extract_score


def score_idea(idea: str) -> int:
    """对单个研究想法进行评分"""
    # 读取评分提示词
    prompt_template = read_file(PROMPT_SCORE_PATH)
    
    # 构建完整的评分提示
    full_prompt = prompt_template + "\n\n" + idea
    
    # 调用LLM进行评分
    response = call_llm(full_prompt)
    
    # 提取评分
    score = extract_score(response)
    
    return score


def score_ideas(ideas: List[str]) -> List[Dict]:
    """对多个研究想法进行评分"""
    scored_ideas = []
    
    for idea in ideas:
        score = score_idea(idea)
        scored_ideas.append({
            "idea": idea,
            "score": score
        })
    
    return scored_ideas


def main():
    """测试评分模块"""
    test_ideas = [
        "1. 研究数字货币对传统银行体系的影响，采用DID方法分析央行数字货币试点对银行存款的影响。",
        "2. 探索人工智能在金融市场预测中的应用，利用机器学习算法分析高频交易数据。",
        "3. 分析气候变化对金融稳定的影响，构建气候风险评估模型。"
    ]
    
    scored_ideas = score_ideas(test_ideas)
    print("评分结果:")
    for item in scored_ideas:
        print(f"想法: {item['idea']}")
        print(f"评分: {item['score']}")
        print()


if __name__ == "__main__":
    main()
