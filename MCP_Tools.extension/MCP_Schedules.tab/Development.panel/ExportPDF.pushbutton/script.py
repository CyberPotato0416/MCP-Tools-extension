# -*- coding: utf-8 -*-
__title__ = "PDF導出\n(Native)"
__doc__ = "利用 Revit 2024 原生 API 導出當前圖紙為 PDF。不需安裝虛擬印表機。"

from pyrevit import revit, DB, forms
import os

doc = revit.doc
view = revit.active_view

def export_active_sheet_to_pdf():
    # 1. 檢查是否為圖紙
    if not isinstance(view, DB.ViewSheet):
        forms.alert("當前視圖不是圖紙 (Sheet)！\n請切換到要導出的圖紙再執行。", title="視圖錯誤")
        return

    # 2. 設定輸出路徑 (預設桌面)
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    output_folder = os.path.join(desktop, "Revit_PDF_Export")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    file_name = "{}_{}".format(view.SheetNumber, view.Name)
    # 移除檔名非法字元
    for char in ['<', '>', ':', '"', '/', '\\', '|', '?', '*']:
        file_name = file_name.replace(char, "_")

    # 3. 配置 PDF 導出選項 (Revit 2022+ New API)
    options = DB.PDFExportOptions()
    options.FileName = file_name
    options.Combine = True
    options.StopOnError = False
    options.AlwaysUseRaster = False # 盡量使用向量輸出
    options.RasterQuality = DB.RasterQualityType.High
    options.ExportQuality = DB.PDFExportQualityType.DPI300
    options.HideCropBoundaries = True
    options.HideReferencePlanes = True
    options.HideUnreferencedViewTags = True
    
    # 設定圖紙大小 (自動偵測)
    options.PaperFormat = DB.ExportPaperFormat.Default
    
    # 4. 執行導出
    try:
        from System.Collections.Generic import List
        view_ids = List[DB.ElementId]()
        view_ids.Add(view.Id)

        with revit.Transaction("Export PDF (Native)"):
            doc.Export(output_folder, view_ids, options)
        
        forms.toast("PDF 導出成功！\n儲存路徑: " + output_folder)
        # 自動打開資料夾
        os.startfile(output_folder)

    except Exception as e:
        forms.alert("導出失敗：\n" + str(e))

if __name__ == "__main__":
    export_active_sheet_to_pdf()
