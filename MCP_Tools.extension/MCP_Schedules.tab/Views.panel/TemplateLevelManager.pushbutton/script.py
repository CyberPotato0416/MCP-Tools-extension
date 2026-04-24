# -*- coding: utf-8 -*-
"""
TemplateLevelManager (樣板樓層管理)
Author: Jerry / Antigravity

[Design Intent / 開發動機]:
An advanced multi-tab management tool for Revit View Templates. 
Allows defining custom level whitelists per template. 
Highly flexible and bridges the gap in native View Template functionality.
此為高級多頁籤管理工具，用於設定各視圖樣板的專屬樓層白名單。
實現樣板層級的動態過濾，提供高度靈活性。
"""

import os
import json
import io
from Autodesk.Revit.DB import *
from pyrevit import revit, forms, script
from System.Collections.Generic import List

# Path to the XAML file
XAML_FILE = os.path.join(os.path.dirname(__file__), "ui.xaml")

class LevelItem:
    def __init__(self, level):
        self.Name = level.Name
        self.Id = level.Id
        self.IsChecked = False

class TemplateLevelManager(forms.WPFWindow):
    def __init__(self):
        forms.WPFWindow.__init__(self, XAML_FILE)
        self.title = "樣板樓層管理工具"
        self.Width = 400
        self.Height = 500
        
        self._doc = revit.doc
        self._config_path = os.path.join(os.path.dirname(__file__), "template_config.json")
        
        # Initialize Data / 初始化數據
        self.setup_ui()
        self.load_config()

    def setup_ui(self):
        # 1. Get View Templates / 獲取視圖樣板
        all_views = FilteredElementCollector(self._doc).OfClass(View).ToElements()
        templates = sorted([v for v in all_views if v.IsTemplate], key=lambda x: x.Name)
        
        # 2. Get Levels / 獲取樓層
        levels = FilteredElementCollector(self._doc).OfClass(Level).ToElements()
        self.level_items = sorted([LevelItem(l) for l in levels], key=lambda x: x.Name)

        # 3. Bind to Tabs / 綁定到各個頁籤
        for i in range(1, 4):
            combo = getattr(self, "Tab{}_TemplateCombo".format(i))
            combo.ItemsSource = templates
            
            # Note: ListBox binding is simpler via code here
            listbox = getattr(self, "Tab{}_LevelList".format(i))
            # Create unique copies of level items for each tab / 為各頁籤建立獨立的樓層物件複本
            tab_levels = [LevelItem(l) for l in sorted(levels, key=lambda x: x.Name)]
            listbox.ItemsSource = tab_levels

    def load_config(self):
        if os.path.exists(self._config_path):
            try:
                with io.open(self._config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    
                for i in range(1, 4):
                    tab_data = config.get("tab_{}".format(i))
                    if tab_data:
                        # Set Enabled
                        getattr(self, "Tab{}_Enabled".format(i)).IsChecked = tab_data.get("enabled", False)
                        # Set Template
                        template_name = tab_data.get("template_name")
                        combo = getattr(self, "Tab{}_TemplateCombo".format(i))
                        for item in combo.ItemsSource:
                            if item.Name == template_name:
                                combo.SelectedItem = item
                                break
                        # Set Levels
                        keep_levels = tab_data.get("keep_levels", [])
                        listbox = getattr(self, "Tab{}_LevelList".format(i))
                        for item in listbox.ItemsSource:
                            if item.Name in keep_levels:
                                item.IsChecked = True
            except:
                pass

    def OnSaveAndApply(self, sender, e):
        config = {}
        processed_templates = []

        with revit.Transaction("Batch Update Template Levels"):
            for i in range(1, 4):
                is_enabled = getattr(self, "Tab{}_Enabled".format(i)).IsChecked
                template = getattr(self, "Tab{}_TemplateCombo".format(i)).SelectedItem
                listbox = getattr(self, "Tab{}_LevelList".format(i))
                keep_names = [item.Name for item in listbox.ItemsSource if item.IsChecked]

                # Save to config dict
                config["tab_{}".format(i)] = {
                    "enabled": is_enabled,
                    "template_name": template.Name if template else None,
                    "keep_levels": keep_names
                }

                # Apply to Revit if enabled
                if is_enabled and template:
                    self.apply_to_template(template, keep_names)
                    processed_templates.append(template.Name)

        # Save config file
        with io.open(self._config_path, 'w', encoding='utf-8') as f:
            f.write(unicode(json.dumps(config, ensure_ascii=False, indent=4)))

        forms.alert("處理完成！\n已更新樣板：\n" + "\n".join(processed_templates), title="完成")
        self.Close()

    def apply_to_template(self, template, keep_names):
        # 1. Get visible levels in template (ViewTemplates are Views)
        # Note: FilteredElementCollector on a template works!
        visible_level_ids = [l.Id for l in FilteredElementCollector(self._doc, template.Id).OfClass(Level)]
        all_levels = FilteredElementCollector(self._doc).OfClass(Level).ToElements()

        ids_to_hide = List[ElementId]()
        ids_to_unhide = List[ElementId]()

        for lvl in all_levels:
            name = lvl.Name
            is_visible = lvl.Id in visible_level_ids
            
            if name in keep_names:
                if not is_visible:
                    ids_to_unhide.Add(lvl.Id)
            else:
                if is_visible:
                    ids_to_hide.Add(lvl.Id)

        if ids_to_hide.Count > 0:
            template.HideElements(ids_to_hide)
        if ids_to_unhide.Count > 0:
            template.UnhideElements(ids_to_unhide)

    def OnCancel(self, sender, e):
        self.Close()

if __name__ == "__main__":
    TemplateLevelManager().show_dialog()
