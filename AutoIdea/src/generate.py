# 研究想法生成模块

from typing import List

import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import PROMPT_GENERATE_PATH, INITIAL_IDEA_PATH
from utils import read_file, call_llm, parse_ideas


def generate_ideas(initial_idea: str = None) -> List[str]:
    """生成研究想法"""
    # 读取提示词
    prompt_template = read_file(PROMPT_GENERATE_PATH)
    
    # 如果没有提供初始想法，从文件中读取
    if initial_idea is None:
        initial_idea = read_file(INITIAL_IDEA_PATH)
    
    # 构建完整的提示
    full_prompt = prompt_template + "\n" + initial_idea
    
    # 调用LLM生成想法
    response = call_llm(full_prompt)
    
    # 解析生成的想法
    ideas = parse_ideas(response)
    
    return ideas


def main():
    """测试生成模块"""
    ideas = generate_ideas()
    print("生成的研究想法:")
    for i, idea in enumerate(ideas, 1):
        print(f"{i}. {idea}")


if __name__ == "__main__":
    main()
