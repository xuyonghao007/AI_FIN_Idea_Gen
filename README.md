# 文献处理与研究想法生成系统

## 项目概述

本项目是一个综合性的文献处理与研究想法生成系统，旨在帮助研究人员更高效地处理文献数据、检索相似文献、生成研究想法以及优化研究设计。系统由三个主要模块组成：文献数据提取器、文献相似度检索器和研究想法生成器。

## 目录结构

```
literature_processor/
├── extractors/          # 文献数据提取器
│   ├── __init__.py
│   ├── extract_literature.py  # 主要提取脚本
│   └── README.md             # 模块说明文档
├── retrievers/          # 文献相似度检索器
│   ├── __init__.py
│   ├── similarity_retriever.py  # 主要检索脚本
│   └── README.md             # 模块说明文档
└── idea_generator/      # 研究想法生成器
    ├── __init__.py
    ├── app.py                # Streamlit应用主文件
    ├── README.md             # 模块说明文档
    ├── conversation_history/  # 对话记录存储
    └── prompt_templates/     # 提示词模板文件夹
        ├── 1_理论拓展型.txt
        ├── 2_方法创新型.txt
        ├── 3_实证拓展型.txt
        ├── 4_跨学科融合型.txt
        ├── 5_政策启示型.txt
        └── 6_研究设计优化型.txt
```

## 功能模块

### 1. 文献数据提取器 (extractors)

**功能**：从指定文件夹及其子文件夹中提取所有TXT格式的文献数据，包括文献标题、内容（前1000个字符）和文件路径。

**使用方法**：
```bash
python literature_processor/extractors/extract_literature.py [文件夹路径] --output output.json
```

### 2. 文献相似度检索器 (retrievers)

**功能**：基于TF-IDF和余弦相似度对文献进行相似度检索，返回最相似的文献。

**使用方法**：
```bash
python literature_processor/retrievers/similarity_retriever.py literature_data.json "查询文本" --top_k 5 --output results.json
```

### 3. 研究想法生成器 (idea_generator)

**功能**：基于用户研究想法和参考顶刊文献摘要，生成具有理论突破的研究想法，并提供研究设计优化功能。

**主要功能**：
- 相似文献检索：基于用户输入的研究想法检索相似文献
- 研究想法生成：根据用户研究想法和参考文献生成新的研究想法
- 研究设计优化：根据用户研究想法和上传的参考论文优化研究设计

**使用方法**：
```bash
streamlit run literature_processor/idea_generator/app.py
```

## 安装依赖

### 基本依赖

```bash
pip install -r requirements.txt
```

### 详细依赖列表

- Python 3.6+
- streamlit
- requests
- scikit-learn
- PyPDF2

## 快速开始

1. **提取文献数据**：
   ```bash
   python literature_processor/extractors/extract_literature.py "文献数据" --output literature_data.json
   ```

2. **启动研究想法生成器**：
   ```bash
   streamlit run literature_processor/idea_generator/app.py
   ```

3. **使用流程**：
   - 在"相似文献检索"标签页：输入研究想法，检索相似文献
   - 在"研究想法生成"标签页：输入研究想法，选择API和提示词模板，生成研究想法
   - 在"研究设计优化"标签页：输入研究想法，上传参考论文，优化研究设计

## 示例

### 示例1：提取文献数据

```bash
python literature_processor/extractors/extract_literature.py "文献数据" --output literature_data.json
```

### 示例2：检索相似文献

```bash
python literature_processor/retrievers/similarity_retriever.py literature_data.json "corporate investment and uncertainty" --top_k 5 --output results.json
```

### 示例3：生成研究想法

1. 启动Streamlit应用：
   ```bash
   streamlit run literature_processor/idea_generator/app.py
   ```

2. 在"研究想法生成"标签页：
   - 选择API（DeepSeek或Qwen）
   - 输入API密钥
   - 选择提示词模板（如"理论拓展型"）
   - 上传包含参考文献的JSON文件
   - 输入研究想法
   - 点击"生成研究想法"按钮

## 注意事项

1. **API密钥**：使用研究想法生成器和研究设计优化功能需要DeepSeek或Qwen的API密钥
2. **文件格式**：
   - 文献数据提取器支持TXT格式的文献
   - 研究设计优化功能支持TXT和PDF格式的参考论文
3. **网络连接**：需要稳定的网络连接以调用API
4. **响应时间**：API调用可能需要几秒钟时间，请耐心等待
5. **文献内容**：研究设计优化功能会自动限制参考论文内容为前30000字

## 扩展功能

用户可以通过以下方式扩展系统功能：

1. **添加新的提示词模板**：在`idea_generator/prompt_templates/`文件夹中添加新的提示词模板
2. **修改提取规则**：修改`extractors/extract_literature.py`中的提取规则，以适应不同格式的文献
3. **优化检索算法**：修改`retrievers/similarity_retriever.py`中的检索算法，以提高检索准确性

## 许可证

本项目采用MIT许可证。

## 联系方式

如有问题或建议，请联系项目维护者。