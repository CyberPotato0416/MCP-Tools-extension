# -*- coding: utf-8 -*-
"""
DependentSplit (視圖矩陣分割器)
Author: Jerry / Antigravity
Version: v1.1 (Fixed Imports & Improved UX)

Description / 功能簡介:
依據指定網格邊界（如 1~5 軸、A~E 軸）自動將大型母視圖分割成矩陣狀的從屬視圖 (Dependent Views)。
每個分割出來的小視圖會自動依序：
1. 套用選定的視圖樣板。
2. 建立專屬的新圖紙 (Sheet)。
3. 將視圖放置在圖紙中心。
"""

import os
from Autodesk.Revit.DB import *
import Autodesk.Revit.DB as DB
from pyrevit import revit, forms

# Define document variable
doc = revit.doc

def get_sorted_grids():
    """ 
    Grab all grids and classify them into X and Y groups based on geometry, then sort them by coordinate.
    抓取所有網格，並依幾何幾何座標分類為 X/Y 組，隨後進行排序。
    """
    all_grids = DB.FilteredElementCollector(doc).OfClass(DB.Grid).ToElements()
    x_grids, y_grids = [], []
    for g in all_grids:
        curve = g.Curve
        if not isinstance(curve, DB.Line): continue
        direction = curve.Direction.Normalize()
        # If line is vertical (X-coordinate constant), it defines an X-position (column boundary)
        if abs(direction.X) < 0.001: x_grids.append(g)
        # If line is horizontal (Y-coordinate constant), it defines a Y-position (row boundary)
        elif abs(direction.Y) < 0.001: y_grids.append(g)
    
    # Sort X-grids by X-coordinate (Left to Right) / 按 X 座標排序（由左至右）
    x_grids.sort(key=lambda g: g.Curve.GetEndPoint(0).X)
    # Sort Y-grids by Y-coordinate (Bottom to Top) / 按 Y 座標排序（由下至上）
    y_grids.sort(key=lambda g: g.Curve.GetEndPoint(0).Y)
    return x_grids, y_grids

def is_primary_view(view):
    """ Check if the view is a primary view (not dependent) / 檢查視圖是否為母視圖（非從屬視圖） """
    if hasattr(view, "GetPrimaryViewId"):
        return view.GetPrimaryViewId() == DB.ElementId.InvalidElementId
    return True

