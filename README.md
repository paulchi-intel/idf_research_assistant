# IDF 研究助手 (IDF Research Assistant)
<p align="left">
  <img src="media/icon_idf_research_assistant.png" alt="IDF Research Assistant Icon" width="200"/>
</p>

這是一個用於 AI PC IDF研究的多功能工具。它包含 IDF 生成器、概念驗證（PoC）生成器、IDF 合併工具和相關論文搜尋工具。

## Demo Video
(Under media/IDF Research Assistant Demo.mp4)
<video width="640" height="360" controls>
  <source src="media/demo_video.mp4" type="video/mp4">
  您的浏览器不支持视频标签。
</video>

## 功能

1. **IDF 生成器**：基於關鍵字生成創新的 AI PC 功能設計。
2. **PoC 生成器**：根據解決方案描述生成概念驗證文件。
3. **IDF 合併工具**：合併兩個 IDF 文件，創建一個新的綜合 IDF。
4. **相關論文搜尋工具**：根據 IDF 內容搜尋相關學術論文。

## 專案結構

本專案使用了多個 agents 和 tasks 來完成不同的功能：

### 1. IDF 生成器

**Agents:**
- ODM PM Agent：負責提出創新和前瞻性的 AI PC 功能設計
- Expert Agent：負責優化 AI PC 的特定功能
- Patent Engineer Agent：負責為 AI PC 創新提供專業的專利保護策略

**Tasks:**
- 生成創意任務
- 生成解決方案任務
- 創建專利文件任務

### 2. PoC 生成器

**Agents:**
- Requirements Analyst：分析並明確 PoC 的需求和目標
- Architect：設計 PoC 的整體架構和技術方案
- Developer：實現 PoC 的核心功能
- QA Engineer：驗證 PoC 的功能和效能
- Project Manager：協調整個 PoC 開發過程
- Security Expert：評估 PoC 的安全性，提供安全建議
- UX Designer：優化 PoC 的使用者介面和互動
- Technical Writer：撰寫 PoC 的技術文件和使用說明

**Tasks:**
- 需求分析任務
- 架構設計任務
- 原型開發任務
- 測試任務
- 專案管理任務
- 安全評估任務
- UI 設計任務
- 文件編寫任務

### 3. IDF 合併工具

**Agents:**
- Patent Analyst Agent：分析並比較兩篇專利的關鍵元素
- Patent Merger Agent：將兩篇專利的關鍵元素合併成一個新的、更全面的專利
- Legal Review Agent：確保合併後的專利符合法律要求並具有可專利性

**Tasks:**
- 專利分析任務
- 專利合併任務
- 法律審查任務

### 4. 相關論文搜尋工具

**Agents:**
- Patent Analyst Agent：分析專利文件，提取關鍵字
- Paper Search Specialist Agent：使用 arXiv API 搜尋相關論文
- System Coordinator Agent：協調整個工作流程，整合結果

**Tasks:**
- 提取關鍵字任務
- 論文搜尋任務
- 研究協調任務

這些 agents 和 tasks 共同工作，以實現 IDF 研究助手的各項功能。

## 安裝

1. 複製此倉庫：

git clone https://github.com/paulchi-intel/idf_research_assistant


2. 安裝依賴套件：
   
pip install -r requirements.txt


3. 創建 .env 文件： 在專案根目錄創建一個 .env 文件，並添加以下內容：
   
   AZURE_OPENAI_VERSION="your_openai_version"
   AZURE_OPENAI_DEPLOYMENT="your_openai_deployment"
   AZURE_OPENAI_ENDPOINT="your_openai_endpoint"
   AZURE_OPENAI_KEY="your_openai_key"

   請確保替換上述佔位符為您的實際 Azure OpenAI 配置資訊。

## 使用

執行主應用程式：

streamlit run idf_research_assistant.py


然後在瀏覽器中打開顯示的 URL 來訪問應用程式。

## 注意事項

- 請確保您有有效的 Azure OpenAI 帳戶和相應的 API 金鑰。
- 使用前請仔細閱讀每個工具的說明。
- 生成的內容僅供參考，請根據實際需求進行調整和驗證。

## 貢獻

歡迎提交問題和拉取請求。對於重大變更，請先開 issue 討論您想要更改的內容。

## 授權

[MIT](https://choosealicense.com/licenses/mit/)  
