from textwrap import dedent
from crewai import Task

class PaperResearcherTasks:
    def extract_keywords_task(self, agent, patent_content, num_keywords):
        return Task(
            description=dedent(f"""
                分析以下專利文件，提取 {num_keywords} 個最重要的關鍵字：

                {patent_content}

                你的任務是：
                1. 解析專利文獻的結構
                2. 識別專利中的重要部分
                3. 提取並優化 {num_keywords} 個關鍵字列表

                請提供一個包含 {num_keywords} 個關鍵字的列表，每個關鍵字都應該與專利的核心內容高度相關。
            """),
            expected_output=f"一個包含 {num_keywords} 個與專利核心內容高度相關的關鍵字列表。",
            agent=agent
        )

    def search_papers_task(self, agent, keywords):
        return Task(
            description=dedent(f"""
                使用以下關鍵字在 arXiv 上搜尋相關論文：

                {', '.join(keywords)}

                你的任務是：
                1. 使用 arXiv API 進行搜索
                2. 處理並過濾搜尋結果
                3. 提供最相關的 5 篇論文的摘要和連結

                請確保搜尋結果與提供的關鍵字高度相關。
            """),
            expected_output="最相關的 5 篇論文的摘要和連結列表。",
            agent=agent
        )

    def coordinate_research_task(self, agent, patent_content, keywords, papers):
        return Task(
            description=dedent(f"""
                協調整個研究過程，整合專利分析和論文搜索的結果。

                專利內容：
                {patent_content}

                提取的關鍵字：
                {keywords}

                搜索到的論文：
                {papers}

                你的任務是：
                1. 審查專利內容和提取的關鍵字
                2. 分析搜索到的論文，確保它們與專利內容相關
                3. 整合所有信息，生成一份綜合研究報告
                4. 報告應包括：專利摘要、關鍵字分析、相關論文摘要、專利與論文的關聯性分析

                請確保研究報告清晰、準確，並突出專利與相關論文之間的聯繫。
            """),
            expected_output="一份完整的研究報告，包含專利分析、關鍵字、相關論文摘要和綜合分析。",
            agent=agent
        )
