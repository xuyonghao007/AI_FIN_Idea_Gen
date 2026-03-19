# 测试脚本

import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from generate import generate_ideas
from score import score_idea
from rank import rank_ideas, get_top_ideas


def test_generate():
    """测试想法生成功能"""
    print("测试想法生成功能...")
    ideas = generate_ideas()
    print(f"生成了 {len(ideas)} 个想法")
    for i, idea in enumerate(ideas, 1):
        print(f"{i}. {idea}")
    return ideas


def test_score(ideas):
    """测试想法评分功能"""
    print("\n测试想法评分功能...")
    scored_ideas = []
    for idea in ideas:
        score = score_idea(idea)
        scored_ideas.append({"idea": idea, "score": score})
        print(f"评分: {score} - {idea[:100]}...")
    return scored_ideas


def test_rank(scored_ideas):
    """测试排序和筛选功能"""
    print("\n测试排序和筛选功能...")
    sorted_ideas = rank_ideas(scored_ideas)
    top_ideas = get_top_ideas(sorted_ideas)
    print("前10个最高分的想法:")
    for i, item in enumerate(top_ideas, 1):
        print(f"{i}. 评分: {item['score']} - {item['idea'][:100]}...")
    return top_ideas


def main():
    """运行所有测试"""
    print("开始测试AutoIdea系统...")
    print("=" * 80)
    
    # 测试生成功能
    ideas = test_generate()
    
    # 测试评分功能
    scored_ideas = test_score(ideas)
    
    # 测试排序和筛选功能
    top_ideas = test_rank(scored_ideas)
    
    print("\n" + "=" * 80)
    print("测试完成！")


if __name__ == "__main__":
    main()
