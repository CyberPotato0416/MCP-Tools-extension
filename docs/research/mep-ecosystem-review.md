# 全球 pyRevit 擴展開發生態系與機電工程自動化實務研究報告

在當前建築資訊模型（BIM）的技術演進過程中，Autodesk Revit 的原生功能往往難以完全滿足機電工程（MEP）領域對於極致效率與精密圖冊輸出的需求。隨著計算設計（Computational Design）與自動化工作流的普及，由 Ehsan Iran-Nejad 所創立的 pyRevit 框架已成為全球 BIM 管理者與開發者首選的快速應用開發（RAD）環境 。對於正致力於完善 MCP-Tools 擴展庫的機電領域專業人士而言，深入研究全球頂尖開發者的源代碼與設計邏輯，不僅能直接擴充工具箱的功能維度，更能洞察如何透過 Python 腳本將複雜的機電邏輯轉化為直觀的 Revit 操作介面 。  

### pyRevit 框架的核心機制與機電開發背景

pyRevit 不僅是一個插件，它更是一個整合了 IronPython、CPython、C# 與 VB.Net 的開發平台，允許開發者在無需編譯的情況下，直接與 Revit API 進行互動 。這對於需要頻繁迭代工具邏輯的機電工程師而言至關重要。機電領域的特點在於其系統高度複雜且數據量龐大，涉及管道（Pipe）、風管（Duct）、電纜橋架（Cable Tray）以及成千上萬的設備族實例 。  

全球機電工程與 BIM 輸出的頂尖開發者通常集中於解決兩大痛點：一是幾何空間的自動化協調，二是高強度文檔編製流程的效率化 。例如，透過 CLI 工具與遠端遙測服務（Telemetry Server），BIM 經理可以跨團隊監控工具的使用情況，並根據數據回饋優化腳本 。這種數據導向的開發思維，是 MCP-Tools 邁向成熟擴展庫的必經之路。  

### 機電工程（MEP）領域的全球頂尖擴展庫解析

在機電自動化領域，Cyril Waechter 與 Chuong Mep 是兩位極具影響力的「大神」。他們的開發項目為全球機電工程師提供了從底層幾何計算到上層系統管理的全面參考 。  

#### Cyril Waechter 與 pyRevitMEP 的精密控制

Cyril Waechter 開發的 pyRevitMEP 是目前公認最成熟的機電專用擴展庫之一 。該庫的核心優勢在於其對 MEP 元素空間關係的深刻理解。例如，其開發的 ElevationUnder 工具利用了 ReferenceIntersector 類別，能在三維視圖中向下投射射線，自動捕捉機電管線下方的結構或建築元素，這在計算管道淨高與吊架安裝空間時具有極高的實用價值 。  

下表整理了 pyRevitMEP 中最具代表性的幾大功能模組及其技術核心：

| 功能名稱 | 核心技術邏輯 | 機電工程應用情境 |
| :--- | :--- | :--- |
| **CreateSectionFrom** | 基於選定線性元素（管線）的向量，自動生成平行或垂直剖面 。 | 快速生成管道剖面圖，確保安裝坡度與淨高符合設計規範。 |
| **ElementChangeLevel** | 在不移動物理位置的情況下修改元素的關聯能階（Level） 。 | 解決模型重整時管線系統與建築樓層關聯錯誤的痛點。 |
| **CopyViewType** | 利用 API 跨文件複製視圖類型設定，確保機電出圖標準一致 。 | 維護企業內部不同項目間的機電出圖標準化。 |
| **Data.panel 數據管理** | 批量讀取與寫入機電系統參數。 | 自動化命名機電空間與設備編號。 |

Cyril Waechter 的設計哲學強調「幾何精準度」。在處理如 45 度或 60 度等特殊角度的管線連接時，其腳本能精確計算旋轉向量（Vector Manipulation），避免了 Revit 原生對齊工具在非正交角度下的失效問題 。  

#### Chuong Mep 與 OpenMEP 的生態系整合

相對於 Cyril Waechter 側重於 pyRevit 工具列的開發，Chuong Mep 開發的 OpenMEP 則更傾向於提供一個跨平台的機電自動化庫 。OpenMEP 支援 Dynamo 與 pyRevit 的雙軌開發，其內部封裝了大量的機電計算節點，包含管道壓力降、風量計算以及設備族自動載入機制 。  

