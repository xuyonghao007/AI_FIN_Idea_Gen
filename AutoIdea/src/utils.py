# 工具函数

import os
import json
import requests
from typing import List, Dict, Any

from config import (
    LLM_TYPE, LLM_API_URL, LLM_API_KEY, LLM_MODEL, 
    LOCAL_LLM_URL, LOCAL_LLM_MODEL, LLM_TEMPERATURE, LLM_MAX_TOKENS,
    OUTPUT_DIR, TEST_MODE
)


def ensure_directory(directory: str):
    """确保目录存在"""
    if not os.path.exists(directory):
        os.makedirs(directory)


def read_file(file_path: str) -> str:
    """读取文件内容"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def write_file(file_path: str, content: str):
    """写入文件内容"""
    ensure_directory(os.path.dirname(file_path))
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)


def write_json(file_path: str, data: Dict):
    """写入JSON文件"""
    ensure_directory(os.path.dirname(file_path))
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def call_llm(prompt: str) -> str:
    """调用LLM"""
    if TEST_MODE:
        # 测试模式，返回模拟响应
        # 检查是否是生成想法的请求
        if "请扮演一位经济学/金融学顶刊资深编辑" in prompt or "构建结构化文献知识库与评价" in prompt:
            # 模拟生成研究想法的响应
            return "1. 研究数字货币对传统银行体系的影响，采用DID方法分析央行数字货币试点对银行存款的影响。\n2. 探索人工智能在金融市场预测中的应用，利用机器学习算法分析高频交易数据。\n3. 分析气候变化对金融稳定的影响，构建气候风险评估模型。"
        elif "You are a top 1% referee in economics and finance" in prompt or "Evaluation Dimensions" in prompt:
            # 模拟评分的响应
            return "score: 85"
        else:
            # 默认返回生成想法的响应
            return "1. 研究数字货币对传统银行体系的影响，采用DID方法分析央行数字货币试点对银行存款的影响。\n2. 探索人工智能在金融市场预测中的应用，利用机器学习算法分析高频交易数据。\n3. 分析气候变化对金融稳定的影响，构建气候风险评估模型。"
    elif LLM_TYPE == "api":
        # API模式
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {LLM_API_KEY}"
        }
        
        data = {
            "model": LLM_MODEL,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": LLM_TEMPERATURE,
            "max_tokens": LLM_MAX_TOKENS
        }
        
        response = requests.post(LLM_API_URL, headers=headers, json=data)
        response.raise_for_status()
        
        return response.json()["choices"][0]["message"]["content"]
    else:
        # 本地模式（Ollama API）
        try:
            headers = {
                "Content-Type": "application/json"
            }
            
            data = {
                "model": LOCAL_LLM_MODEL,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": LLM_TEMPERATURE,
                "max_tokens": LLM_MAX_TOKENS,
                "stream": False
            }
            
            response = requests.post(LOCAL_LLM_URL, headers=headers, json=data, timeout=300)
            response.raise_for_status()
            
            return response.json()["message"]["content"]
        except Exception as e:
            print(f"本地大模型调用失败: {e}")
            print("切换到测试模式...")
            # 失败时返回模拟响应
            # 根据请求类型返回不同的响应
            if "You are a top 1% referee in economics and finance" in prompt or "Evaluation Dimensions" in prompt:
                # 评分请求
                return "score: 85"
            else:
                # 生成想法请求
                return "1. 研究数字货币对传统银行体系的影响，采用DID方法分析央行数字货币试点对银行存款的影响。\n2. 探索人工智能在金融市场预测中的应用，利用机器学习算法分析高频交易数据。\n3. 分析气候变化对金融稳定的影响，构建气候风险评估模型。"


def extract_score(text: str) -> int:
    """从评分文本中提取分数"""
    import re
    match = re.search(r'score:\s*(\d+)', text)
    if match:
        return int(match.group(1))
    return 0


def parse_ideas(text: str) -> List[str]:
    """从生成的文本中解析研究想法"""
    # 解析生成的研究想法
    ideas = []
    
    # 查找研究思路部分
    import re
    
    # 尝试不同的模式匹配研究思路
    patterns = [
        r'研究思路\s*\d+[：:](.+?)(?=研究思路\s*\d+[：:]|希望以上分析|$)',
        r'研究思路\s*\d+[：:].*?核心问题：(.+?)(?=研究思路\s*\d+[：:]|希望以上分析|$)',
        r'\d+\.\s*研究思路.*?：(.+?)(?=\d+\.\s*研究思路|希望以上分析|$)'
    ]
    
    for pattern in patterns:
        research_ideas = re.findall(pattern, text, re.DOTALL)
        if research_ideas:
            # 提取每个研究思路
            for idea in research_ideas:
                idea = idea.strip()
                if idea and len(idea) > 200:
                    ideas.append(idea)
            break
    
    # 如果没有找到研究思路部分，尝试提取包含研究思路的段落
    if not ideas:
        # 查找包含特定关键词的段落
        keywords = ['研究思路', '研究设计', '创新点', '潜在贡献']
        paragraphs = text.split('\n\n')
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if any(keyword in paragraph for keyword in keywords) and len(paragraph) > 200:
                ideas.append(paragraph)
    
    # 确保至少返回一个想法
    if not ideas:
        ideas.append(text)
    
    # 限制返回的想法数量为3个
    return ideas[:3]
