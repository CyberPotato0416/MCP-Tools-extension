# -*- coding: utf-8 -*-
from pyrevit import revit, DB

doc = revit.doc
view = doc.ActiveView

if not isinstance(view, DB.ViewSheet):
    print("請在圖紙視圖執行此腳本。")
else:
    # 取得這張圖紙上所有的視埠
    viewports = [doc.GetElement(id) for id in view.GetAllViewports()]
    
    # 圖框尺寸約為 3.5 英呎 x 2.5 英呎
    # 我們設定四個黃金象限點
    positions = {
        0: DB.XYZ(0.9, 0.8, 0), # Plan (左下)
        1: DB.XYZ(2.4, 0.8, 0), # Front (右下)
        2: DB.XYZ(0.9, 1.8, 0), # Side (左上)
        3: DB.XYZ(2.4, 1.8, 0)  # 3D (右上)
    }

    with revit.Transaction("精確排版視埠"):
        for i, vp in enumerate(viewports):
            # 取得視圖名稱以判斷類型 (如果索引不準的話)
            v = doc.GetElement(vp.ViewId)
            vname = v.Name.lower()
            
            target_pos = None
            if "plan" in vname: target_pos = positions[0]
            elif "front" in vname: target_pos = positions[1]
            elif "side" in vname: target_pos = positions[2]
            elif "3d" in vname: target_pos = positions[3]
            
            if target_pos:
                vp.SetBoxCenter(target_pos)
            elif i in positions: # 備案：按索引排
                vp.SetBoxCenter(positions[i])
            
    print("視埠已精確排版至四個象限。")
