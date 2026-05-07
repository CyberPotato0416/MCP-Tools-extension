# -*- coding: utf-8 -*-
from pyrevit import revit, DB

doc = revit.doc
view = doc.ActiveView

if not isinstance(view, DB.ViewSheet):
    print("請在圖紙視圖執行此腳本。")
else:
    viewports = [doc.GetElement(id) for id in view.GetAllViewports()]
    
    with revit.Transaction("優化零件圖視覺風格"):
        for vp in viewports:
            v = doc.GetElement(vp.ViewId)
            
            # 1. 設定詳細等級為精緻 (3 = Fine)
            param_detail = v.get_Parameter(DB.BuiltInParameter.VIEW_DETAIL_LEVEL)
            if param_detail:
                param_detail.Set(3)
            
            # 2. 設定視覺型式 (2=隱藏線, 3=描影)
            param_style = v.get_Parameter(DB.BuiltInParameter.MODEL_GRAPHICS_STYLE)
            if param_style:
                if v.ViewType == DB.ViewType.ThreeD:
                    param_style.Set(3) # Shaded
                else:
                    param_style.Set(2) # Hidden Line
            
            # 3. 隱藏 Levels, Grids
            for cat_enum in [DB.BuiltInCategory.OST_Levels, DB.BuiltInCategory.OST_Grids]:
                cat_id = doc.Settings.Categories.get_Item(cat_enum).Id
                if v.CanCategoryBeHidden(cat_id):
                    v.SetCategoryHidden(cat_id, True)
            
    print("視覺風格優化完成！(透過 BuiltInParameter 強制修改)")
