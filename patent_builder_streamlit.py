import streamlit as st
import os
from dotenv import load_dotenv
from crewai import Crew, Agent, Task
from langchain_openai import AzureChatOpenAI
from patent_builder_tasks import PatentTasks
from patent_builder_agents import PatentAgents

load_dotenv()

# 設置Azure OpenAI
default_llm = AzureChatOpenAI(
    openai_api_version=os.environ.get("AZURE_OPENAI_VERSION", "2023-07-01-preview"),
    azure_deployment=os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt35"),
    azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT", "https://<your-endpoint>.openai.azure.com/"),
    api_key=os.environ.get("AZURE_OPENAI_KEY")
)

tasks = PatentTasks()
agents = PatentAgents()

def patent_builder_app():
    st.header("AI PC IDF產生器")
    
    keyword = st.text_input("請輸入關鍵字（例如：Power and Performance）", value="Power and Performance")

    odm_pm_agent = agents.odm_pm_agent(llm=default_llm, keyword=keyword)
    expert_agent = agents.expert_agent(llm=default_llm, keyword=keyword)
    patent_engineer_agent = agents.patent_engineer_agent(llm=default_llm)

    # 添加一個按鈕來開始生成創意
    if st.button("開始生成創意", key="idf_generate"):
        # 第一階段：生成創意
        with st.spinner('正在生成創意...'):
            generate_ideas = tasks.generate_ideas_task(odm_pm_agent)
            ideas_crew = Crew(
                agents=[odm_pm_agent],
                tasks=[generate_ideas],
                verbose=True
            )
            ideas_output = ideas_crew.kickoff()
            ideas = str(ideas_output)
            st.session_state.ideas = ideas

        # 處理創意
        ideas_list = st.session_state.ideas.split('\n')
        cleaned_ideas = []
        current_idea = ""
        current_title = ""
        ideas_dict = {}
        for idea in ideas_list:
            if "創意" in idea and ":" in idea:
                if current_idea and current_title:
                    cleaned_ideas.append(current_title)
                    ideas_dict[current_title] = current_idea.strip()
                current_title = idea.strip().split(':', 1)[-1].strip()
                current_idea = current_title + "\n"
            elif idea.strip() and not idea.strip().startswith(("---", "my best complete final answer")):
                current_idea += idea.strip() + "\n"
        if current_idea and current_title:
            cleaned_ideas.append(current_title)
            ideas_dict[current_title] = current_idea.strip()

        # 展示創意並讓用戶選擇
        st.session_state.cleaned_ideas = cleaned_ideas
        st.session_state.ideas_dict = ideas_dict

    # 如果已經生成了創意,則顯示選擇框
    if 'cleaned_ideas' in st.session_state and 'ideas_dict' in st.session_state:
        selected_idea_title = st.selectbox("請選擇一個創意:", st.session_state.cleaned_ideas)
        if selected_idea_title:
            st.text_area("創意詳情:", value=st.session_state.ideas_dict[selected_idea_title], height=300)

            # 第二階段：生成解決方案
            if st.button("生成解決方案"):
                with st.spinner('正在生成解決方案...'):
                    generate_solutions = tasks.generate_solutions_task(expert_agent, st.session_state.ideas_dict[selected_idea_title])
                    solutions_crew = Crew(
                        agents=[expert_agent],
                        tasks=[generate_solutions],
                        verbose=True
                    )
                    solutions_output = solutions_crew.kickoff()
                    solutions = str(solutions_output)
                    st.session_state.solutions = solutions

    # 處理解決方案
    if 'solutions' in st.session_state:
        solutions_list = st.session_state.solutions.split('\n')
        cleaned_solutions = []
        current_solution = ""
        current_title = ""
        solutions_dict = {}
        for solution in solutions_list:
            if "解決方案" in solution and ":" in solution:
                if current_solution and current_title:
                    cleaned_solutions.append(current_title)
                    solutions_dict[current_title] = current_solution.strip()
                current_title = solution.strip().split(':', 1)[-1].strip()
                current_solution = current_title + "\n"
            elif solution.strip() and not solution.strip().startswith(("---", "my best complete final answer")):
                current_solution += solution.strip() + "\n"
        if current_solution and current_title:
            cleaned_solutions.append(current_title)
            solutions_dict[current_title] = current_solution.strip()

        # 展示解決方案並讓用戶選擇
        selected_solution_title = st.selectbox("請選擇一個解決方案:", cleaned_solutions)
        if selected_solution_title:
            st.text_area("解決方案詳情:", value=solutions_dict[selected_solution_title], height=300)

        # 第三階段：生成專利文檔
        if st.button("生成專利文檔"):
            with st.spinner('正在生成專利文檔...'):
                create_patent = tasks.create_patent_task(patent_engineer_agent, st.session_state.ideas_dict[selected_idea_title], solutions_dict[selected_solution_title])
                patent_crew = Crew(
                    agents=[patent_engineer_agent],
                    tasks=[create_patent],
                    verbose=True
                )
                patent_output = patent_crew.kickoff()
                patent = str(patent_output)
                st.session_state.patent = patent

    # 顯示生成的專利
    if 'patent' in st.session_state:
        st.subheader("生成的IDF文檔:")
        st.markdown(st.session_state.patent)

        # 保存IDF文檔
        import datetime
        current_time = datetime.datetime.now()
        file_name = f"idf_{current_time.strftime('%Y%m%d_%H%M%S')}.md"
        
        # 創建 .\idf 文件夾（如果不存在）
        idf_folder = os.path.join('.', 'idf')
        os.makedirs(idf_folder, exist_ok=True)
        
        # 將文件保存到 .\idf 文件夾
        file_path = os.path.join(idf_folder, file_name)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("# AI PC IDF文檔\n\n")
            f.write(st.session_state.patent)
        st.success(f"IDF文檔已保存為: {file_path}")

if __name__ == "__main__":
    patent_builder_app()