def main():
    # 0. 功能前導說明 / Guided Intro
    forms.alert(
        "【視圖矩陣分割器】\n\n"
        "此工具將引導您執行以下操作：\n"
        "1. 選擇母視圖\n"
        "2. 選擇樣板（將會自動套用至所有生成的分割視圖）\n"
        "3. 設定分割範圍（網格座標）\n"
        "4. 自動建立圖紙與排版\n\n"
        "若準備好了請點選 OK 開始。",
        title="DependentSplit 使用引導"
    )

    # 1. 視圖多選 (加入預載邏輯)
    active_view = doc.ActiveView
    all_views_col = FilteredElementCollector(doc).OfClass(ViewPlan).WhereElementIsNotElementType()
    view_list = [v for v in all_views_col if not v.IsTemplate and is_primary_view(v)]
    view_list.sort(key=lambda x: x.Name)
    
    # 建立彈框實例以支援預先勾選
    view_form = forms.SelectFromList(view_list, name_attr='Name', title='[1/5] 勾選母視圖', multiselect=True)
    
    # 如果當前視圖在清單內，自動勾選
    if active_view in view_list:
        view_form.checked_elements = [active_view]
    
    if not view_form.show(): return
    selected_views = view_form.selected_elements

    # 2. 視圖樣板選擇 (加入預載邏輯)
    all_templates = FilteredElementCollector(doc).OfClass(ViewPlan).ToElements()
    template_list = [t for t in all_templates if t.IsTemplate]
    template_list.sort(key=lambda x: x.Name)
    
    # 偵測樣板預選：取第一個母視圖的樣板
    active_template_id = selected_views[0].ViewTemplateId if selected_views else ElementId.InvalidElementId
    active_template = doc.GetElement(active_template_id) if active_template_id != ElementId.InvalidElementId else None

    # 建立彈框實例
    temp_form = forms.SelectFromList(template_list, name_attr='Name', title='[2/5] 選擇視圖樣板 (可點取消視同不套用)')
    
    # 如果母視圖有樣板，自動預選
    if active_template:
        temp_form.selected_elements = [active_template]
    
    selected_template = temp_form.show()
    template_id = selected_template.Id if selected_template else ElementId.InvalidElementId

    # 3. 各別參數輸入 (穩定版)
    out = forms.ask_for_string(default='1000', title="[3/5] 外擴值 Offset (mm)")
    if not out: return
    
    x_start = forms.ask_for_string(default='1', title="[4/5] X 軸起始網格")
    x_end = forms.ask_for_string(default='5', title="[4/5] X 軸結束網格")
    x_step = forms.ask_for_string(default='2', title="[4/5] X 軸步長")
    if not x_step: return
    
    y_start = forms.ask_for_string(default='A', title="[5/5] Y 軸起始網格")
    y_end = forms.ask_for_string(default='E', title="[5/5] Y 軸結束網格")
    y_step = forms.ask_for_string(default='2', title="[5/5] Y 軸步長")
    if not y_step: return
    
    sh_num = forms.ask_for_string(default='C2-B02-D', title="圖紙參數: 號碼前綴")
    sh_name = forms.ask_for_string(default='平面分圖', title="圖紙參數: 名稱基礎")

    try:
        offset = float(out) / 304.8
        step_x, step_y = int(x_step), int(y_step)
    except:
        forms.alert("請確保數值欄位輸入皆為數字。")
        return

    # 4. 網格與座標解析
    x_grids, y_grids = get_sorted_grids()
    x_names, y_names = [g.Name for g in x_grids], [g.Name for g in y_grids]
    if any(n not in x_names for n in [x_start, x_end]) or any(n not in y_names for n in [y_start, y_end]):
        forms.alert("網格名稱錯誤或不存在。")
        return

    ix1, ix2 = x_names.index(x_start), x_names.index(x_end)
    if ix1 > ix2: ix1, ix2 = ix2, ix1
    iy1, iy2 = y_names.index(y_start), y_names.index(y_end)
    if iy1 > iy2: iy1, iy2 = iy2, iy1

    split_x = list(range(ix1, ix2, step_x))
    if ix2 not in split_x: split_x.append(ix2)
    split_y = list(range(iy1, iy2, step_y))
    if iy2 not in split_y: split_y.append(iy2)
    
    def get_x(i): return x_grids[i].Curve.GetEndPoint(0).X
    def get_y(i): return y_grids[i].Curve.GetEndPoint(0).Y

    tb = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_TitleBlocks).WhereElementIsElementType().FirstElementId()
    
    # 5. Batch Execution / 批次執行
    with revit.Transaction("Batch Matrix Split with Template"):
        for v_idx, parent_view in enumerate(selected_views):
            for r in range(len(split_y) - 1):
                for c in range(len(split_x) - 1):
                    try:
                        # Define Crop BoundingBox based on grid crossings / 依據網格交點定義裁切邊界框
                        v1x, v2x = get_x(split_x[c]), get_x(split_x[c+1])
                        v1y, v2y = get_y(split_y[r]), get_y(split_y[r+1])
                        
                        bbox = DB.BoundingBoxXYZ()
                        bbox.Min = DB.XYZ(min(v1x,v2x)-offset, min(v1y,v2y)-offset, -1)
                        bbox.Max = DB.XYZ(max(v1x,v2x)+offset, max(v1y,v2y)+offset, 1)
                        
                        # Create Dependent View / 建立從屬視圖
                        new_id = parent_view.Duplicate(DB.ViewDuplicateOption.AsDependent)
                        nv = doc.GetElement(new_id)
                        nv.Name = "{}-R{}-C{}".format(parent_view.Name, r+1, c+1)
                        nv.CropBox = bbox
                        nv.CropBoxActive = True
                        
                        # Apply View Template / 套用視圖樣板
                        if template_id != DB.ElementId.InvalidElementId:
                            nv.ViewTemplateId = template_id
                        
                        # Create corresponding Sheet / 建立對應圖紙
                        if tb:
                            sheet = DB.ViewSheet.Create(doc, tb)
                            sheet.SheetNumber = "{}-V{}-R{}-C{}".format(sh_num, v_idx+1, r+1, c+1)
                            sheet.Name = "{} ({}-{})".format(sh_name, r+1, c+1)
                            # Place Viewport on Sheet (Center offset) / 在圖紙上建立視埠 (偏移量調整)
                            DB.Viewport.Create(doc, sheet.Id, nv.Id, DB.XYZ(1.38, 0.97, 0))
                    except: pass
    forms.alert("樣板批次分割完成！ (Batch Matrix Split Completed)")

if __name__ == "__main__":
    main()
