# 文献相似度检索器

## 功能描述

此模块用于基于TF-IDF和余弦相似度对文献进行相似度检索。用户可以输入一个查询文本，系统会返回最相似的5篇文献（可自定义数量），并将结果保存为JSON格式。

## 目录结构

```
literature_processor/
└── retrievers/
    ├── __init__.py
    ├── similarity_retriever.py  # 主要检索脚本
    └── README.md             # 本文档
```

## 依赖

本模块依赖以下库：
- Python 3.6+
- scikit-learn

## 安装依赖

```bash
pip install scikit-learn
```

## 使用方法

### 命令行使用

```bash
python similarity_retriever.py <文献数据JSON文件路径> <查询文本> [--top_k <返回数量>] [--output <输出JSON文件路径>]
```

参数说明：
- `<文献数据JSON文件路径>`: 包含文献数据的JSON文件路径
- `<查询文本>`: 用于检索相似文献的查询文本
- `--top_k`: 可选参数，返回的最相似文献数量，默认为5
- `--output`: 可选参数，指定输出JSON文件的路径，默认为`retrieval_results.json`

### 作为模块导入使用

```python
from retrievers.similarity_retriever import SimilarityRetriever

# 初始化检索器并加载数据
retriever = SimilarityRetriever()
retriever.load_data('path/to/literature_data.json')

# 执行检索
query = "corporate investment and uncertainty"
results = retriever.retrieve_similar(query, top_k=5)

# 保存结果
retriever.save_results(results, 'retrieval_results.json')

# 打印结果
for i, result in enumerate(results):
    print(f"\n{i+1}. 相似度: {result['score']:.4f}")
    print(f"标题: {result['title']}")
    print(f"路径: {result['path']}")
    print(f"内容预览: {result['content'][:100]}...")
```

## 输出格式

输出的JSON文件格式如下：

```json
[
  {
    "title": "文献标题",
    "content": "文献正文前1000个字符...",
    "path": "文件的完整路径",
    "score": 0.95
  },
  {
    "title": "另一篇文献标题",
    "content": "另一篇文献正文前1000个字符...",
    "path": "文件的完整路径",
    "score": 0.87
  }
]
```

## 示例

假设我们有一个包含文献数据的JSON文件 `literature_data.json`，我们可以这样使用：

```bash
python similarity_retriever.py literature_data.json "corporate investment and uncertainty" --top_k 5 --output results.json
```

这将检索与"corporate investment and uncertainty"最相似的5篇文献，并将结果保存到 `results.json` 文件中。

## 算法说明

本模块使用以下算法：
1. **TF-IDF (Term Frequency-Inverse Document Frequency)**：用于将文本转换为数值向量
2. **余弦相似度**：用于计算查询文本与文献内容之间的相似度

这种方法简单有效，能够快速找到与查询文本最相关的文献。