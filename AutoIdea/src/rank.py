# 排序和筛选模块

from typing import List, Dict

import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import TOP_N


def rank_ideas(scored_ideas: List[Dict]) -> List[Dict]:
    """对评分后的研究想法进行排序"""
    # 按评分降序排序
    sorted_ideas = sorted(scored_ideas, key=lambda x: x['score'], reverse=True)
    return sorted_ideas


def get_top_ideas(sorted_ideas: List[Dict]) -> List[Dict]:
    """获取前N个最高分的研究想法"""
    return sorted_ideas[:TOP_N]


def main():
    """测试排序和筛选模块"""
    test_scored_ideas = [
        {"idea": "研究数字货币对传统银行体系的影响", "score": 85},
        {"idea": "探索人工智能在金融市场预测中的应用", "score": 90},
        {"idea": "分析气候变化对金融稳定的影响", "score": 75},
        {"idea": "研究区块链技术在供应链金融中的应用", "score": 88},
        {"idea": "分析 FinTech 对传统金融机构的冲击", "score": 82},
        {"idea": "研究ESG投资对企业绩效的影响", "score": 86},
        {"idea": "分析人口老龄化对金融市场的影响", "score": 78},
        {"idea": "研究数字经济对就业市场的影响", "score": 80},
        {"idea": "分析贸易摩擦对全球金融市场的影响", "score": 83},
        {"idea": "研究金融科技监管对创新的影响", "score": 87},
        {"idea": "分析加密货币市场的波动性", "score": 79}
    ]
    
    sorted_ideas = rank_ideas(test_scored_ideas)
    top_ideas = get_top_ideas(sorted_ideas)
    
    print("排序后的研究想法:")
    for i, item in enumerate(sorted_ideas, 1):
        print(f"{i}. 评分: {item['score']} - {item['idea']}")
    
    print("\n前10个最高分的研究想法:")
    for i, item in enumerate(top_ideas, 1):
        print(f"{i}. 评分: {item['score']} - {item['idea']}")


if __name__ == "__main__":
    main()
