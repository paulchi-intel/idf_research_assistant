from textwrap import dedent
from crewai import Task

class PatentTasks():
    def generate_ideas_task(self, agent):
        return Task(description=dedent(f"""
            作為專注於{agent.role.split(' ')[-3]}的ODM專案經理,請為AI PC生成三個創新和前瞻性的功能創意。
            這些創意應該專注於提升AI PC的{agent.role.split(' ')[-3]}。
            每個創意應該包括:
            - 創意名稱
            - 簡短描述 (著重於如何優化{agent.role.split(' ')[-3]})
            - 潛在用戶場景 (展示{agent.role.split(' ')[-3]}如何改善用戶體驗)
            - 市場需求分析 (強調{agent.role.split(' ')[-3]}在市場中的重要性)

            請確保這些創意具有前瞻性、未來性和市場性,並且直接關聯到{agent.role.split(' ')[-3]}。
            """),
            expected_output=f"三個詳細的AI PC {agent.role.split(' ')[-3]}功能創意,每個創意包括名稱、描述、用戶場景和市場分析。",
            agent=agent
        )

    def generate_solutions_task(self, agent, idea):
        return Task(description=dedent(f"""
            基於以下選定的AI PC創意,生成三個優化{agent.role.split(' ')[-5]}的解決方案:

            選定創意:
            ------------
            {idea}

            每個解決方案應包括:
            1. 解決方案名稱
            2. 技術描述
            3. {agent.role.split(' ')[-5]}優化策略
            4. AI和LLM技術的應用

            請確保解決方案既創新又實用,特別關注AI和LLM技術的應用。
            """),
            expected_output=f"三個詳細的解決方案,每個包括名稱、技術描述、{agent.role.split(' ')[-3]}優化策略和AI應用。",
            agent=agent
        )

    def create_patent_task(self, agent, idea, solution):
        return Task(description=dedent(f"""
            基於以下選定的AI PC創意和解決方案,創建一份完整的專利申請文檔:

            選定創意:
            ------------
            {idea}

            選定解決方案:
            ------------
            {solution}

            請按照以下格式創建專利文檔:
            1. 發明名稱
            2. 技術背景
            3. 發明概述
            4. 系統架構
            5. 可檢測性
            6. 發明詳情
            確保文檔涵蓋所有必要的技術細節和法律要求,並突出創新點和技術優勢。
            """),
            expected_output="完整的專利申請文檔,包含所有必要的章節和詳細信息。",
            agent=agent
        )
''' 
1. TITLE OF THE INVENTION 
2. TECHNOLOGY BACKGROUND
3. OVERVIEW OF THE INVENTION
4. SYSTEM ARCHITECTURE
5. DETECTABILITY
6. DETAILS OF THE INVENTION
'''   
