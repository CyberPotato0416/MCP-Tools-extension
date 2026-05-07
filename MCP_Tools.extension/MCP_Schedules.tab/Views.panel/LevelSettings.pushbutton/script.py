# -*- coding: utf-8 -*-
__title__  = "LevelSettings"
__author__ = "Jerry / Antigravity"
__doc__    = "Configure the custom whitelist of levels to be displayed by IsolateLevels."

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
