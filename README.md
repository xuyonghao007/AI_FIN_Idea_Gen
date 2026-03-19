# AI_FIN_Idea_Gen - 经济学金融学研究想法生成系统

## 项目介绍

AI_FIN_Idea_Gen是一个基于LLM的经济学金融学研究想法生成与评分系统，包含两个主要模块：

1. **AutoIdea** - 单个研究想法的生成、评分和排序系统
2. **AutoIdea_Batch** - 批量处理多个初始想法的脚本

该系统能够：
- 根据初始研究想法自动生成新的研究思路
- 对生成的研究想法进行评分
- 按评分排序并返回最高十个分数的研究想法
- 批量处理多个初始想法，提高研究效率

## 项目结构

```
AI_FIN_Idea_Gen/
├── AutoIdea/            # 单个研究想法生成系统
│   ├── src/            # 源代码目录
│   │   ├── config.py   # 配置文件
│   │   ├── utils.py    # 工具函数
│   │   ├── generate.py # 研究想法生成模块
│   │   ├── score.py    # 研究想法评分模块
│   │   ├── rank.py     # 排序和筛选模块
│   │   └── main.py     # 主工作流程
│   ├── 提示词/         # 提示词文件
│   │   ├── 提示词1 想法生成.txt  # 用于生成研究想法的提示词
│   │   ├── 提示词2 想法评分.txt  # 用于评分研究想法的提示词
│   │   └── 提示词3 研究设计.txt  # 用于研究设计的提示词
│   ├── 初始想法.txt     # 初始研究想法
│   ├── 初始研究想法.xlsx # 批量处理的初始研究想法
│   ├── output/         # 输出目录（自动创建）
│   ├── requirements.txt # 依赖文件
│   ├── test.py         # 测试脚本
│   └── README.md       # 项目说明
├── AutoIdea_Batch/      # 批量处理模块
│   ├── batch_generate.py # 批量生成脚本
│   └── output_v3/      # 批量处理输出目录（自动创建）
└── README.md           # 项目总说明
```

## 环境要求

- Python 3.7+
- requests 库
- pandas 库（用于批量处理）
- 本地 LLM（如 Ollama）或 DeepSeek API 密钥

## 安装步骤

1. 克隆项目到本地
   ```bash
   git clone git@github.com:xuyonghao007/AI_FIN_Idea_Gen.git
   cd AI_FIN_Idea_Gen
   ```

2. 安装依赖：
   ```bash
   pip install -r AutoIdea/requirements.txt
   ```

3. 配置LLM设置：
   - 编辑 `AutoIdea/src/config.py` 文件
   - 选择使用本地LLM或API
   - 对于本地LLM，确保Ollama服务正在运行

## 使用方法

### 1. AutoIdea - 单个研究想法处理

#### 准备初始想法
编辑 `AutoIdea/初始想法.txt` 文件，输入您的初始研究想法。

#### 运行主工作流程
```bash
python AutoIdea/src/main.py
```

系统将：
- 运行多次，每次生成多个研究想法
- 对每个想法进行评分
- 按评分排序并筛选出前10个最高分的想法
- 将结果保存到 `AutoIdea/output` 目录

#### 查看结果
运行完成后，您可以在 `AutoIdea/output` 目录中找到：
- `all_ideas_时间戳.json` - 所有生成的想法及其评分
- `top_10_ideas_时间戳.json` - 前10个最高分的想法
- `top_10_ideas_时间戳.md` - 前10个最高分的想法（Markdown格式）

### 2. AutoIdea_Batch - 批量处理多个初始想法

#### 准备初始想法
编辑 `AutoIdea/初始研究想法.xlsx` 文件，在Excel中输入多个初始研究想法。

#### 运行批量处理
```bash
python AutoIdea_Batch/batch_generate.py
```

系统将：
- 读取Excel文件中的所有初始想法
- 为每个初始想法生成指定数量的研究想法
- 对每个生成的想法进行评分
- 为每个初始想法保存所有生成的想法和前10个最高分的想法
- 将结果保存到 `AutoIdea_Batch/output_v3` 目录

#### 查看结果
运行完成后，您可以在 `AutoIdea_Batch/output_v3` 目录中找到：
- `initial_1_all_ideas.json` - 第一个初始想法生成的所有想法
- `initial_1_top_10_ideas.json` - 第一个初始想法的前10个最高分想法
- `initial_1_top_10_ideas.md` - 第一个初始想法的前10个最高分想法（Markdown格式）
- `all_initial_results.json` - 所有初始想法的结果汇总

## 配置说明

### AutoIdea 配置
您可以在 `AutoIdea/src/config.py` 文件中调整以下配置：

- `USE_LOCAL_LLM` - 是否使用本地LLM（Ollama）
- `LOCAL_LLM_URL` - 本地LLM API地址
- `LOCAL_LLM_MODEL` - 本地LLM模型名称
- `LLM_API_URL` - 远程LLM API地址
- `LLM_API_KEY` - 远程LLM API密钥
- `LLM_MODEL` - 远程LLM模型名称
- `LLM_TEMPERATURE` - LLM生成温度
- `LLM_MAX_TOKENS` - LLM最大生成 tokens
- `NUM_IDEAS_PER_RUN` - 每次运行生成的想法数量
- `TOTAL_RUNS` - 总运行次数
- `SCORE_RANGE` - 评分范围
- `TOP_N` - 返回前N个最高分的想法

### AutoIdea_Batch 配置
您可以在 `AutoIdea_Batch/batch_generate.py` 文件中调整以下配置：

- `BATCH_OUTPUT_DIR` - 批量处理输出目录
- `ideas_per_initial` - 每个初始想法生成的想法数量

## 测试

运行测试脚本以验证AutoIdea系统功能：

```bash
python AutoIdea/test.py
```

## 技术实现

- 采用模块化设计，将生成、评分、排序等功能分离
- 支持本地LLM（Ollama）和远程API两种模式
- 基于提示词文件构建提示，确保生成和评分的质量
- 实现完整的自动工作流程，从生成到排序筛选
- 支持批量处理多个初始想法，提高研究效率

## 扩展建议

1. 可以尝试使用不同的LLM模型，如GPT-4、Claude等
2. 可以扩展提示词，以生成更符合特定领域的研究想法
3. 可以添加更多的评分维度，以获得更全面的评估
4. 可以实现Web界面，提供更友好的用户体验
5. 可以集成文献检索功能，为生成的想法提供相关文献支持

## 注意事项

1. 确保本地LLM服务（如Ollama）正在运行，或拥有有效的API密钥
2. 生成和评分过程可能需要一些时间，取决于LLM响应速度
3. 生成的研究想法质量可能因初始想法和LLM响应而异
4. 评分结果仅供参考，最终研究价值还需人工评估
5. 批量处理多个初始想法时，可能需要较长时间，请耐心等待

## 许可证

MIT
