# 配置文件

import os

# 获取当前文件目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 提示词文件路径
PROMPT_GENERATE_PATH = os.path.join(BASE_DIR, "提示词", "提示词1 想法生成.txt")
PROMPT_SCORE_PATH = os.path.join(BASE_DIR, "提示词", "提示词2 想法评分.txt")

# 初始想法文件路径
INITIAL_IDEA_PATH = os.path.join(BASE_DIR, "初始想法.txt")

# 输出文件路径
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

# LLM配置
LLM_TYPE = "local"  # 可选: "api", "local" 或 "test"

# API模式配置
LLM_API_URL = "https://api.deepseek.com/v1/chat/completions"
LLM_API_KEY = "your_api_key_here"  # 请替换为实际的API密钥
LLM_MODEL = "deepseek-chat"

# 本地模式配置
LOCAL_LLM_URL = "http://localhost:11434/api/chat"
LOCAL_LLM_MODEL = "gemma3:12b"

# 测试模式配置
TEST_MODE = LLM_TYPE == "test"

# 通用配置
LLM_TEMPERATURE = 0.7
LLM_MAX_TOKENS = 2000

# 生成配置
NUM_IDEAS_PER_RUN = 3  # 每次生成的想法数量
TOTAL_RUNS = 50        # 总运行次数，以获得足够多的想法

# 评分配置
SCORE_RANGE = (0, 100)  # 评分范围

# 排序配置
TOP_N = 10  # 返回前10个最高分的想法
