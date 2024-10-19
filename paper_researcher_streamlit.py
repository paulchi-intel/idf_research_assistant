import streamlit as st
import os
from dotenv import load_dotenv
from crewai import Crew, Agent, Task
from langchain_openai import AzureChatOpenAI
from paper_researcher_tasks import PaperResearcherTasks
from paper_researcher_agents import PaperResearcherAgents

load_dotenv()

# 設置 Azure OpenAI
default_llm = AzureChatOpenAI(
    openai_api_version=os.environ.get("AZURE_OPENAI_VERSION", "2023-07-01-preview"),
    azure_deployment=os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt35"),
    azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT", "https://<your-endpoint>.openai.azure.com/"),
    api_key=os.environ.get("AZURE_OPENAI_KEY")
)

tasks = PaperResearcherTasks()
agents = PaperResearcherAgents()

def paper_researcher_app():
    st.header("IDF相關論文查找工具")

    # 上傳IDF文件
    uploaded_file = st.file_uploader("上傳IDF文件", type=["txt", "md"])

    if uploaded_file is not None:
        idf_content = uploaded_file.getvalue().decode("utf-8")
        
        # 顯示上傳的IDF內容
        with st.expander("查看IDF內容"):
            st.text_area("IDF內容", idf_content, height=300)

        # 輸入關鍵字數量
        num_keywords = st.number_input("請輸入需要提取的關鍵字數量:", min_value=1, max_value=20, value=5)

        if st.button("開始研究"):
            # 創建代理
            patent_analyst = agents.patent_analyst_agent(llm=default_llm)
            paper_search_specialist = agents.paper_search_specialist_agent(llm=default_llm)
            system_coordinator = agents.system_coordinator_agent(llm=default_llm)

            # 執行研究任務
            with st.spinner('正在進行專利分析...'):
                extract_keywords_task = tasks.extract_keywords_task(patent_analyst, idf_content, num_keywords)
                extract_keywords_crew = Crew(
                    agents=[patent_analyst],
                    tasks=[extract_keywords_task],
                    verbose=True
                )
                keywords_output = extract_keywords_crew.kickoff()
                st.session_state.keywords = str(keywords_output)
            
            with st.expander("專利分析結果", expanded=True):
                st.write("提取的關鍵字：")
                st.write(st.session_state.keywords)

            with st.spinner('正在搜索相關論文...'):
                search_papers_task = tasks.search_papers_task(paper_search_specialist, st.session_state.keywords)
                search_papers_crew = Crew(
                    agents=[paper_search_specialist],
                    tasks=[search_papers_task],
                    verbose=True
                )
                papers_output = search_papers_crew.kickoff()
                st.session_state.papers = str(papers_output)
            
            with st.expander("論文搜索結果", expanded=True):
                st.write("搜索到的論文：")
                st.write(st.session_state.papers)

            with st.spinner('正在生成研究報告...'):
                coordinate_research_task = tasks.coordinate_research_task(
                    system_coordinator, 
                    idf_content, 
                    st.session_state.keywords, 
                    st.session_state.papers
                )
                coordinate_research_crew = Crew(
                    agents=[system_coordinator],
                    tasks=[coordinate_research_task],
                    verbose=True
                )
                research_output = coordinate_research_crew.kickoff()
                st.session_state.research_result = str(research_output)

            st.success("研究完成")
            with st.expander("查看完整研究報告", expanded=True):
                st.write(st.session_state.research_result)

            # 保存研究結果
            import datetime
            current_time = datetime.datetime.now()
            file_name = f"idf_research_{current_time.strftime('%Y%m%d_%H%M%S')}.md"
            
            # 創建 .\idf_research 文件夾（如果不存在）
            research_folder = os.path.join('.', 'idf_research')
            os.makedirs(research_folder, exist_ok=True)
            
            # 將文件保存到 .\idf_research 文件夾
            file_path = os.path.join(research_folder, file_name)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("# IDF相關論文研究報告\n\n")
                f.write("## 提取的關鍵字\n")
                f.write(st.session_state.keywords + "\n\n")
                f.write("## 搜索到的論文\n")
                f.write(st.session_state.papers + "\n\n")
                f.write("## 完整研究報告\n")
                f.write(st.session_state.research_result)
            st.success(f"研究報告已保存為: {file_path}")
    else:
        st.info("請上傳IDF文件")

if __name__ == "__main__":
    paper_researcher_app()
