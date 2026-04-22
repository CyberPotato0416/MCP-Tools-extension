# REVIT_MCP_study: Agent 協作規範與專案指南

歡迎參與 `REVIT_MCP_study` 專案！本文件的目的是為 AI 代理（Agents）提供開發背景、核心原則以及研究資源指引，確保開發過程符合專案的「雙軌分權」策略。

## 1. 專案導覽 (Project Overview)

本專案是一個關於 **Revit MCP (Model Context Protocol)** 的研究與知識庫專案。

*   **目標**：透過 Domain-Driven 的方式，記錄如何透過 AI 與 MCP Server 自動化 Revit 工作流。
*   **雙軌分權架構 (Dual-Track Architecture)**：
    *   **本倉庫 (`REVIT_MCP_study`)**：存放「知識 (Knowledge)」。包含 Domain 文件 (`domain/`)、研究報告 (`docs/research/`) 以及視圖、標註等自動化工作流的邏輯指引。
    *   **工具擴展庫 (`MCP-Tools-extension`)**：存放「實體代碼 (Physical Code)」。開發者所有的 pyRevit 實體腳本 (`.py`) 應存放於此獨立倉庫。
        *   🔗 GitHub Link: [MCP-Tools-extension](https://github.com/CyberPotato0416/MCP-Tools-extension)

## 2. Agent 開發核心原則

當您在本專案中進行任務時，請務必遵守以下規範：

1.  **禁止重複造輪子**：在嘗試編寫任何自動化指令前，請先檢索 `domain/` 下的文件，確認是否已有既有的 MCP 工具或 pyRevit 方案。
2.  **知識優先原則**：若開發了新的 pyRevit 工具，請先在 `domain/` 下更新/建立對應的 Markdown 文件，描述「為什麼要這樣做」與「5步驟操作流程」。
3.  **遵循 CI 門衛規範**：本倉庫的 CI (`check-files`) 嚴格禁止在非 `domain/` 或指定目錄下提交程式碼檔案。請保持本倉庫的「純淨知識庫」屬性。
4.  **人機協作 (Human-in-the-loop)**：對於涉及 UI 交互或需要大量手動選取的工具（如 Dependent Split），請定義好 AI 的引導邊界，不要嘗試跳過人為確認步驟。

## 3. 重要研究資源指引

在進行 MEP 幾何運算、出圖自動化或工具優化前，Agent **務必先行閱讀** 以下研究報告：

*   **[MEP 生態系與自動化研究報告](file:///H:/0_REVIT%20MCP/REVIT_MCP_study-main/docs/research/mep-ecosystem-review.md)**：
    *   介紹了全球頂尖開發者（如 Cyril Waechter, Gui Talarico）的技術邏輯。
    *   包含向量數學在管線幾何、標註對齊以及視圖批次產生的實務應用。
    *   為 `MCP-Tools` 提供了功能優化與結構設計的藍圖。

## 4. 目錄結構參考

*   `/domain/`：存放各功能模組的業務場景、邏輯摘要與操作導引。
*   `/docs/research/`：存放關於外部生態系、全球最佳實務的深度研究報告。
*   `/MCP-Server/`：存放 MCP 服務端的接口定義與測試實作。

---
**維護者**：CYBERPOTATO0416
**最後更新**：2026-04-22
