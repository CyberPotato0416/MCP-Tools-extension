# -*- coding: utf-8 -*-
from pyrevit import revit, DB

doc = revit.doc
selection = revit.get_selection()

for el in selection:
    if isinstance(el, DB.Viewport):
        outline = el.GetBoxOutline()
        width = (outline.Max.X - outline.Min.X) * 304.8  # 轉公釐
        height = (outline.Max.Y - outline.Min.Y) * 304.8 # 轉公釐
        print("視埠 ID: {}".format(el.Id))
        print("視埠圖面尺寸: {:.2f} mm x {:.2f} mm".format(width, height))
        print("視埠中心座標: {}".format(el.GetBoxCenter()))
    
    if el.Category and el.Category.Id.IntegerValue == int(DB.BuiltInCategory.OST_TitleBlocks):
        bbox = el.get_BoundingBox(None)
        width = (bbox.Max.X - bbox.Min.X) * 304.8
        height = (bbox.Max.Y - bbox.Min.Y) * 304.8
        print("圖框 ID: {}".format(el.Id))
        print("圖紙總尺寸: {:.2f} mm x {:.2f} mm".format(width, height))
