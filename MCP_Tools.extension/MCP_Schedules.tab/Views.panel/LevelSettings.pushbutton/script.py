# -*- coding: utf-8 -*-
"""
LevelSettings (設定樓層按鈕)
Author: Jerry / Antigravity

[Design Intent / 開發動機]:
This tool fills a critical gap in Revit View Templates. While templates can toggle 
the 'Levels' category on/off, they lack the granularity to isolate specific levels. 
This "Dynamic Level Whitelist" allows users to save a custom selection of levels 
to be displayed, which is essential for high-tech fab layouts and high-rise coordination.

此工具補足了 Revit 視圖樣板 (View Template) 的功能缺口。視圖樣板通常僅能針對「樓層」品類進行全開或全關，
無法精確隔離特定樓層。本工具建立一套「動態樓層白名單」，允許使用者儲存特定的樓層顯示組合，
其運作邏輯提供極高的靈活性，效果等同於在單張視圖中手動調整 VG (Visibility/Graphics) 覆蓋，
但改由動態設定檔統一驅動。這在處理高科技廠房佈局與高層建築協調時極具實務價值。
"""
from pyrevit import revit, DB, forms, script
import json
import os

def main():
    doc = revit.doc
    
    # 1. Get all levels / 獲取所有樓層
    levels = DB.FilteredElementCollector(doc).OfClass(DB.Level).ToElements()
    level_names = sorted([l.Name for l in levels])
    
    # 2. Show Selection UI / 顯示選擇介面
    selected_levels = forms.SelectFromList.show(
        level_names,
        title="[設定] 選擇要保持顯示的樓層",
        multiselect=True
    )
    
    if selected_levels:
        # 3. Save to Config File (Forcing UTF-8) / 儲存至設定檔 (強制 UTF-8)
        config_path = os.path.join(os.path.dirname(__file__), "level_config.json")
        data = {"keep_levels": selected_levels}
        
        try:
            import io
            with io.open(config_path, 'w', encoding='utf-8') as f:
                f.write(unicode(json.dumps(data, ensure_ascii=False, indent=4)))
            forms.alert("設定已儲存：\n" + "\n".join(selected_levels), title="設定成功")
        except Exception as e:
            forms.alert("儲存設定失敗: " + str(e))
    else:
        forms.alert("未選擇任何樓層，設定取消。", title="取消")

if __name__ == "__main__":
    main()
