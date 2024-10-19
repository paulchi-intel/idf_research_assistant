import streamlit as st
import os
from dotenv import load_dotenv
from crewai import Crew, Agent, Task
from langchain_openai import AzureChatOpenAI
from poc_builder_tasks import PoCTasks
from poc_builder_agents import PoCAgents

load_dotenv()

# 設定 Azure OpenAI
default_llm = AzureChatOpenAI(
    openai_api_version=os.environ.get("AZURE_OPENAI_VERSION", "2023-07-01-preview"),
    azure_deployment=os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt35"),
    azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT", "https://<your-endpoint>.openai.azure.com/"),
    api_key=os.environ.get("AZURE_OPENAI_KEY")
)

tasks = PoCTasks()
agents = PoCAgents()

def poc_builder_app():
    st.header("PoC(Proof of Concept)產生器")

    # 輸入解決方案描述
    solution_description = st.text_area("請輸入解決方案的描述:", height=200)

    if st.button("開始產生 PoC"):
        if solution_description:
            # 建立代理人
            requirements_analyst = agents.requirements_analyst(llm=default_llm)
            architect = agents.architect(llm=default_llm)
            developer = agents.developer(llm=default_llm)
            qa_engineer = agents.qa_engineer(llm=default_llm)
            project_manager = agents.project_manager(llm=default_llm)
            security_expert = agents.security_expert(llm=default_llm)
            ux_designer = agents.ux_designer(llm=default_llm)
            technical_writer = agents.technical_writer(llm=default_llm)

            # 執行任務
            with st.spinner('正在進行需求分析...'):
                requirements_task = tasks.requirements_analysis_task(requirements_analyst, solution_description)
                requirements_crew = Crew(agents=[requirements_analyst], tasks=[requirements_task], verbose=True)
                requirements_output = requirements_crew.kickoff()
                st.session_state.requirements = str(requirements_output)
            
            with st.expander("需求分析詳細過程", expanded=False):
                st.write(st.session_state.requirements)

            with st.spinner('正在設計架構...'):
                architecture_task = tasks.architecture_design_task(architect, st.session_state.requirements)
                architecture_crew = Crew(agents=[architect], tasks=[architecture_task], verbose=True)
                architecture_output = architecture_crew.kickoff()
                st.session_state.architecture = str(architecture_output)
            
            with st.expander("架構設計詳細過程", expanded=False):
                st.write(st.session_state.architecture)

            with st.spinner('正在開發原型...'):
                prototype_task = tasks.prototype_development_task(developer, st.session_state.architecture)
                prototype_crew = Crew(agents=[developer], tasks=[prototype_task], verbose=True)
                prototype_output = prototype_crew.kickoff()
                st.session_state.prototype = str(prototype_output)
            
            with st.expander("原型開發詳細過程", expanded=False):
                st.write(st.session_state.prototype)

            with st.spinner('正在進行測試...'):
                testing_task = tasks.testing_task(qa_engineer, st.session_state.prototype)
                testing_crew = Crew(agents=[qa_engineer], tasks=[testing_task], verbose=True)
                testing_output = testing_crew.kickoff()
                st.session_state.testing = str(testing_output)
            
            with st.expander("測試詳細過程", expanded=False):
                st.write(st.session_state.testing)

            with st.spinner('正在撰寫文件...'):
                documentation_task = tasks.documentation_task(technical_writer, st.session_state.prototype)
                documentation_crew = Crew(agents=[technical_writer], tasks=[documentation_task], verbose=True)
                documentation_output = documentation_crew.kickoff()
                st.session_state.documentation = str(documentation_output)
            
            with st.expander("文件撰寫詳細過程", expanded=False):
                st.write(st.session_state.documentation)

            # 顯示結果
            st.subheader("需求分析")
            st.markdown(st.session_state.requirements)

            st.subheader("架構設計")
            st.markdown(st.session_state.architecture)

            st.subheader("原型開發")
            st.markdown(st.session_state.prototype)

            st.subheader("測試報告")
            st.markdown(st.session_state.testing)

            st.subheader("文件")
            st.markdown(st.session_state.documentation)

            # 儲存 PoC 文件
            import datetime
            current_time = datetime.datetime.now()
            file_name = f"poc_{current_time.strftime('%Y%m%d_%H%M%S')}.md"
            
            # 建立 .\poc 資料夾（如果不存在）
            poc_folder = os.path.join('.', 'poc')
            os.makedirs(poc_folder, exist_ok=True)
            
            # 將文件儲存到 .\poc 資料夾
            file_path = os.path.join(poc_folder, file_name)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("# PoC (概念驗證) 文件\n\n")
                f.write("## 需求分析\n")
                f.write(st.session_state.requirements + "\n\n")
                f.write("## 架構設計\n")
                f.write(st.session_state.architecture + "\n\n")
                f.write("## 原型開發\n")
                f.write(st.session_state.prototype + "\n\n")
                f.write("## 測試報告\n")
                f.write(st.session_state.testing + "\n\n")
                f.write("## 文件\n")
                f.write(st.session_state.documentation)
            st.success(f"PoC 文件已儲存為: {file_path}")
        else:
            st.error("請輸入解決方案描述")

if __name__ == "__main__":
    poc_builder_app()