對於 MCP-Tools 的開發而言，OpenMEP 的意義在於其提供的「底層組件庫」。開發者可以透過引用 OpenMEP 的 DLL 或 Python 庫，快速實現如自動避讓（Auto-Clash Resolve）或管徑自動計算等高級功能 。此外，Chuong Mep 也積極整合 RevitDBExplorer，這讓開發者在調試機電系統數據時，能以樹狀結構清晰地觀察 MEP 系統（MEP System）中各構件的隸屬關係 。  

### BIM 出圖與文檔編製的自動化大師

對於「常常用 BIM 出圖的人」來說，出圖效率決定了項目的利潤率。在這個領域，Gui Talarico、Erik Frits 以及 Gavin Crump (aussieBIMguru) 提供了極致的圖冊管理方案 。  

#### Gui Talarico 與 pyrevitplus 的對齊美學

Gui Talarico 所開發的 pyrevitplus 是 pyRevit 社群中最受歡迎的擴展之一，其核心在於「Smart Align」系列工具 。在機電圖紙中，標註（Tag）與文字（Text）的整齊排列直接影響圖紙的可讀性。Smart Align 能自動計算多個標註之間的間距，並沿著指定軸線進行等距分布，這在平面圖中管線密集的機電區域尤為重要 。  

此外，其 Auto Plans 功能能根據選定的房間或區域自動生成放大圖，並套用預設的視圖模板 。對於機電工程師來說，這意規著只需點擊一次，就能完成所有機電房（Plant Room）或電力間的放大詳圖製作 。  

#### Erik Frits 與 EF-Tools 的效率工具箱

Erik Frits 的 EF-Tools 包含了超過 50 個實用工具，其開發理念是「消滅重複性勞動」 。在 BIM 出圖過程中，字體統一與圖紙編號往往耗費大量時間。EF-Tools 提供的 Change Font 工具能跨族群修改字體，而其 Warnings Manager 則能根據優先級對機電模型中的衝突進行分類，確保在出圖前模型健康度達到標準 。  

| 出圖自動化工具 | 開發者 | 核心價值 |
| :--- | :--- | :--- |
| **Batch Sheet Maker** | pyRevit 內建 / Ehsan | 透過 Excel 清單秒級創建數百張圖紙 。 |
| **Print Ordered Sheets** | Ehsan / Ryan | 根據圖紙索引排序批量打印，解決 Revit 亂序打印問題 。 |
| **Smart Align (Text/Tag)** | Gui Talarico | 自動化排列機電標註，提升圖面專業感 。 |
| **AnnoChart** | Gui Talarico | 將明細表數據轉化為柱狀圖，直觀展示機電能耗或工程量 。 |

#### Gavin Crump 與 guRoo 的交付優化

Gavin Crump（aussieBIMguru）開發的 guRoo 庫則專注於項目交付階段的效率提升 。他的工具強調與 Excel 的深度鏈接，例如將圖紙清單從 Excel 寫回 Revit，或是自動化導出符合 BIM 交付標準的圖紙參數 。這對於需要處理大量變更單與圖冊更新的機電設計師來說，是極具參考價值的開發範例。  

### 機電自動化開發的深層技術邏輯

在研究上述大神的插件時，必須關注其背後的幾何代數運算與 API 呼叫效率。機電管線的自動對齊與避讓本質上是向量運算 。  

#### 向量數學在管線連接中的應用

當開發者嘗試撰寫如 PipeSplit 或 AutoRoute 工具時，必須精確計算兩條管線在空間中的交點。若兩管線分別由直線 $L_1: P_1 + t v_1$ 與 $L_2: P_2 + s v_2$ 表示，腳本需要判定兩者是否共面，並計算其最短距離向量 。在 pyRevitMEP 中，這類運算常被封裝於底層函式庫中，以實現如自動生成 45 度彎頭（Elbow）的功能。  

#### 數據庫檢索與過濾性能

機電模型動輒包含數萬個元素，使用 FilteredElementCollector 時，過濾器的選擇直接影響腳本運行速度 。頂尖開發者通常會結合 ElementMulticategoryFilter 同時獲取管道、風管與橋架，並利用 WhereElementIsNotElementType 排除類型定義，僅保留實例 。  

