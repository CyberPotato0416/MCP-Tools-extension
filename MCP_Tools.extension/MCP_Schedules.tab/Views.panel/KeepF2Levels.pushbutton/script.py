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

# Collect all Level elements in the document / 在文件中收集所有樓層元素
all_levels = FilteredElementCollector(doc).OfClass(Level).ToElements()

# Get IDs of levels currently visible in the active view / 獲取當前視圖中可見的樓層 ID
visible_level_ids = [l.Id for l in FilteredElementCollector(doc, view.Id).OfClass(Level)]

ids_to_hide = List[ElementId]()   # Initialize hide list / 初始化隱藏清單
ids_to_unhide = List[ElementId]() # Initialize unhide list / 初始化解除隱藏清單

for lvl in all_levels:
    name = lvl.Name
    is_visible = lvl.Id in visible_level_ids
    
    if name in KEEP_LEVEL_NAMES:
        # If it should be kept but is currently hidden, unhide it
        # 若應保持可見但目前被隱藏，則加入解除隱藏清單
        if not is_visible:
            ids_to_unhide.Add(lvl.Id)
    else:
        # If it's not in the white-list but is currently visible, hide it
        # 若不在白名單中且目前可見，則加入隱藏清單
        if is_visible:
            ids_to_hide.Add(lvl.Id)

if ids_to_hide.Count > 0 or ids_to_unhide.Count > 0:
    with revit.Transaction("Update Level Visibility (F2)"):
        # Bulk hide extra levels / 批量隱藏多餘樓層
        if ids_to_hide.Count > 0:
            view.HideElements(ids_to_hide)
        
        # Bulk unhide required levels / 批量解除隱藏必備樓層
        if ids_to_unhide.Count > 0:
            view.UnhideElements(ids_to_unhide)
