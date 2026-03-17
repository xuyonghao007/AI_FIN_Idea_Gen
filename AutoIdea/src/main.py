# 主工作流程

import time
from typing import List, Dict

import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import TOTAL_RUNS, OUTPUT_DIR
from generate import generate_ideas
from score import score_ideas
from rank import rank_ideas, get_top_ideas
from utils import write_json, write_file


def main_workflow():
    """主工作流程"""
    all_ideas = []
    
    print("开始执行AutoIdea工作流程...")
    print(f"将运行 {TOTAL_RUNS} 次，每次生成3个研究想法")
    print("=" * 80)
    
    for run in range(1, TOTAL_RUNS + 1):
        print(f"\n第 {run} 次运行:")
        print("-" * 40)
        
        # 生成想法
        print("1. 生成研究想法...")
        start_time = time.time()
        ideas = generate_ideas()
        end_time = time.time()
        print(f"生成完成，耗时 {end_time - start_time:.2f} 秒")
        
        # 评分想法
        print("2. 对研究想法进行评分...")
        start_time = time.time()
        scored_ideas = score_ideas(ideas)
        end_time = time.time()
        print(f"评分完成，耗时 {end_time - start_time:.2f} 秒")
        
        # 添加到总列表
        all_ideas.extend(scored_ideas)
        
        # 打印本次运行结果
        print("本次运行生成的想法及评分:")
        for i, item in enumerate(scored_ideas, 1):
            print(f"  {i}. 评分: {item['score']} - {item['idea'][:100]}...")
    
    print("\n" + "=" * 80)
    print("所有运行完成，开始排序和筛选...")
    
    # 排序所有想法
    sorted_ideas = rank_ideas(all_ideas)
    
    # 获取前10个最高分的想法
    top_ideas = get_top_ideas(sorted_ideas)
    
    # 保存结果
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    
    # 保存所有想法
    all_ideas_path = f"{OUTPUT_DIR}/all_ideas_{timestamp}.json"
    write_json(all_ideas_path, sorted_ideas)
    print(f"所有想法已保存到: {all_ideas_path}")
    
    # 保存前10个想法
    top_ideas_path = f"{OUTPUT_DIR}/top_10_ideas_{timestamp}.json"
    write_json(top_ideas_path, top_ideas)
    print(f"前10个最高分的想法已保存到: {top_ideas_path}")
    
    # 保存前10个想法的文本版本
    top_ideas_text = "# 前10个最高分的研究想法\n\n"
    for i, item in enumerate(top_ideas, 1):
        top_ideas_text += f"## {i}. 评分: {item['score']}\n"
        top_ideas_text += f"{item['idea']}\n\n"
    
    top_ideas_text_path = f"{OUTPUT_DIR}/top_10_ideas_{timestamp}.md"
    write_file(top_ideas_text_path, top_ideas_text)
    print(f"前10个最高分的想法(文本版)已保存到: {top_ideas_text_path}")
    
    # 打印前10个想法
    print("\n" + "=" * 80)
    print("前10个最高分的研究想法:")
    print("=" * 80)
    for i, item in enumerate(top_ideas, 1):
        print(f"\n{i}. 评分: {item['score']}")
        print(f"   {item['idea']}")
    
    print("\n" + "=" * 80)
    print("AutoIdea工作流程执行完成！")


def main():
    """主函数"""
    main_workflow()


if __name__ == "__main__":
    main()
