# 文献数据提取器

## 功能描述

此模块用于从指定文件夹及其所有子文件夹中提取所有TXT格式的文献数据，包括文献标题和正文前1000个字符的内容，并将其存储为JSON格式。

## 目录结构

```
literature_processor/
└── extractors/
    ├── __init__.py
    ├── extract_literature.py  # 主要提取脚本
    └── README.md             # 本文档
```

## 安装与依赖

本模块仅依赖Python标准库，无需额外安装依赖。

## 使用方法

### 命令行使用

```bash
python extract_literature.py [文件夹路径] [--output <输出JSON文件路径>]
```

参数说明：
- `[文件夹路径]`: 包含TXT文献的文件夹路径，默认为`文献数据`
- `--output`: 可选参数，指定输出JSON文件的路径，默认为`literature_data.json`

### 作为模块导入使用

```python
from extractors.extract_literature import extract_literature

# 使用默认路径（文献数据）提取数据并返回结果
result = extract_literature()

# 指定文件夹路径提取数据
result = extract_literature('path/to/literature/folder')

# 提取数据并保存到指定文件
extract_literature('path/to/literature/folder', 'output.json')

# 使用默认路径并保存到指定文件
extract_literature(output_json='output.json')
```

## 输出格式

输出的JSON文件格式如下：

```json
[
  {
    "title": "文献标题",
    "content": "文献正文前1000个字符...",
    "path": "文件的完整路径"
  },
  {
    "title": "另一篇文献标题",
    "content": "另一篇文献正文前1000个字符...",
    "path": "文件的完整路径"
  }
]
```

## 示例

假设我们有一个包含TXT文献的文件夹 `JFE202403`，我们可以这样使用：

```bash
python extract_literature.py ../../JFE文献数据/JFE202403 --output jfe_202403_data.json
```

这将提取 `JFE202403` 文件夹中的所有TXT文献，并将结果保存到 `jfe_202403_data.json` 文件中。

## 注意事项

1. 本模块会从文件名中提取标题，自动移除 `.txt` 后缀、年份信息（如 `_2024_` 或 `_2025_`）以及期刊名称，并将下划线替换为空格。
2. 对于无法读取的文件，会输出错误信息并跳过该文件。
3. 输出的JSON文件使用UTF-8编码，确保中文字符能正确显示。