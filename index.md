# 🛠️ MCP-Tools 私人研發室索引 (Repository Index)

本倉庫存放由 Jerry / Antigravity 開發的私人機電自動化工具集 (pyRevit Extension)。這些工具旨在優化 BIM 建模與交付效率，並嚴格遵循 MCP 專案協議。

---

## 📺 1. Views (視圖管理)
| 工具名稱 | 版本 | 圖示 | 功能簡介 |
| :--- | :--- | :--- | :--- |
| **TemplateLevelManager** | v1.1 | 🔍| **樣板樓層管理員**。跨樣板批量控制樓層線隱藏，支援領域/類型篩選與狀態記憶。 |
| **DependentSplit** | v1.1 | 🍕| **視圖矩陣分割器**。鋼彈光束軍刀切披薩！精準矩陣裁切從屬視圖並自動放圖排版。 |

---

## 🏷️ 2. Marking (標記系統)
| 工具名稱 | 版本 | 功能簡介 |
| :--- | :--- | :--- |
| **Pick Mark** | v1.0 | 元素手動標註。透過點選元件快速寫入遞增序列號。 |
| **Mark Settings** | v1.0 | 標註參數配置。設定標記前綴、補位長度與起始序號。 |
| **Wizard Pick** | v1.0 | 標註精靈。依照高級協議自動生成複雜結構化編碼。 |
| **Wizard Settings** | v1.0 | 精靈標註配置。設定精靈編碼協議的各項細節內容。 |

---

## 🏗️ 3. TEST & Sandbox (實驗性工具與沙盒)
*此區域工具已移至專屬 `TEST` 目錄進行持續驗證。*

| 工具名稱 | 狀態 | 功能簡介 |
| :--- | :--- | :--- |
| **SplitPipe** | WIP | 🏗️ | **切管大師**。精準 5m 模組化切割，並在間隙中自動預留背對背法蘭位置。 |
| **Quick Pipe (1-5)** | v1.1 | ⚡ | **五路快速管材**。已進化為 5 個實體小按鈕，支援一鍵切換預設的水管/風管系統模型。 |
| **Quick Pipe Settings** | v1.0 | 🛠️ | **管材按鈕配置**。自訂 5 個小按鈕對應的管類型與系統，實現極速建模切換。 |
| **Flange Diagnosis** | Tool | **法蘭診斷箱**。檢驗向量旋轉與拓樸連接，為 AI 分析提供基礎數據。 |
| **Common Utilities** | Tools | 包含 CropBox 擴張、DumpInfo 數據導出等開發者輔助工具。 |

---

## ⚡ 4. Standard / Schedules (工程標準化)
| 工具名稱 | 版本 | 功能簡介 |
| :--- | :--- | :--- |
| **Create Schedules**| v1.0 | 建立標準明細表。一鍵生成 MCP V1.1 採購明細表。 |
| **Quick Pipe Set** | v1.0 | 常用管材設定。配置頂部功能區的 5 個常用管材快選按鈕。 |

---

## 🚀 核心競爭力分析 (Strategic Analysis)
*相對於全球開源庫 (pyRevitMEP, EF-Tools) 的獨特優勢：*

1.  **矩陣式分圖邏輯 (Grid-Matrix Focus)**：
    專攻大型廠房的矩陣式分割，解決了大規模專案的裁切精度與批量放圖問題。
2.  **動態過濾與配置持久化 (Filtering & Persistence)**：
    `TemplateLevelManager` 展現了標準工具的 UI 交互，具備領域、類型篩選與跨工作階段的狀態記憶 (JSON Based)。
3.  **深度協定標註 (Protocol-Driven Tagging)**：
    `WizardPick` 內建的結構化編碼邏輯，是專為複雜機電系統 (LOD 350+) 交付標準量身打造。


---
**最新維護日期**：2026-04-24 
**開發指南**：請參閱內部的 `AGENTS.md` 以進行 AI 協作開發。
