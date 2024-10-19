from textwrap import dedent
from crewai import Task

class PoCTasks():
    def requirements_analysis_task(self, agent, solution_description):
        return Task(description=dedent(f"""
            基於以下解決方案描述,進行需求分析:
            {solution_description}

            你的任務是:
            1. 分析客戶提供的解決方案
            2. 確定 PoC 的具體目標和範圍
            3. 定義功能需求和非功能需求

            請提供一份詳細的需求分析報告。
            """),
            expected_output="詳細的需求分析報告,包括 PoC 的目標、範圍、功能需求和非功能需求。",
            agent=agent
        )

    def architecture_design_task(self, agent, requirements):
        return Task(description=dedent(f"""
            基於以下需求分析,設計 PoC 的架構:
            {requirements}

            你的任務是:
            1. 設計 PoC 的整體架構
            2. 選擇適當的技術堆疊
            3. 制定資料流程和介面規範

            請提供一份詳細的架構設計文件。
            """),
            expected_output="詳細的架構設計文件,包括整體架構、技術堆疊選擇、資料流程和介面規範。",
            agent=agent
        )

    def prototype_development_task(self, agent, architecture):
        return Task(description=dedent(f"""
            基於以下架構設計,開發 PoC 原型:
            {architecture}

            你的任務是:
            1. 實現 PoC 的核心功能
            2. 撰寫必要的程式碼
            3. 整合所需的第三方函式庫或服務

            請提供開發完成的 PoC 原型程式碼和說明。
            """),
            expected_output="PoC 原型程式碼和開發說明文件。",
            agent=agent
        )

    def testing_task(self, agent, prototype):
        return Task(description=dedent(f"""
            對以下 PoC 原型進行測試:
            {prototype}

            你的任務是:
            1. 設計測試案例
            2. 執行功能測試
            3. 進行效能和安全性測試

            請提供一份詳細的測試報告。
            """),
            expected_output="詳細的測試報告,包括測試案例、功能測試結果、效能和安全性測試結果。",
            agent=agent
        )

    def documentation_task(self, agent, poc_details):
        return Task(description=dedent(f"""
            為以下 PoC 撰寫文件:
            {poc_details}

            你的任務是:
            1. 撰寫技術文件
            2. 建立使用者指南
            3. 準備展示材料

            請提供完整的 PoC 文件包。
            """),
            expected_output="完整的 PoC 文件包,包括技術文件、使用者指南和展示材料。",
            agent=agent
        )

    def ui_design_task(self, agent, requirements):
        return Task(description=dedent(f"""
            基於以下需求,設計 PoC 的使用者介面:
            {requirements}

            你的任務是:
            1. 設計 PoC 的使用者介面
            2. 實現基本的互動功能

            請提供 UI 設計稿和互動說明。
            """),
            expected_output="UI 設計稿和互動說明文件。",
            agent=agent
        )

    def security_assessment_task(self, agent, poc_details):
        return Task(description=dedent(f"""
            對以下 PoC 進行安全評估:
            {poc_details}

            你的任務是:
            1. 進行安全漏洞掃描
            2. 提供安全強化建議

            請提供一份詳細的安全評估報告。
            """),
            expected_output="詳細的安全評估報告,包括漏洞掃描結果和安全強化建議。",
            agent=agent
        )

    def project_management_task(self, agent, project_details):
        return Task(description=dedent(f"""
            管理以下 PoC 專案:
            {project_details}

            你的任務是:
            1. 制定專案計畫和時程表
            2. 協調各個任務之間的相依關係
            3. 監控進度並解決問題

            請提供一份專案管理報告。
            """),
            expected_output="專案管理報告,包括專案計畫、時程表、任務相依關係和進度監控情況。",
            agent=agent
        )