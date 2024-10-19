import streamlit as st
from patent_builder_streamlit import patent_builder_app
from poc_builder_streamlit import poc_builder_app
from patent_merger_streamlit import patent_merger_app
from paper_researcher_streamlit import paper_researcher_app

st.title("IDF Research Assistant")

tab1, tab2, tab3, tab4 = st.tabs(["IDF產生器", "PoC 產生器", "IDF合併工具", "相關論文搜尋工具"])

with tab1:
    patent_builder_app()

with tab2:
    poc_builder_app()

with tab3:
    patent_merger_app()

with tab4:
    paper_researcher_app()
