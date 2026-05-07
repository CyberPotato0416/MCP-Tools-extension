# -*- coding: utf-8 -*-
__title__  = "Pipe Settings"
__author__ = "Jerry / Antigravity"
__doc__    = "Configure your 5 favorite pipe types for quick one-click modeling. Supports empty slots for small projects."

from pyrevit import revit, DB, forms
import os
import sys

# Nested inside Pipes_B.stack -> 5 levels up to reach MCP_Tools.extension/lib
lib_path = os.path.join(
    os.path.dirname(
    os.path.dirname(
    os.path.dirname(
    os.path.dirname(
    os.path.dirname(__file__))))), "lib")
if lib_path not in sys.path:
    sys.path.append(lib_path)

import quick_access

doc = revit.doc
EMPTY_LABEL = "<-- Leave Empty -->"

def select_pipe_types():
    # 取得專案中所有管材類型
    pipe_types = DB.FilteredElementCollector(doc).OfClass(DB.Plumbing.PipeType).ToElements()
    type_names = sorted([
        pt.get_Parameter(DB.BuiltInParameter.SYMBOL_NAME_PARAM).AsString()
        for pt in pipe_types
    ])

    if not type_names:
        forms.alert("No pipe types found in this project!", title="Error")
        return

    # 讀取目前的設定
    current_config = quick_access.get_config()
    current_favorites = current_config.get("pipe_types", [None] * 5)
    # 確保長度為 5
    while len(current_favorites) < 5:
        current_favorites.append(None)

    new_favorites = []

    for i in range(5):
        # 每一輪都用完整的 type_names，再加上空白選項
        # 讓使用者可以重複選同一個，或選擇留空
        options = [EMPTY_LABEL] + type_names

        # 預設選項
        current_val = current_favorites[i]
        if current_val and current_val in type_names:
            default = current_val
        else:
            default = EMPTY_LABEL

        selected = forms.SelectFromList.show(
            options,
            title="Pipe Button {} / 5  (select '{}' to leave empty)".format(i + 1, EMPTY_LABEL),
            button_name="Confirm",
            multiselect=False,
            default=default
        )

        # 使用者按 X 關閉視窗 → 視為放棄此輪，保持原設定
        if selected is None:
            new_favorites.append(current_val)
        elif selected == EMPTY_LABEL:
            new_favorites.append(None)
        else:
            new_favorites.append(selected)

    # 儲存設定
    quick_access.save_config({"pipe_types": new_favorites})

    # 同步更新 Ribbon 按鈕名稱
    quick_access.update_ribbon_titles()

    # 顯示確認結果
    summary_lines = []
    for idx, name in enumerate(new_favorites):
        label = name if name else "(empty)"
        summary_lines.append("Pipe {}: {}".format(idx + 1, label))

    forms.alert(
        "Configuration saved!\n\n" + "\n".join(summary_lines),
        title="Quick Pipe Settings"
    )

if __name__ == "__main__":
    select_pipe_types()
