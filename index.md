# 🛠️ MCP-Tools 私人研發室索引 (Repository Index)

本倉庫存放由 Jerry / Antigravity 開發的私人機電自動化工具集 (pyRevit Extension)。這些工具旨在優化 BIM 建模與交付效率，並嚴格遵循 MCP 專案協議。

---

## 📺 1. Views (視圖管理)
| 工具名稱 | 版本 | 功能簡介 |
| :--- | :--- | :--- |
| **DependentSplit** | v1.0 | 視圖矩陣分割器。自動裁切從屬視圖並批量生成圖紙。 |

---

## 🏷️ 2. Marking (標記系統)
| 工具名稱 | 版本 | 功能簡介 |
| :--- | :--- | :--- |
| **Pick Mark** | v1.0 | 元素手動標註。透過點選元件快速寫入遞增序列號。 |
| **Mark Settings** | v1.0 | 標註參數配置。設定標記前綴、補位長度與起始序號。 |
| **Wizard Pick** | v1.0 | 標註精靈。依照高級協議自動生成複雜結構化編碼。 |
| **Wizard Settings** | v1.0 | 精靈標註配置。設定精靈編碼協議的各項細節內容。 |

---

## 📏 3. Standard (工程開發與診斷)
| 工具名稱 | 版本 | 功能簡介 |
| :--- | :--- | :--- |
| **SplitPipe** | v1.0 (WIP) | 切管大師。精準 5m 模組切分與法蘭對接 (開發中)。 |
| **Create Schedules**| v1.0 | 建立標準明細表。一鍵生成 MCP V1.1 採購明細表。 |
| **Flange Diagnosis** | v1.0 | 法蘭診斷箱。診斷法蘭的向量旋轉與拓樸連接問題。 |
| **Dump Info** | v1.0 | 數據導出工具。將法蘭幾何數據導出為 JSON 供 AI 分析。 |
| **TestPipe Sandbox** | v1.0 | 測試沙盒。快速複製測試環境以進行幾何驗證。 |

---

## ⚡ 4. Quick Access (快速存取)
| 工具名稱 | 版本 | 功能簡介 |
| :--- | :--- | :--- |
| **Quick Pipe Set** | v1.0 | 常用管材設定。配置頂部功能區的 5 個常用管材快選按鈕。 |

---

## 🚀 核心競爭力分析 (Strategic Analysis)
*相對於全球開源庫 (pyRevitMEP, EF-Tools, pyrevitplus, OpenMEP, guRoo) 的獨特優勢：*

1.  **矩陣式分圖邏輯 (Grid-Matrix Focus)**：
    相較於大師庫常見的「一樓一層」生成，`DependentSplit` 專攻超大型廠房的矩陣分圖，解決了大規模專案的裁切精度問題。
2.  **深度協定標註 (Protocol-Driven Tagging)**：
    `WizardPick` 內建的複雜編碼邏輯 (System;Bldg.Floor.Zone-Seq) 是專為工程交付標準打造，超越了通用型工具的單純跳號功能。
3.  **構造級切割 (Construction-Level Splitting)**：
    `SplitPipe` 採用獨家的「Delete & Redraw」策略，並在 5m 模組中精準安插背對背法蘭間隙，是少見具備實體施工安裝考量的建模工具。
4.  **開發者診斷意識 (Diagnostics & Metadata)**：
    `FlangeDiagnosis` 與 `DumpInfo` 的存在，大幅降低了機電自動化開發過程中的幾何除錯成本，確保模型數據的潔淨度。

---
**最新維護日期**：2026-04-23
**開發指南**：請參閱內部的 `AGENTS.md` 以進行 AI 協作開發。
