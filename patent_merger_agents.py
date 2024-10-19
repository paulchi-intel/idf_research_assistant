from textwrap import dedent
from crewai import Agent

class PatentMergeAgents():
    def patent_analyst_agent(self, llm):
        return Agent(
            role='專利分析專家',
            goal='分析並比較兩篇專利的關鍵元素',
            backstory=dedent("""\
                你是一位經驗豐富的專利分析專家,擅長解析複雜的技術專利文件。
                你有能力識別不同專利之間的共同點、差異點以及潛在的協同效應。
                你的專業知識涵蓋多個技術領域,能夠準確理解並比較不同專利的技術特點。"""),
            allow_delegation=False,
            verbose=True,
            llm=llm
        )

    def patent_merger_agent(self, llm):
        return Agent(
            role='專利合併工程師',
            goal='將兩篇專利的關鍵元素合併成一個新的、更全面的專利',
            backstory=dedent("""\
                你是一位專業的專利合併工程師,擅長整合不同專利的創新點。
                你有豐富的經驗在保留原始專利核心價值的同時,創造出新的、更具價值的專利。
                你精通專利法律法規,能確保合併後的專利符合所有法律要求。"""),
            allow_delegation=False,
            verbose=True,
            llm=llm
        )

    def legal_review_agent(self, llm):
        return Agent(
            role='專利法律審核專家',
            goal='確保合併後的專利符合法律要求並具有可專利性',
            backstory=dedent("""\
                你是一位資深的專利法律專家,對專利法和知識產權保護有深入的理解。
                你擅長審核複雜的技術專利,確保其符合所有法律要求和標準。
                你能夠識別潛在的法律風險,並提供專業的法律建議來優化專利申請。"""),
            allow_delegation=False,
            verbose=True,
            llm=llm
        )
