# -*- coding: utf-8 -*-
__title__ = "零件自動出圖\n(Part Doc)"
__doc__ = "選取零件後自動建立組件視圖與圖紙 (三視圖 + 3D)，具備自動幾何判定與視覺標準控制。"

from pyrevit import revit, DB, forms
import math

# 初始化文件與選取
doc = revit.doc
uidoc = revit.uidoc
selection = revit.get_selection()

def get_assembly_geom_extents(assembly_inst):
    """計算組件內所有成員幾何的聯集 BoundingBox"""
    member_ids = assembly_inst.GetMemberIds()
    union_bbox = None
    
    for mid in member_ids:
        el = doc.GetElement(mid)
        # 取得幾何資訊
        opt = DB.Options()
        geom = el.get_Geometry(opt)
        if not geom: continue
        
        bbox = el.get_BoundingBox(None)
        if not bbox: continue
        
        if union_bbox is None:
            union_bbox = DB.BoundingBoxXYZ()
            union_bbox.Min = bbox.Min
            union_bbox.Max = bbox.Max
        else:
            union_bbox.Min = DB.XYZ(
                min(union_bbox.Min.X, bbox.Min.X),
                min(union_bbox.Min.Y, bbox.Min.Y),
                min(union_bbox.Min.Z, bbox.Min.Z)
            )
            union_bbox.Max = DB.XYZ(
                max(union_bbox.Max.X, bbox.Max.X),
                max(union_bbox.Max.Y, bbox.Max.Y),
                max(union_bbox.Max.Z, bbox.Max.Z)
            )
    return union_bbox

def create_part_documentation():
    if not selection:
        forms.alert("請先選取至少一個零件元件！", title="未選取物件")
        return

    # 1. 取得物件與品類
    valid_ids = [eid for eid in selection.element_ids if doc.GetElement(eid).Category]
            
    if not valid_ids:
        forms.alert("選取的物件不包含有效的實體品類。")
        return

    main_el = doc.GetElement(valid_ids[0])
    category_id = main_el.Category.Id
    
    from System.Collections.Generic import List
    typed_ids = List[DB.ElementId](valid_ids)

    # 2. 開始交易
    with revit.Transaction("Auto Part Documentation (Advanced)"):
        try:
            # 建立組件 (Assembly)
            if main_el.AssemblyInstanceId == DB.ElementId.InvalidElementId:
                assembly_inst = DB.AssemblyInstance.Create(doc, typed_ids, category_id)
                doc.Regenerate()
                base_name = main_el.Name
                assembly_inst.AssemblyTypeName = "零件-" + base_name
            else:
                assembly_inst = doc.GetElement(main_el.AssemblyInstanceId)
                base_name = assembly_inst.AssemblyTypeName

            # 3. 幾何分析與比例計算
            bbox = get_assembly_geom_extents(assembly_inst)
            if bbox:
                size_x = (bbox.Max.X - bbox.Min.X) * 304.8
                size_y = (bbox.Max.Y - bbox.Min.Y) * 304.8
                size_z = (bbox.Max.Z - bbox.Min.Z) * 304.8
                max_dim = max(size_x, size_y, size_z)
                target_scale = int(math.ceil(max_dim / 150.0 / 5.0) * 5)
                if target_scale < 1: target_scale = 1
            else:
                target_scale = 20

            # 4. 建立詳細視圖
            view_types = {
                "Plan": DB.AssemblyDetailViewOrientation.HorizontalDetail,
                "Front": DB.AssemblyDetailViewOrientation.ElevationFront,
                "Side": DB.AssemblyDetailViewOrientation.ElevationRight,
                "3D": DB.AssemblyDetailViewOrientation.Isometric
            }
            
            created_views = {}
            for name, orient in view_types.items():
                v = DB.AssemblyDetailViewBuilder.CreateDetailView(doc, assembly_inst.Id, orient)
                v.Name = "Assembly_" + name + "_" + base_name + "_" + str(assembly_inst.Id.IntegerValue)
                v.DetailLevel = DB.ViewDetailLevel.Fine
                if orient == DB.AssemblyDetailViewOrientation.Isometric:
                    v.get_Parameter(DB.BuiltInParameter.MODEL_GRAPHICS_STYLE).Set(3)
                else:
                    v.get_Parameter(DB.BuiltInParameter.MODEL_GRAPHICS_STYLE).Set(2)
                
                v.Scale = target_scale
                created_views[name] = v

            # 5. 建立圖紙
            tblock = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_TitleBlocks).FirstElement()
            sheet = DB.ViewSheet.Create(doc, tblock.Id)
            sheet.Name = "零件圖-" + base_name
            sheet.SheetNumber = "P-" + str(assembly_inst.Id.IntegerValue)[-4:]

            # 6. 擺放視圖
            locs = {
                "Plan": DB.XYZ(0.5, 0.4, 0),
                "Front": DB.XYZ(1.3, 0.4, 0),
                "Side": DB.XYZ(2.1, 0.4, 0),
                "3D": DB.XYZ(2.0, 1.3, 0)
            }
            
            for name, view in created_views.items():
                DB.Viewport.Create(doc, sheet.Id, view.Id, locs[name])

            forms.toast("自動出圖完成！\n比例: 1/{}\n圖紙: {}".format(target_scale, sheet.SheetNumber))
            revit.uidoc.ActiveView = sheet

        except Exception as e:
            forms.alert("執行過程中發生錯誤：\n" + str(e))

if __name__ == "__main__":
    create_part_documentation()
