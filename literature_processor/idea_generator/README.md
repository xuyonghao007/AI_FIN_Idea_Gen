# 研究想法生成器

## 功能描述

此模块用于基于用户提出的研究想法和参考的顶刊文献摘要，生成具有理论突破的研究想法。它使用Streamlit构建了一个交互式界面，支持用户选择不同的API（DeepSeek或Qwen）和提示词模板，生成3个高质量的研究想法。

## 目录结构

```
literature_processor/
└── idea_generator/
    ├── __init__.py
    ├── app.py                # Streamlit应用主文件
    ├── README.md             # 本文档
    └── prompt_templates/     # 提示词模板文件夹
        ├── 1_理论拓展型.txt
        ├── 2_方法创新型.txt
        ├── 3_实证拓展型.txt
        ├── 4_跨学科融合型.txt
        └── 5_政策启示型.txt
```

## 依赖

本模块依赖以下库：
- Python 3.6+
- streamlit
- requests

## 安装依赖

```bash
pip install streamlit requests
```

## 使用方法

1. **启动应用**：
   ```bash
   streamlit run literature_processor/idea_generator/app.py
   ```

2. **配置设置**：
   - 在侧边栏选择API（DeepSeek或Qwen）
   - 输入API密钥
   - 选择提示词模板
   - 选择是否只依据摘要进行研究想法判断

3. **上传数据**：
   - 上传包含参考文献的JSON文件（格式与`test_retrieval_results.json`相同）

4. **输入研究想法**：
   - 在文本框中输入你的研究想法

5. **生成研究想法**：
   - 点击"生成研究想法"按钮
   - 等待API响应，生成3个研究想法

## 提示词模板

本模块提供了5个不同类型的提示词模板，用于生成不同类型的研究想法：

1. **理论拓展型**：基于现有理论进行深度拓展和创新
2. **方法创新型**：开发和应用新的研究方法
3. **实证拓展型**：基于新的数据来源或处理方法进行实证研究
4. **跨学科融合型**：融合不同学科的理论或方法
5. **政策启示型**：分析政策影响和提出政策建议

## 输出格式

生成的研究想法包含以下部分：
- 研究问题
- 突破点（理论拓展点/方法创新点/实证拓展点/跨学科融合点/政策启示点）
- 研究设计
- 预期贡献

## 示例

1. **启动应用**：
   ```bash
   streamlit run literature_processor/idea_generator/app.py
   ```

2. **配置设置**：
   - 选择API：DeepSeek
   - 输入API密钥：your_api_key
   - 选择提示词模板：理论拓展型
   - 勾选"只依据摘要进行研究想法判断"

3. **上传数据**：
   - 上传`test_retrieval_results.json`文件

4. **输入研究想法**：
   - "研究企业社会责任对公司价值的影响"

5. **生成研究想法**：
   - 点击"生成研究想法"按钮
   - 等待API响应，查看生成的3个研究想法

## 注意事项

1. **API密钥**：用户需要自行获取DeepSeek或Qwen的API密钥
2. **JSON文件格式**：上传的JSON文件必须包含`title`和`content`字段
3. **网络连接**：需要稳定的网络连接以调用API
4. **响应时间**：API调用可能需要几秒钟时间，请耐心等待

## 扩展功能

用户可以通过在`prompt_templates`文件夹中添加新的提示词模板来扩展本模块的功能，生成不同类型的研究想法。