# 批量生成研究想法脚本

import os
import sys
import pandas as pd
import time
from typing import List, Dict

# 添加autoidea/src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'autoidea', 'src'))

from config import OUTPUT_DIR as ORIGINAL_OUTPUT_DIR
from generate import generate_ideas
from score import score_ideas
from rank import rank_ideas, get_top_ideas
from utils import write_json, write_file, ensure_directory

# 新的输出目录
BATCH_OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'output_v3')


def read_initial_ideas(excel_path: str) -> List[str]:
    """读取Excel文件中的初始研究想法"""
    df = pd.read_excel(excel_path)
    # 假设Excel文件中有一列名为"研究想法"或"idea"的列
    if '研究想法' in df.columns:
        return df['研究想法'].dropna().tolist()
    elif 'idea' in df.columns:
        return df['idea'].dropna().tolist()
    else:
        # 如果没有明确的列名，返回所有非空单元格
        ideas = []
        for col in df.columns:
            ideas.extend(df[col].dropna().tolist())
        return ideas


def batch_generate(initial_ideas: List[str], ideas_per_initial: int = 10):
    """为每个初始想法生成指定数量的研究想法"""
    ensure_directory(BATCH_OUTPUT_DIR)
    
    all_results = []
    
    print(f"开始批量生成研究想法...")
    print(f"将处理 {len(initial_ideas)} 个初始想法，每个生成 {ideas_per_initial} 个研究想法")
    print("=" * 80)
    
    for i, initial_idea in enumerate(initial_ideas, 1):
        print(f"\n处理第 {i} 个初始想法:")
        print(f"初始想法: {initial_idea[:100]}...")
        print("-" * 40)
        
        # 为每个初始想法生成多个研究想法
        initial_results = []
        
        for j in range(1, ideas_per_initial + 1):
            print(f"  生成第 {j} 个研究想法...")
            start_time = time.time()
            
            # 生成想法
            ideas = generate_ideas(initial_idea=initial_idea)
            
            # 评分想法
            scored_ideas = score_ideas(ideas)
            
            initial_results.extend(scored_ideas)
            
            end_time = time.time()
            print(f"  完成，耗时 {end_time - start_time:.2f} 秒")
        
        # 对当前初始想法的所有生成结果进行排序
        sorted_results = rank_ideas(initial_results)
        
        # 获取前10个最高分的想法
        top_results = get_top_ideas(sorted_results)
        
        # 保存当前初始想法的结果
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        initial_idea_id = f"initial_{i}"
        
        # 保存所有生成的想法
        all_ideas_path = os.path.join(BATCH_OUTPUT_DIR, f"{initial_idea_id}_all_ideas.json")
        write_json(all_ideas_path, sorted_results)
        print(f"  所有生成的想法已保存到: {all_ideas_path}")
        
        # 保存前10个最高分的想法
        top_ideas_path = os.path.join(BATCH_OUTPUT_DIR, f"{initial_idea_id}_top_10_ideas.json")
        write_json(top_ideas_path, top_results)
        print(f"  前10个最高分的想法已保存到: {top_ideas_path}")
        
        # 保存前10个想法的文本版本
        top_ideas_text = f"# 基于初始想法 {i} 生成的前10个最高分研究想法\n\n"
        top_ideas_text += f"## 初始想法\n{initial_idea}\n\n"
        for k, item in enumerate(top_results, 1):
            top_ideas_text += f"## {k}. 评分: {item['score']}\n"
            top_ideas_text += f"{item['idea']}\n\n"
        
        top_ideas_text_path = os.path.join(BATCH_OUTPUT_DIR, f"{initial_idea_id}_top_10_ideas.md")
        write_file(top_ideas_text_path, top_ideas_text)
        print(f"  前10个最高分的想法(文本版)已保存到: {top_ideas_text_path}")
        
        # 添加到总结果
        all_results.append({
            "initial_idea": initial_idea,
            "generated_ideas": sorted_results,
            "top_ideas": top_results
        })
    
    # 保存所有初始想法的结果
    all_initial_results_path = os.path.join(BATCH_OUTPUT_DIR, f"all_initial_results.json")
    write_json(all_initial_results_path, all_results)
    print(f"\n所有初始想法的结果已保存到: {all_initial_results_path}")
    
    print("\n" + "=" * 80)
    print("批量生成研究想法完成！")


def main():
    """主函数"""
    # Excel文件路径
    excel_path = os.path.join(os.path.dirname(__file__), '..', 'AutoIdea', '初始研究想法.xlsx')
    
    # 读取初始研究想法
    initial_ideas = read_initial_ideas(excel_path)
    
    # 批量生成研究想法
    batch_generate(initial_ideas, ideas_per_initial=10)


if __name__ == "__main__":
    main()