例如，在 ElevationUnder 腳本中，開發者使用了以下邏輯：
1. 建立 ElementMulticategoryFilter，包含機電與結構類別 。  
2. 初始化 ReferenceIntersector，設定其在 3D 視圖中沿 −Z 軸投射 。  
3. 獲取所有 ReferenceWithContext，並過濾出距離最近的結構面 。  

這種基於幾何射線（Ray Casting）的檢索技術，是 MCP-Tools 實現高級協調功能（如管線與樑底自動淨高標註）的核心技術儲備。

### 針對 MCP-Tools-extension 的具體建議與整合路徑

基於對目前全球 pyRevit 擴展庫的調研，對於 MCP-Tools 的未來開發與納庫工作，建議採取以下戰略步驟：

#### 1. 核心功能納庫優先順序

開發者應優先參考 Cyril Waechter 的 pyRevitMEP 以完善機電幾何功能，並參考 Gui Talarico 的 pyrevitplus 以強化出圖效率。
*   **管線切分與優化 (Pipe/Duct Splitting)**：借鑒 André Rodrigues da Silva 的 MEPDesign 。實現代碼中應包含對標準管段長度的判斷，自動在 6 米或 4 米處切分並添加法蘭或套管 。  
*   **機電標註對齊 (MEP Tag Alignment)**：借鑒 pyrevitplus 的 Smart Align 。這能極大地縮短機電平面圖的整理時間。  
*   **設備參數同步 (Parameter Synchronizer)**：開發一套工具，能將建築房間（Room）的參數（如房間編號、名稱）自動同步至該房間內的機電設備（如風機過濾單元 FFU 或插座）中，這在後期維護管理中極其重要 。  

#### 2. 開發規範與庫結構優化

為了確保 MCP-Tools 具有良好的可維護性，建議參考 pyrevitlabs 的官方規範與 GerhardPaw 的 RevitPythonDocs 指南 ：  
*   **模組化函式庫 (lib 夾)**：將重複使用的機電邏輯（如獲取管道內徑、計算電纜填充率等）放入 lib 文件夾中，這與 guRoo 和 pyRevitMEP 的架構一致 。  
*   **用戶介面一致性**：使用 pyrevit.forms 提供的標準對話框（如 SelectFromList），這能讓機電工程師在使用 MCP-Tools 時感到與 pyRevit 原生工具無異 。  
*   **異常處理 (Transaction Handling)**：在進行大規模機電參數寫入時，務必使用 Python 的上下文管理器（With Transaction）以確保數據完整性，並在出錯時自動回滾（Rollback） 。  

#### 3. 團隊協作與分發策略

對於機電設計院或 BIM 諮詢公司而言，MCP-Tools 的分發同樣關鍵。研究顯示，透過「共享網絡驅動器」部署 pyRevit 擴展是最高效的方案 。  
在這種模式下：
1. MCP-Tools 存儲於公司內部的 `X:\BIM_Standard\MCP-Tools.extension` 。  
2. 每位工程師的 pyRevit 設置中添加該路徑。
3. 開發者只需更新該目錄下的腳本，全公司所有工程師即可在重啟 Revit 後獲得最新功能 。  

配合 Telemetry Server，BIM 經理可以追蹤哪些機電自動化腳本最常被使用，進而將資源投入到高頻工具的研發中 。  

### 結論：機電 BIM 自動化的未來展望

機電工程的自動化已從簡單的「參數填充」演進為複雜的「決策輔助」。透過對 Cyril Waechter、Chuong Mep、Gui Talarico 等大神的深入研究，開發者可以發現，優秀的 pyRevit 擴展庫不僅僅是代碼的集合，更是機電設計邏輯與 BIM 操作習慣的深度契合。

對於 MCP-Tools-extension 而言，納入全球大神的精華代碼只是第一步。真正的價值在於根據台灣或特定市場的機電法規與出圖標準，對這些工具進行二次開發與優化。例如，結合 OpenMEP 的計算邏輯與 pyrevitplus 的視覺對齊，開發出一套專屬於機電消防或空調系統的「一鍵出圖」工作流 。隨著 CPython 在 pyRevit 中的進一步成熟，未來機電開發者甚至可以引入機器學習庫（如 Scikit-learn），實現自動化的機電管線路由建議，將 BIM 的價值從單純的建模提升至智慧設計的高度 。
