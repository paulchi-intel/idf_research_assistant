from textwrap import dedent
from crewai import Task

class PatentMergeTasks():
    def analyze_patents_task(self, agent, patent1, patent2):
        return Task(
            description=dedent(f"""
                分析以下兩篇專利文件:

                專利1:
                ------------
                {patent1}

                專利2:
                ------------
                {patent2}

                請完成以下任務:
                1. 識別兩篇專利的主要創新點和技術特徵
                2. 比較兩篇專利的異同點
                3. 找出可能的協同效應和整合機會
                4. 提出初步的合併建議

                輸出應包含詳細的分析報告,突出關鍵發現和建議。
                """),
            expected_output="詳細的專利分析報告，包括兩篇專利的主要創新點、技術特徵、異同點、潛在協同效應和初步合併建議。",
            agent=agent
        )

    def merge_patents_task(self, agent, analysis_report):
        return Task(
            description=dedent(f"""
                基於以下專利分析報告,創建一份新的、整合的專利文檔:

                分析報告:
                ------------
                {analysis_report}

                請完成以下任務:
                1. 創建一個新的專利標題,反映整合後的創新
                2. 撰寫一份綜合的技術背景部分
                3. 描述整合後的發明概述,突出主要創新點
                4. 詳細說明整合後的系統架構和技術細節
                5. 闡述新專利的優勢和潛在應用

                確保新的專利文檔保留了原始專利的核心價值,同時創造出新的協同效應。
                """),
            expected_output="一份完整的、整合後的新專利文檔，包括新的專利標題、技術背景、發明概述、系統架構、技術細節、優勢和潛在應用。",
            agent=agent
        )

    def legal_review_task(self, agent, merged_patent):
        return Task(
            description=dedent(f"""
                審核以下合併後的專利文檔:

                合併專利:
                ------------
                {merged_patent}

                請完成以下任務:
                1. 評估專利的可專利性
                2. 檢查是否符合所有法律要求和標準
                3. 識別潛在的法律風險或衝突
                4. 提供優化建議以增強專利的法律保護

                輸出應包含詳細的法律審核報告,包括任何需要修改或改進的地方。
                """),
            expected_output="詳細的法律審核報告，包括專利的可專利性評估、法律合規性檢查結果、潛在風險識別和優化建議。",
            agent=agent
        )
