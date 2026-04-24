# -*- coding: utf-8 -*-
from Autodesk.Revit.DB import *
from pyrevit import revit, forms
from System.Collections.Generic import List
import json
import os

def main():
    doc = revit.doc
    view = revit.active_view
    
    if view is None or view.IsTemplate:
        forms.alert("請在非樣板的啟動視圖中執行。")
        return

    # 1. Load Config / 讀取設定
    # Note: We look for the config in the sibling directory 'LevelSettings.pushbutton'
    # or define a shared path. Here we assume they are siblings.
    parent_dir = os.path.dirname(os.path.dirname(__file__))
    config_path = os.path.join(parent_dir, "LevelSettings.pushbutton", "level_config.json")
    
    if not os.path.exists(config_path):
        forms.alert("尚未設定樓層清單，請先執行 [設定樓層] 按鈕。", title="找不到設定")
        return
        
    try:
        import io
        with io.open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()
            data = json.loads(content)
            keep_names = data.get("keep_levels", [])
    except Exception as e:
        forms.alert("讀取設定失敗: " + str(e))
        return

    if not keep_names:
        forms.alert("設定清單為空。")
        return

    # 2. Logic: Hide/Unhide / 執行隱藏與顯示邏輯
    all_levels = FilteredElementCollector(doc).OfClass(Level).ToElements()
    visible_level_ids = [l.Id for l in FilteredElementCollector(doc, view.Id).OfClass(Level)]

    ids_to_hide = List[ElementId]()
    ids_to_unhide = List[ElementId]()

    for lvl in all_levels:
        name = lvl.Name
        is_visible = lvl.Id in visible_level_ids
        
        if name in keep_names:
            if not is_visible:
                ids_to_unhide.Add(lvl.Id)
        else:
            if is_visible:
                ids_to_hide.Add(lvl.Id)

    if ids_to_hide.Count > 0 or ids_to_unhide.Count > 0:
        with revit.Transaction("Update Level Visibility (Dynamic)"):
            if ids_to_hide.Count > 0:
                view.HideElements(ids_to_hide)
            if ids_to_unhide.Count > 0:
                view.UnhideElements(ids_to_unhide)
        
        forms.alert("樓層處理完成！\n保持顯示: " + ", ".join(keep_names), title="完成")
    else:
        forms.toast("目前視圖樓層顯示狀態已符合設定。")

if __name__ == "__main__":
    main()
