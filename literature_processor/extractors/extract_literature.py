import os
import json

def extract_literature(folder_path="文献数据", output_json=None):
    """
    提取指定文件夹及其子文件夹中所有TXT文献的标题和前1000个字符的内容
    
    Args:
        folder_path (str, optional): 包含TXT文献的文件夹路径，默认为"文献数据"
        output_json (str, optional): 输出JSON文件的路径。如果不指定，将返回结果
    
    Returns:
        list: 包含文献信息的列表，每个元素为包含'title'和'content'的字典
    """
    literature_data = []
    
    # 递归遍历文件夹及其子文件夹
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            if filename.endswith('.txt'):
                file_path = os.path.join(root, filename)
                
                # 从文件名提取标题（去掉后缀和年份信息）
                title = filename.replace('.txt', '')
                # 移除年份和期刊信息
                if '_2024_' in title:
                    title = title.split('_2024_')[0]
                elif '_2025_' in title:
                    title = title.split('_2025_')[0]
                # 将下划线替换为空格
                title = title.replace('_', ' ')
                
                # 读取文件内容，提取前1000个字符
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        content = content[:2000]  # 提取前1000个字符
                except Exception as e:
                    print(f"读取文件 {filename} 时出错: {e}")
                    content = ""
                
                # 添加到结果列表
                literature_data.append({
                    'title': title,
                    'content': content,
                    'path': file_path
                })
    
    # 如果指定了输出文件，写入JSON
    if output_json:
        with open(output_json, 'w', encoding='utf-8') as f:
            json.dump(literature_data, f, ensure_ascii=False, indent=2)
        print(f"已成功提取 {len(literature_data)} 篇文献到 {output_json}")
    
    return literature_data

if __name__ == "__main__":
    # 示例用法
    import argparse
    
    parser = argparse.ArgumentParser(description='提取文献数据并存储为JSON')
    parser.add_argument('folder', nargs='?', default="文献数据", help='包含TXT文献的文件夹路径，默认为"文献数据"')
    parser.add_argument('--output', help='输出JSON文件路径', default='literature_data.json')
    
    args = parser.parse_args()
    extract_literature(args.folder, args.output)