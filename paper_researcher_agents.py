from textwrap import dedent
from crewai import Agent
from tools.arxiv_tools import ArxivTools

class PaperResearcherAgents:
    def patent_analyst_agent(self, llm):
        return Agent(
            role='專利分析專家',
            goal='分析專利文件，提取關鍵字',
            backstory=dedent("""\
                你是一位經驗豐富的專利分析專家。
                你熟悉專利文獻結構，擅長文本分析與關鍵資訊提取。
                你的任務是從專利文件中提取最相關和重要的關鍵字。"""),
            allow_delegation=False,
            verbose=True,
            llm=llm
        )

    def paper_search_specialist_agent(self, llm):
        return Agent(
            role='論文搜尋專家',
            goal='使用 arXiv API 搜尋相關論文',
            backstory=dedent("""\
                你是一位專業的論文搜尋專家。
                你熟悉 arXiv API 的使用，擅長數據處理與檢索。
                你的任務是使用提供的關鍵字在 arXiv 上搜尋相關論文。"""),
            tools=[ArxivTools.search_arxiv_papers, ArxivTools.get_paper_details],
            allow_delegation=False,
            verbose=True,
            llm=llm
        )

    def system_coordinator_agent(self, llm):
        return Agent(
            role='系統協調員',
            goal='協調整個工作流程，整合結果',
            backstory=dedent("""\
                你是一位經驗豐富的系統協調員。
                你具備專案管理經驗，能有效組織並整合資訊。
                你的任務是協調整個研究過程，確保各個環節順利進行並整合最終結果。"""),
            allow_delegation=True,
            verbose=True,
            llm=llm
        )
