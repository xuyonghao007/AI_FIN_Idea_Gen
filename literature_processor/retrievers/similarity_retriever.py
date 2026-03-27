import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class SimilarityRetriever:
    """
    基于TF-IDF和余弦相似度的文献检索器
    """
    
    def __init__(self, literature_data=None):
        """
        初始化检索器
        
        Args:
            literature_data (list, optional): 文献数据列表。如果为None，需要后续调用load_data加载
        """
        self.literature_data = literature_data
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = None
        
        if literature_data:
            self._fit()
    
    def load_data(self, data_path):
        """
        从JSON文件加载文献数据
        
        Args:
            data_path (str): JSON文件路径
        """
        with open(data_path, 'r', encoding='utf-8') as f:
            self.literature_data = json.load(f)
        self._fit()
    
    def _fit(self):
        """
        构建TF-IDF矩阵
        """
        if not self.literature_data:
            raise ValueError("No literature data loaded. Please load data first.")
        
        # 提取所有文献的内容
        contents = [item['content'] for item in self.literature_data]
        # 构建TF-IDF矩阵
        self.tfidf_matrix = self.vectorizer.fit_transform(contents)
    
    def retrieve_similar(self, query, top_k=5):
        """
        根据查询文本检索最相似的文献
        
        Args:
            query (str): 查询文本
            top_k (int): 返回的最相似文献数量，默认为5
        
        Returns:
            list: 包含最相似文献的列表，每个元素为包含'title'、'content'、'path'和'score'的字典
        """
        if self.tfidf_matrix is None:
            raise ValueError("No TF-IDF matrix built. Please load data first.")
        
        # 将查询文本转换为TF-IDF向量
        query_vector = self.vectorizer.transform([query])
        # 计算余弦相似度
        similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        
        # 获取最相似的top_k个文献的索引
        top_indices = similarities.argsort()[-top_k:][::-1]
        
        # 构建结果列表
        results = []
        for idx in top_indices:
            result = {
                'title': self.literature_data[idx]['title'],
                'content': self.literature_data[idx]['content'],
                'path': self.literature_data[idx]['path'],
                'score': float(similarities[idx])
            }
            results.append(result)
        
        return results
    
    def save_results(self, results, output_path):
        """
        保存检索结果到JSON文件
        
        Args:
            results (list): 检索结果列表
            output_path (str): 输出JSON文件路径
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"检索结果已保存到 {output_path}")

if __name__ == "__main__":
    # 示例用法
    import argparse
    
    parser = argparse.ArgumentParser(description='基于相似度检索文献')
    parser.add_argument('data_path', help='文献数据JSON文件路径')
    parser.add_argument('query', help='查询文本')
    parser.add_argument('--top_k', type=int, default=5, help='返回的最相似文献数量')
    parser.add_argument('--output', help='输出JSON文件路径', default='retrieval_results.json')
    
    args = parser.parse_args()
    
    # 初始化检索器并加载数据
    retriever = SimilarityRetriever()
    retriever.load_data(args.data_path)
    
    # 执行检索
    results = retriever.retrieve_similar(args.query, args.top_k)
    
    # 保存结果
    retriever.save_results(results, args.output)
    
    # 打印结果
    print(f"\n检索结果（前{args.top_k}个最相似文献）：")
    for i, result in enumerate(results):
        print(f"\n{i+1}. 相似度: {result['score']:.4f}")
        print(f"标题: {result['title']}")
        print(f"路径: {result['path']}")
        print(f"内容预览: {result['content'][:100]}...")