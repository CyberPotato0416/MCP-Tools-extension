# -*- coding: utf-8 -*-
from pyrevit import revit, DB, forms


# ============================================================
# 🔒 Fixed Coordinates (From Debug Checklist) / 固定座標（來自調試檢查清單）
# These coordinates define specific areas for the "F2" project.
# 這些座標定義了 "F2" 專案中的特定分割區域。
# ============================================================

X_COORDS = [
    0.000, 29.528, 59.055, 86.614, 114.173, 141.732,
    169.291, 196.850, 224.409, 251.969, 279.528,
    307.087, 334.646, 362.205, 389.764, 417.323,
    456.693, 496.063, 523.622, 551.181, 578.740,
    606.299, 633.858, 661.417, 688.976, 716.535,
    744.094, 771.654, 799.213
]

Y_COORDS = [
    0.000, 49.213, 98.425, 147.638, 196.850, 246.063, 295.276
]


# ============================================================
# Main
# ============================================================

def main():
    doc = revit.doc
    origin_view = revit.active_view

    if not isinstance(origin_view, DB.ViewPlan):
        forms.alert("請在平面視圖中執行", title="錯誤")
        return

    step = 2                    # 每 2 條線一區
    offset = 1000.0 / 304.8     # 1000 mm
    part_index = 1

    with revit.Transaction("Create Partition Views (By Coords)"):

        # Vertical iteration (Y-axis outer layer) / 上下迭代（Y 軸外層）
        for yi in range(0, len(Y_COORDS) - step, step):
            y1, y2 = Y_COORDS[yi], Y_COORDS[yi + step]

            # Horizontal iteration (X-axis inner layer) / 左右迭代（X 軸內層）
            for xi in range(0, len(X_COORDS) - step, step):
                x1, x2 = X_COORDS[xi], X_COORDS[xi + step]

                # Create Dependent View / 建立從屬視圖
                dep_id = origin_view.Duplicate(
                    DB.ViewDuplicateOption.AsDependent
                )
                dep_view = doc.GetElement(dep_id)
                dep_view.Name = "{}-分區{}".format(
                    origin_view.Name,
                    part_index
                )

                # Set Bounding Box Based on Fixed Coords / 依據固定座標設置邊界框
                bbox = DB.BoundingBoxXYZ()
                bbox.Min = DB.XYZ(
                    min(x1, x2) - offset,
                    min(y1, y2) - offset,
                    -10
                )
                bbox.Max = DB.XYZ(
                    max(x1, x2) + offset,
                    max(y1, y2) + offset,
                    10
                )

                dep_view.CropBox = bbox
                dep_view.CropBoxActive = True
                dep_view.CropBoxVisible = True

                part_index += 1

    forms.alert(
        "切割完成（硬座標模式），共建立 {} 個分區視圖 / Partition Split Completed (Fixed Coords), {} views created".format(part_index - 1, part_index - 1),
        title="完成 / Finished"
    )


if __name__ == "__main__":
    main()
