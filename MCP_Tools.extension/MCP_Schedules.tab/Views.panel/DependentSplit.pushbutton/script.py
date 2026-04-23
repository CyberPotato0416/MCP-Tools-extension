# -*- coding: utf-8 -*-
"""
DependentSplit (視圖矩陣分割器)
Author: Jerry / Antigravity
Version: v1.0

Description / 功能簡介:
Matrix-based dependent view cropping with automatic sheet generation and template application.
依據網格交叉點精準裁切從屬視圖，並自動生成對應圖紙與套用視圖樣板。

Key Features / 關鍵功能:
- Grid-based Matrix Detection (自動網格矩陣偵測)
- Automatic Sheet & Viewport Creation (自動生成圖紙與視埠)
- View Template Application (批量套用視圖樣板)

How to Use / 使用說明:
1. Select primary parent views (選擇母視圖)
2. Choose a View Template (選擇視圖樣板)
3. Define Grid range and Offset (定義網格範圍與外擴值)
"""

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
    # 1. 視圖多選
    all_views_col = DB.FilteredElementCollector(doc).OfClass(DB.ViewPlan).WhereElementIsNotElementType()
    view_list = [v for v in all_views_col if not v.IsTemplate and is_primary_view(v)]
    view_list.sort(key=lambda x: x.Name)
    selected_views = forms.SelectFromList.show(
        view_list, name_attr='Name', title='[1/5] 勾選母視圖', multiselect=True
    )
    if not selected_views: return

    # 2. 視圖樣板選擇 (新增 Step)
    all_templates = DB.FilteredElementCollector(doc).OfClass(DB.ViewPlan).ToElements()
    template_list = [t for t in all_templates if t.IsTemplate]
    template_list.sort(key=lambda x: x.Name)
    
    selected_template = forms.SelectFromList.show(
        template_list, name_attr='Name', title='[2/5] 選擇視圖樣板 (可點取消視同不套用)'
    )
    template_id = selected_template.Id if selected_template else DB.ElementId.InvalidElementId

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
