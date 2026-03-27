import streamlit as st
import json
import os
import requests
import datetime
import PyPDF2

# 加载提示词模板
def load_prompt_templates():
    templates_dir = "literature_processor/idea_generator/prompt_templates"
    templates = {}
    for filename in os.listdir(templates_dir):
        if filename.endswith('.txt'):
            template_name = filename.replace('.txt', '')
            with open(os.path.join(templates_dir, filename), 'r', encoding='utf-8') as f:
                templates[template_name] = f.read()
    return templates

# 加载参考文献数据
def load_references(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    # 提取前5篇文献的摘要
    references = []
    for i, item in enumerate(data[:5]):
        title = item.get('title', '未知标题')
        content = item.get('content', '无摘要')
        references.append(f"[{i+1}] 标题: {title}\n摘要: {content}")
    return "\n\n".join(references)

# 调用DeepSeek API（流式）
def call_deepseek_api_stream(prompt, api_key):
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 8192,
        "stream": True
    }
    response = requests.post(url, headers=headers, json=data, stream=True)
    if response.status_code == 200:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                chunk_str = chunk.decode('utf-8')
                # 处理流式响应
                lines = chunk_str.split('\n')
                for line in lines:
                    line = line.strip()
                    if line.startswith('data: '):
                        line = line[6:]
                        if line == '[DONE]':
                            break
                        try:
                            data = json.loads(line)
                            if 'choices' in data and len(data['choices']) > 0:
                                delta = data['choices'][0].get('delta', {})
                                if 'content' in delta:
                                    yield delta['content']
                        except json.JSONDecodeError:
                            pass
    else:
        yield f"API调用失败: {response.text}"

# 调用Qwen API（流式）
def call_qwen_api_stream(prompt, api_key):
    # Qwen API目前不支持流式输出，使用非流式调用但模拟流式效果
    url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "qwen-plus",
        "input": prompt,
        "parameters": {
            "temperature": 0.7,
            "max_length": 8192
        }
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        content = response.json()['output']['text']
        # 模拟流式输出
        for i in range(0, len(content), 50):
            yield content[i:i+50]
    else:
        yield f"API调用失败: {response.text}"

# 保存对话记录
def save_conversation_history(user_idea, references, prompt, response, api_choice, template_choice):
    history_dir = "literature_processor/idea_generator/conversation_history"
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"conversation_{timestamp}.json"
    filepath = os.path.join(history_dir, filename)
    
    conversation = {
        "timestamp": timestamp,
        "user_idea": user_idea,
        "references": references,
        "prompt": prompt,
        "response": response,
        "api_choice": api_choice,
        "template_choice": template_choice
    }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(conversation, f, ensure_ascii=False, indent=2)
    
    return filepath

# 处理上传的文件（支持txt和pdf）
def process_uploaded_file(uploaded_file):
    if uploaded_file.name.endswith('.txt'):
        # 读取txt文件，限制为前30000字
        content = uploaded_file.getvalue().decode('utf-8', errors='ignore')
        return content[:30000]
    elif uploaded_file.name.endswith('.pdf'):
        # 读取pdf文件并转换为txt，限制为前30000字
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        content = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            content += page.extract_text()
            if len(content) >= 30000:
                break
        return content[:30000]
    else:
        return None

# 导入相似度检索器
from literature_processor.retrievers.similarity_retriever import SimilarityRetriever

