from Autodesk.Revit.DB import *
from pyrevit import revit
from System.Collections.Generic import List

doc = revit.doc
view = revit.active_view

# Defined list of Levels to keep visible for F2 layout / 定義 F2 配置中要保持可見的樓層名稱
KEEP_LEVEL_NAMES = []
KEEP_LEVEL_NAMES.append("SFAB_L05 TOPPING")

if view is None:
    raise Exception("沒有啟動中的視圖")

if view.IsTemplate:
    raise Exception("目前視圖是 View Template")

# Collect all Level elements in the current view / 在當前視圖中收集所有樓層元素
collector = FilteredElementCollector(doc, view.Id)
levels = collector.OfClass(Level).ToElements()

ids_to_hide = List[ElementId]()   # Initialize hide list / 初始化隱藏清單

for lvl in levels:
    name = lvl.Name
    # If Level Name is NOT in our white-list, add to hide list / 若樓層名稱不在白名單中，則加入隱藏清單
    if name not in KEEP_LEVEL_NAMES:
        ids_to_hide.Add(lvl.Id)

if ids_to_hide.Count > 0:
    with revit.Transaction("Hide Extra Levels (F2)"):
        # Bulk hide identified levels / 批量隱藏識別出的樓層
        view.HideElements(ids_to_hide)
