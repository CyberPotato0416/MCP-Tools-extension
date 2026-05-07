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

    # 2. 設定輸出路徑
    date_str = datetime.datetime.now().strftime("%y%m%d")
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    output_folder = os.path.join(desktop, "Revit_PDF_" + date_str)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 檔名合法化 (參考大神邏輯)
    def legalize_name(name):
        for char in ['<', '>', ':', '"', '/', '\\', '|', '?', '*']:
            name = name.replace(char, "_")
        return name

    sheet_name = legalize_name("{}_{}".format(view.SheetNumber, view.Name))

    # 3. 配置 PDF 導出選項 (Revit 2022+ API 精確屬性)
    options = DB.PDFExportOptions()
    options.FileName = sheet_name
    options.Combine = True
    options.StopOnError = False
    options.AlwaysUseRaster = False
    options.RasterQuality = DB.RasterQualityType.High
    options.ExportQuality = DB.PDFExportQualityType.DPI300
    options.HideCropBoundaries = True
    options.HideRefPlanes = True # 修正為正確的 API 名稱
    options.HideUnreferencedViewTags = True
    
    # 4. 執行導出 (背景執行，不需切換視圖)
    try:
        from System.Collections.Generic import List
        view_ids = List[DB.ElementId]()
        view_ids.Add(view.Id)

        # 導出不一定需要 Transaction，但為了安全起見包裹在 Transaction 中
        with revit.Transaction("Export PDF"):
            doc.Export(output_folder, view_ids, options)
        
        forms.toast("PDF 導出成功！\n" + sheet_name)
        # 僅在第一次導出時打開資料夾
        os.startfile(output_folder)

    except Exception as e:
        forms.alert("導出失敗：\n" + str(e))

if __name__ == "__main__":
    # 加入時間模組
    import datetime
    export_active_sheet_to_pdf()
