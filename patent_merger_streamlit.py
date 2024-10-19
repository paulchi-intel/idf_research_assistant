import streamlit as st
import os
from dotenv import load_dotenv
from crewai import Crew, Agent, Task
from langchain_openai import AzureChatOpenAI
from patent_merger_tasks import PatentMergeTasks
from patent_merger_agents import PatentMergeAgents

load_dotenv()

# 設置 Azure OpenAI
default_llm = AzureChatOpenAI(
    openai_api_version=os.environ.get("AZURE_OPENAI_VERSION", "2023-07-01-preview"),
    azure_deployment=os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt35"),
    azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT", "https://<your-endpoint>.openai.azure.com/"),
    api_key=os.environ.get("AZURE_OPENAI_KEY")
)

tasks = PatentMergeTasks()
agents = PatentMergeAgents()

def patent_merger_app():
    st.header("IDF合併工具")

    # 上傳兩個IDF文件
    idf1 = st.file_uploader("上傳第一個IDF文件", type=["txt", "md"])
    idf2 = st.file_uploader("上傳第二個IDF文件", type=["txt", "md"])

    if idf1 and idf2:
        idf1_content = idf1.getvalue().decode("utf-8")
        idf2_content = idf2.getvalue().decode("utf-8")

        # 顯示上傳的IDF內容
        with st.expander("查看第一個IDF內容"):
            st.text_area("IDF 1 內容", idf1_content, height=300)
        
        with st.expander("查看第二個IDF內容"):
            st.text_area("IDF 2 內容", idf2_content, height=300)

        # 開始合併流程
        if st.button("開始合併IDF"):
            # 創建代理
            patent_analyst = agents.patent_analyst_agent(llm=default_llm)
            patent_merger = agents.patent_merger_agent(llm=default_llm)
            legal_reviewer = agents.legal_review_agent(llm=default_llm)

            # 第一階段：分析IDF
            with st.spinner('正在分析IDF...'):
                analyze_idfs = tasks.analyze_patents_task(patent_analyst, idf1_content, idf2_content)
                analysis_crew = Crew(
                    agents=[patent_analyst],
                    tasks=[analyze_idfs],
                    verbose=True
                )
                analysis_output = analysis_crew.kickoff()
                st.session_state.analysis_report = str(analysis_output)

            st.success("IDF分析完成")
            with st.expander("查看IDF分析報告", expanded=True):
                st.write(st.session_state.analysis_report)

            # 第二階段：合併IDF
            with st.spinner('正在合併IDF...'):
                merge_idfs = tasks.merge_patents_task(patent_merger, st.session_state.analysis_report)
                merge_crew = Crew(
                    agents=[patent_merger],
                    tasks=[merge_idfs],
                    verbose=True
                )
                merge_output = merge_crew.kickoff()
                st.session_state.merged_idf = str(merge_output)

            st.success("IDF合併完成")
            with st.expander("查看合併後的IDF", expanded=True):
                st.write(st.session_state.merged_idf)

            # 第三階段：法律審核
            with st.spinner('正在進行法律審核...'):
                legal_review = tasks.legal_review_task(legal_reviewer, st.session_state.merged_idf)
                legal_crew = Crew(
                    agents=[legal_reviewer],
                    tasks=[legal_review],
                    verbose=True
                )
                legal_output = legal_crew.kickoff()
                st.session_state.legal_review = str(legal_output)

            st.success("法律審核完成")
            with st.expander("查看法律審核報告", expanded=True):
                st.write(st.session_state.legal_review)

            # 保存合併後的IDF文檔
            import datetime
            current_time = datetime.datetime.now()
            file_name = f"merged_idf_{current_time.strftime('%Y%m%d_%H%M%S')}.md"
            
            # 創建 .\merged_idfs 文件夾（如果不存在）
            merged_idfs_folder = os.path.join('.', 'merged_idfs')
            os.makedirs(merged_idfs_folder, exist_ok=True)
            
            # 將文件保存到 .\merged_idfs 文件夾
            file_path = os.path.join(merged_idfs_folder, file_name)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("# 合併IDF文檔\n\n")
                f.write("## IDF分析報告\n")
                f.write(st.session_state.analysis_report + "\n\n")
                f.write("## 合併後的IDF\n")
                f.write(st.session_state.merged_idf + "\n\n")
                f.write("## 法律審核報告\n")
                f.write(st.session_state.legal_review)
            st.success(f"合併後的IDF文檔已保存為: {file_path}")

if __name__ == "__main__":
    patent_merger_app()
