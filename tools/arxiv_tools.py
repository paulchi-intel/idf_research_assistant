import os
import requests
import urllib.parse
from dotenv import load_dotenv
from langchain.tools import tool
import arxiv

load_dotenv()

class ArxivTools:
    @tool("Search arXiv Papers")
    def search_arxiv_papers(query, max_results=10):
        """
        用於搜索arXiv上的論文。
        輸入應為搜索查詢字符串。
        """
        search = arxiv.Search(
            query = query,
            max_results = max_results,
            sort_by = arxiv.SortCriterion.Relevance,
            sort_order = arxiv.SortOrder.Descending
        )

        results = []
        for result in search.results():
            paper_info = {
                "標題": result.title,
                "作者": ', '.join(author.name for author in result.authors),
                "摘要": result.summary[:200] + "...",  # 只返回前200個字符
                "URL": result.entry_id
            }
            results.append(paper_info)

        return results

    @tool("Get Paper Details")
    def get_paper_details(paper_id):
        """
        用於獲取指定arXiv論文的詳細信息。
        輸入應為arXiv論文ID。
        """
        search = arxiv.Search(id_list=[paper_id])
        try:
            paper = next(search.results())
            return {
                "標題": paper.title,
                "作者": ', '.join(author.name for author in paper.authors),
                "摘要": paper.summary,
                "URL": paper.entry_id,
                "發布日期": paper.published.strftime("%Y-%m-%d"),
                "分類": ', '.join(paper.categories)
            }
        except StopIteration:
            return f"無法找到ID為 '{paper_id}' 的論文。"

# 使用示例
if __name__ == "__main__":
    keyword = "quantum computing"
    print(ArxivTools.search_arxiv_papers(keyword))
    print(ArxivTools.get_paper_details("2208.00733v1"))  # 替換為實際的論文ID
