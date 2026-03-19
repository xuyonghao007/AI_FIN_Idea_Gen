# AutoIdea - 经济学金融学研究想法自动生成与评分系统

## 项目介绍

AutoIdea是一个基于LLM的经济学金融学研究想法自动生成与评分系统，参考了autoresearch的设计理念。该系统能够：

1. 根据初始研究想法和提示词自动生成新的研究思路
2. 对生成的研究想法进行评分
3. 按评分排序并返回最高十个分数的研究想法

## 项目结构

```
AutoIdea/
├── src/                # 源代码目录
│   ├── config.py       # 配置文件
│   ├── utils.py        # 工具函数
│   ├── generate.py     # 研究想法生成模块
│   ├── score.py        # 研究想法评分模块
│   ├── rank.py         # 排序和筛选模块
│   └── main.py         # 主工作流程
├── 提示词/             # 提示词文件
│   ├── 提示词1 想法生成.txt  # 用于生成研究想法的提示词
│   └── 提示词2 想法评分.txt  # 用于评分研究想法的提示词
├── 初始想法.txt         # 初始研究想法
├── output/             # 输出目录（自动创建）
├── requirements.txt    # 依赖文件
├── test.py             # 测试脚本
└── README.md           # 项目说明
```

## 环境要求

- Python 3.7+
- requests 库
- DeepSeek API 密钥（用于调用LLM）

## 安装步骤

1. 克隆项目到本地
2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
3. 配置API密钥：
   - 编辑 `src/config.py` 文件，将 `LLM_API_KEY` 设置为您的DeepSeek API密钥

## 使用方法

### 1. 准备初始想法

编辑 `初始想法.txt` 文件，输入您的初始研究想法。

### 2. 运行主工作流程

```bash
python src/main.py
```

系统将：
- 运行10次，每次生成3个研究想法
- 对每个想法进行评分
- 按评分排序并筛选出前10个最高分的想法
- 将结果保存到 `output` 目录

### 3. 查看结果

运行完成后，您可以在 `output` 目录中找到：
- `all_ideas_时间戳.json` - 所有生成的想法及其评分
- `top_10_ideas_时间戳.json` - 前10个最高分的想法
- `top_10_ideas_时间戳.md` - 前10个最高分的想法（Markdown格式）

## 测试

运行测试脚本以验证系统功能：

```bash
python test.py
```

## 配置说明

您可以在 `src/config.py` 文件中调整以下配置：

- `PROMPT_GENERATE_PATH` - 想法生成提示词文件路径
- `PROMPT_SCORE_PATH` - 想法评分提示词文件路径
- `INITIAL_IDEA_PATH` - 初始想法文件路径
- `OUTPUT_DIR` - 输出目录路径
- `LLM_API_URL` - LLM API地址
- `LLM_API_KEY` - LLM API密钥
- `LLM_MODEL` - LLM模型名称
- `LLM_TEMPERATURE` - LLM生成温度
- `LLM_MAX_TOKENS` - LLM最大生成 tokens
- `NUM_IDEAS_PER_RUN` - 每次运行生成的想法数量
- `TOTAL_RUNS` - 总运行次数
- `SCORE_RANGE` - 评分范围
- `TOP_N` - 返回前N个最高分的想法

## 注意事项

1. 确保您拥有有效的DeepSeek API密钥
2. 生成和评分过程可能需要一些时间，取决于API响应速度
3. 生成的研究想法质量可能因初始想法和LLM响应而异
4. 评分结果仅供参考，最终研究价值还需人工评估

## 技术实现

- 采用模块化设计，将生成、评分、排序等功能分离
- 使用DeepSeek API进行文本生成和评分
- 基于提示词文件构建提示，确保生成和评分的质量
- 实现完整的自动工作流程，从生成到排序筛选

## 扩展建议

1. 可以尝试使用不同的LLM模型，如GPT-4、Claude等
2. 可以扩展提示词，以生成更符合特定领域的研究想法
3. 可以添加更多的评分维度，以获得更全面的评估
4. 可以实现批量处理功能，一次处理多个初始想法

## 许可证

MIT