# 主应用
st.set_page_config(
    page_title="研究想法生成器",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 添加自定义CSS，优化显示效果
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stTextArea textarea {
        font-size: 14px;
        line-height: 1.5;
    }
    .stMarkdown {
        font-size: 14px;
        line-height: 1.6;
    }
    .stSubheader {
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }
    .idea-card {
        background-color: #f9f9f9;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .streaming-output {
        background-color: #f0f0f0;
        border-radius: 8px;
        padding: 1rem;
        font-family: monospace;
        white-space: pre-wrap;
        word-wrap: break-word;
        line-height: 1.5;
    }
    .reference-card {
        background-color: #f5f5f5;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
        border-left: 4px solid #3498db;
    }
    .tab-content {
        padding: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# 创建标签页
tab1, tab2, tab3 = st.tabs(["🔍 相似文献检索", "🧠 研究想法生成", "📋 研究设计优化"])

# 相似文献检索标签页
with tab1:
    st.title("🔍 相似文献检索")
    st.info("基于您的研究想法，检索英文顶刊中的相似文献。")
    
    # 输入研究想法
    search_query = st.text_area("💡 输入您的研究想法", height=150, help="请用英文描述您的研究想法，以便检索英文顶刊文献")
    
    # 选择检索数量
    top_k = st.slider("选择返回的文献数量", min_value=1, max_value=10, value=5)
    
    # 检索按钮
    if st.button("🔎 开始检索", type="primary"):
        if not search_query:
            st.error("请输入研究想法")
        else:
            try:
                # 初始化检索器
                retriever = SimilarityRetriever()
                retriever.load_data("literature_data.json")
                
                # 执行检索
                with st.spinner("正在检索相似文献..."):
                    results = retriever.retrieve_similar(search_query, top_k=top_k)
                
                # 显示结果
                st.success(f"找到 {len(results)} 篇相似文献")
                
                # 保存结果为JSON
                import json
                results_json = json.dumps(results, ensure_ascii=False, indent=2)
                
                # 提供JSON下载
                st.download_button(
                    label="📥 下载检索结果 (JSON)",
                    data=results_json,
                    file_name="similarity_search_results.json",
                    mime="application/json"
                )
                
                # 显示检索结果
                for i, result in enumerate(results):
                    with st.container():
                        st.subheader(f"文献 {i+1}")
                        st.markdown(f"""<div class='reference-card'>
                            <p><strong>标题</strong>：{result['title']}</p>
                            <p><strong>路径</strong>：{result['path']}</p>
                            <p><strong>摘要预览</strong>：{result['content'][:1000]}...</p>
                        </div>""", unsafe_allow_html=True)
                        
                        # 提供原始TXT文件下载
                        if os.path.exists(result['path']):
                            with open(result['path'], 'r', encoding='utf-8', errors='ignore') as f:
                                txt_content = f.read()
                            st.download_button(
                                label=f"📥 下载原始TXT文件 - {result['title']}",
                                data=txt_content,
                                file_name=f"{result['title']}.txt",
                                mime="text/plain"
                            )
                        else:
                            st.warning(f"原始文件不存在: {result['path']}")
                
            except Exception as e:
                st.error(f"检索出错: {str(e)}")

# 研究想法生成标签页
with tab2:
    st.title("🧠 研究想法生成")

# 研究设计优化标签页
with tab3:
    st.title("📋 研究设计优化")
    st.info("基于您的研究想法和上传的参考论文，优化并完善研究设计，确保符合英文顶刊的标准。")
    
    # 输入研究想法
    research_idea = st.text_area("💡 输入您的研究想法", height=150, help="请详细描述您的研究想法，包括研究问题、研究背景等")
    
    # 上传参考论文
    uploaded_paper = st.file_uploader("📄 上传参考论文 (支持txt或pdf格式)", type=["txt", "pdf"])
    
    # 选择是否包含详细描述性统计设计
    include_descriptive_stats = st.checkbox("包含详细描述性统计设计", value=True)
    
    # 选择API
    api_choice_design = st.selectbox(
        "选择API",
        ["DeepSeek", "Qwen"]
    )
    
    # 输入API密钥
    api_key_design = st.text_input("输入API密钥", type="password")
    
    # 优化按钮
    if st.button("✨ 优化研究设计", type="primary"):
        if not api_key_design:
            st.error("请输入API密钥")
        elif not uploaded_paper:
            st.error("请上传参考论文")
        elif not research_idea:
            st.error("请输入研究想法")
        else:
            try:
                # 处理上传的文件
                reference_paper = process_uploaded_file(uploaded_paper)
                if reference_paper is None:
                    st.error("不支持的文件格式，请上传txt或pdf格式的文件")
                    # 跳过后续处理
                    pass
                else:
                    # 加载研究设计优化提示词模板
                    templates = load_prompt_templates()
                    prompt_template = templates.get("6_研究设计优化型", "")
                    
                    # 填充提示词模板
                    if include_descriptive_stats:
                        descriptive_stats_section = "详细描述性统计设计"
                    else:
                        descriptive_stats_section = "描述性统计（简要）"
                    
                    prompt = prompt_template.format(
                        user_idea=research_idea,
                        reference_paper=reference_paper,
                        include_descriptive_stats="是" if include_descriptive_stats else "否",
                        descriptive_stats_section=descriptive_stats_section
                    )
                    
                    # 创建流式输出区域
                    st.info("正在优化研究设计...")
                    streaming_container = st.empty()
                    full_response = ""
                    
                    # 调用流式API
                    if api_choice_design == "DeepSeek":
                        for chunk in call_deepseek_api_stream(prompt, api_key_design):
                            full_response += chunk
                            streaming_container.markdown(f"<div class='streaming-output'>{full_response}</div>", unsafe_allow_html=True)
                    else:
                        for chunk in call_qwen_api_stream(prompt, api_key_design):
                            full_response += chunk
                            streaming_container.markdown(f"<div class='streaming-output'>{full_response}</div>", unsafe_allow_html=True)
                    
                    # 保存对话记录
                    history_file = save_conversation_history(
                        user_idea=research_idea,
                        references=reference_paper[:1000] + "..." if len(reference_paper) > 1000 else reference_paper,
                        prompt=prompt,
                        response=full_response,
                        api_choice=api_choice_design,
                        template_choice="6_研究设计优化型"
                    )
                    st.success(f"对话记录已保存到：{history_file}")
                    
                    # 清除流式输出
                    streaming_container.empty()
                    
                    # 显示结果
                    st.success("研究设计优化成功！")
                    # 直接以Markdown格式显示结果
                    st.markdown(f"""<div class='idea-card'>{full_response}</div>""", unsafe_allow_html=True)
                

                    
            except Exception as e:
                st.error(f"处理文件时出错: {str(e)}")
                import traceback
                traceback.print_exc()

# 加载提示词模板
templates = load_prompt_templates()

# 侧边栏设置
st.sidebar.title("⚙️ 设置")

# 选择API
api_choice = st.sidebar.selectbox(
    "选择API",
    ["DeepSeek", "Qwen"]
)

# 输入API密钥
api_key = st.sidebar.text_input("输入API密钥", type="password")

# 选择提示词模板
template_choice = st.sidebar.selectbox(
    "选择提示词模板",
    list(templates.keys())
)

# 选择是否只依据摘要
only_abstract = st.sidebar.checkbox("只依据摘要进行研究想法判断", value=True)

# 上传JSON文件
uploaded_file = st.file_uploader("📁 上传包含参考文献的JSON文件", type="json")

# 输入研究想法
user_idea = st.text_area("💡 输入你的研究想法", height=200, help="请详细描述你的研究想法，包括研究问题、研究背景等")

# 生成按钮
if st.button("🚀 生成研究想法", type="primary"):
    if not api_key:
        st.error("请输入API密钥")
    elif not uploaded_file:
        st.error("请上传包含参考文献的JSON文件")
    elif not user_idea:
        st.error("请输入研究想法")
    else:
        # 读取上传的文件
        try:
            # 保存上传的文件
            with open("temp_references.json", "wb") as f:
                f.write(uploaded_file.getvalue())
            
            # 加载参考文献
            references = load_references("temp_references.json")
            
            # 加载提示词模板
            prompt_template = templates[template_choice]
            
            # 填充提示词模板
            prompt = prompt_template.format(
                user_idea=user_idea,
                references=references
            )
            
            # 创建流式输出区域
            st.info("正在生成研究想法...")
            streaming_container = st.empty()
            full_response = ""
            
            # 调用流式API
            if api_choice == "DeepSeek":
                for chunk in call_deepseek_api_stream(prompt, api_key):
                    full_response += chunk
                    streaming_container.markdown(f"<div class='streaming-output'>{full_response}</div>", unsafe_allow_html=True)
            else:
                for chunk in call_qwen_api_stream(prompt, api_key):
                    full_response += chunk
                    streaming_container.markdown(f"<div class='streaming-output'>{full_response}</div>", unsafe_allow_html=True)
            
            # 保存对话记录
            history_file = save_conversation_history(
                user_idea=user_idea,
                references=references,
                prompt=prompt,
                response=full_response,
                api_choice=api_choice,
                template_choice=template_choice
            )
            st.success(f"对话记录已保存到：{history_file}")
            
            # 清除流式输出
            streaming_container.empty()
            
            # 显示结果
            st.success("研究想法生成成功！")
            # 直接以Markdown格式显示结果
            st.markdown(f"""<div class='idea-card'>{full_response}</div>""", unsafe_allow_html=True)
                    
        except Exception as e:
            st.error(f"处理文件时出错: {str(e)}")
        finally:
            # 清理临时文件
            if os.path.exists("temp_references.json"):
                os.remove("temp_references.json")