# -*- coding: utf-8 -*-
from pyrevit import revit, DB, forms
import os

def get_sorted_grids():
    """ 
    Retrieve and sort grids for U1U3/UCUE specific layout.
    獲取並排序網格，專用於 U1U3/UCUE 特定配置。
    """
    all_grids = DB.FilteredElementCollector(revit.doc).OfClass(DB.Grid).ToElements()
    x_grids, y_grids = [], []
    for g in all_grids:
        curve = g.Curve
        if not isinstance(curve, DB.Line):
            continue
        d = curve.Direction.Normalize()
        # Classify by normalized direction / 依據標準化方向進行分類
        if abs(d.X) < 0.001:
            x_grids.append(g)
        elif abs(d.Y) < 0.001:
            y_grids.append(g)

    # Sort to ensure sequential partitioning / 進行排序以確保視圖分區依序排列
    x_grids.sort(key=lambda g: min(g.Curve.GetEndPoint(0).X, g.Curve.GetEndPoint(1).X))
    y_grids.sort(key=lambda g: min(g.Curve.GetEndPoint(0).Y, g.Curve.GetEndPoint(1).Y))
    return x_grids, y_grids

def main():
    doc = revit.doc
    origin_view = revit.active_view
    if origin_view is None or not isinstance(origin_view, DB.ViewPlan):
        forms.alert("目前的激活視圖無效或不是平面視圖，請切換到有效的平面視圖後再試。", title="錯誤")
        return

    x_grids, y_grids = get_sorted_grids()
    if not x_grids or not y_grids:
        forms.alert("無法找到任何網格，請確認是否存在網格。", title="錯誤")
        return

    x_coords = [g.Curve.Evaluate(0.5, True).X for g in x_grids]
    y_coords = [g.Curve.Evaluate(0.5, True).Y for g in y_grids]

    x_start, x_end = x_coords[0], x_coords[-1]
    y_start, y_end = y_coords[0], y_coords[-1]

    x_increment = 2     # Defines the grid step for each partition / 定義每個分區跨越的網格數量
    partition_count = 1

    # Vertical stripping logic (Split by X-coordinates) / 垂直長條分割邏輯 (依 X 座標分割)
    for x in range(0, len(x_coords) - x_increment, x_increment):
        x1, x2 = x_coords[x], x_coords[x + x_increment]
        with revit.Transaction("Split View Partition {}".format(partition_count)):
            # Duplicate view as Dependent / 複製視圖為從屬視圖
            dep_id = origin_view.Duplicate(DB.ViewDuplicateOption.AsDependent)
            dep_view = doc.GetElement(dep_id)
            dep_view.Name = "{}-分區{}".format(origin_view.Name, partition_count)

            # Set BoundingBox to cover full height and specified width / 設置邊界框覆蓋全高與指定寬度
            bbox = DB.BoundingBoxXYZ()
            bbox.Min = DB.XYZ(x1, y_start, -10)
            bbox.Max = DB.XYZ(x2, y_end, 10)
            dep_view.CropBox = bbox
            dep_view.CropBoxActive = True
            dep_view.CropBoxVisible = True

        partition_count += 1

    forms.alert("切割完成，已建立 {} 個分區視圖。 / Split Completed, {} partition views created.".format(partition_count - 1, partition_count - 1), title="完成 / Finished")

if __name__ == '__main__':
    main()

