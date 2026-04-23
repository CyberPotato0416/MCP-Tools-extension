# -*- coding: utf-8 -*-
"""
Crop Box +500mm Grid Adjuster (裁切框網格調整器)
Author: Jerry / Antigravity
Description / 功能簡介:
Automatically adjusts Grid end points to be 500mm outside the current View Crop Box.
自動將網格端點調整至視圖裁切框外 500mm 處。
"""
from Autodesk.Revit.DB import *
from pyrevit import revit, script

doc = revit.doc
view = doc.ActiveView

# Define offset: 500mm to feet (Revit Internal Unit) / 定義偏移量：500mm 轉為英呎
OFFSET_MM = 500
OFFSET_FT = OFFSET_MM / 304.8  # mm → feet

# Get current Crop Box boundaries / 獲取當前裁切框邊界
crop = view.CropBox
xmin, xmax = crop.Min.X, crop.Max.X
ymin, ymax = crop.Min.Y, crop.Max.Y

# Collect grids visible in current view / 收集當前視圖中可見的網格
collector = FilteredElementCollector(doc, view.Id)\
    .OfCategory(BuiltInCategory.OST_Grids)\
    .WhereElementIsNotElementType()

with revit.Transaction("Move Grid Head to Crop Boundary"):
    for grid in collector:
        curve = grid.Curve
        if not isinstance(curve, Line):
            continue

        p0 = curve.GetEndPoint(0)
        p1 = curve.GetEndPoint(1)

        # Determine direction: vertical or horizontal / 判斷網格方向：垂直或水平
        is_vertical = abs(p0.X - p1.X) < abs(p0.Y - p1.Y)

        if is_vertical:
            # Vertical Grid → Move p0/p1 along Y axis / 垂直網格 → 沿 Y 軸移動端點
            new_p0 = XYZ(p0.X, ymin - OFFSET_FT, p0.Z)
            new_p1 = XYZ(p1.X, ymax + OFFSET_FT, p1.Z)
        else:
            # Horizontal Grid → Move p0/p1 along X axis / 水平網格 → 沿 X 軸移動端點
            new_p0 = XYZ(xmin - OFFSET_FT, p0.Y, p0.Z)
            new_p1 = XYZ(xmax + OFFSET_FT, p1.Y, p1.Z)

        # Update grid placement in view / 更新網格在視圖中的位置線
        new_line = Line.CreateBound(new_p0, new_p1)
        grid.SetCurveInView(DatumExtentType.ViewSpecific, view, new_line)
