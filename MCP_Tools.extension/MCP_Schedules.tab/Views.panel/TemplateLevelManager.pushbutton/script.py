# -*- coding: utf-8 -*-
__title__  = "TemplateLevelManager"
__author__ = "Jerry / Antigravity"
__doc__    = "Batch manage level visibility across multiple view templates with domain/type filtering and JSON state memory."


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
        
        # 1. Collect only valid Graphical View Templates (that can have Levels/Discipline)
        valid_types = [ViewType.FloorPlan, ViewType.CeilingPlan, ViewType.Elevation, ViewType.Section, ViewType.ThreeD]
        self._all_templates = [v for v in FilteredElementCollector(self._doc).OfClass(View).ToElements() 
                               if v.IsTemplate and v.ViewType in valid_types]
        self._all_templates.sort(key=lambda x: x.Name)

        # 2. Collect unique filter options safely
        disciplines_set = set()
        view_types_set = set()
        for t in self._all_templates:
            try:
                disciplines_set.add(str(t.Discipline))
            except: pass
            try:
                view_types_set.add(str(t.ViewType))
            except: pass

        self._disciplines = sorted(list(disciplines_set))
        self._view_types = sorted(list(view_types_set))

        # 3. Setup UI and Filter logic
        self.setup_ui_filters()
        self.load_config()

    def setup_ui_filters(self):
        # Filter options
        filter_data = {
            "disciplines": ["<全部>"] + self._disciplines,
            "types": ["<全部>"] + self._view_types
        }

        for i in range(1, 4):
            # Populate Filter Combos
            disc_combo = getattr(self, "Tab{}_DisciplineFilter".format(i))
            type_combo = getattr(self, "Tab{}_TypeFilter".format(i))
            
            disc_combo.ItemsSource = filter_data["disciplines"]
            disc_combo.SelectedIndex = 0
            
            type_combo.ItemsSource = filter_data["types"]
            type_combo.SelectedIndex = 0

            # Levels
            levels = FilteredElementCollector(self._doc).OfClass(Level).ToElements()
            tab_levels = sorted([LevelItem(l) for l in levels], key=lambda x: x.Name)
            listbox = getattr(self, "Tab{}_LevelList".format(i))
            listbox.ItemsSource = tab_levels

            # Initial Template Population
            self.refresh_template_list(i)

    def OnFilterChanged(self, sender, e):
        # Find which tab triggered this (Name follows "TabX_...")
        sender_name = sender.Name
        try:
            tab_num = int(sender_name[3]) # Extract '1', '2' or '3'
            self.refresh_template_list(tab_num)
        except:
            pass

    def refresh_template_list(self, tab_num):
        disc_filter = getattr(self, "Tab{}_DisciplineFilter".format(tab_num)).SelectedItem
        type_filter = getattr(self, "Tab{}_TypeFilter".format(tab_num)).SelectedItem
        combo = getattr(self, "Tab{}_TemplateCombo".format(tab_num))

        # Filter the master list
        filtered = self._all_templates
        if disc_filter and disc_filter != "<全部>":
            filtered = [t for t in filtered if str(t.Discipline) == disc_filter]
        if type_filter and type_filter != "<全部>":
            filtered = [t for t in filtered if str(t.ViewType) == type_filter]

        # Preserve selection if it's already in the filtered results
        current_sel = combo.SelectedItem
        combo.ItemsSource = filtered
        
        if current_sel:
            for item in filtered:
                if item.Id == current_sel.Id:
                    combo.SelectedItem = item
                    break

    def load_config(self):
        active_template_id = self._doc.ActiveView.ViewTemplateId
        active_template = self._doc.GetElement(active_template_id) if active_template_id != ElementId.InvalidElementId else None

        if os.path.exists(self._config_path):
            try:
                with io.open(self._config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    
                for i in range(1, 4):
                    tab_data = config.get("tab_{}".format(i))
                    combo = getattr(self, "Tab{}_TemplateCombo".format(i))
                    disc_filter_combo = getattr(self, "Tab{}_DisciplineFilter".format(i))
                    type_filter_combo = getattr(self, "Tab{}_TypeFilter".format(i))
                    
                    if tab_data:
                        # 1. Restore Filters first
                        saved_disc = tab_data.get("discipline_filter", "<全部>")
                        saved_type = tab_data.get("view_type_filter", "<全部>")
                        
                        disc_filter_combo.SelectedItem = saved_disc
                        type_filter_combo.SelectedItem = saved_type
                        
                        # 2. Refresh List based on restored filters
                        self.refresh_template_list(i)
                        
                        # 3. Set Enabled
                        getattr(self, "Tab{}_Enabled".format(i)).IsChecked = tab_data.get("enabled", False)
                        
                        # 4. Set Template from config
                        template_name = tab_data.get("template_name")
                        target_template = None
                        for t in self._all_templates:
                            if t.Name == template_name:
                                target_template = t
                                break
                        
                        if target_template:
                            # Even if filtered out by current UI state, we ensure it's selectable during load
                            # (The UI state was just restored above, so it SHOULD be in there, but as safety:)
                            if target_template not in combo.ItemsSource:
                                combo.ItemsSource = self._all_templates
                            combo.SelectedItem = target_template
                            
                        # 5. Set Levels from config
                        keep_levels = tab_data.get("keep_levels", [])
                        listbox = getattr(self, "Tab{}_LevelList".format(i))
                        for item in listbox.ItemsSource:
                            if item.Name in keep_levels:
                                item.IsChecked = True
                    
                    # Pre-select Active View Template for Tab 1 if nothing selected yet
                    # 如果 Tab 1 還沒選樣板，且當前視圖有樣板，則預先導入
                    if i == 1 and not combo.SelectedItem and active_template:
                        for item in combo.ItemsSource:
                            if item.Id == active_template.Id:
                                combo.SelectedItem = item
                                break
            except:
                pass
        else:
            # First time running: Pre-select Active View Template for Tab 1
            if active_template:
                combo = getattr(self, "Tab1_TemplateCombo")
                for item in combo.ItemsSource:
                    if item.Id == active_template.Id:
                        combo.SelectedItem = item
                        break

    def OnSaveAndApply(self, sender, e):
        config = {}
        processed_templates = []

        with revit.Transaction("Batch Update Template Levels"):
            for i in range(1, 4):
                is_enabled = getattr(self, "Tab{}_Enabled".format(i)).IsChecked
                template = getattr(self, "Tab{}_TemplateCombo".format(i)).SelectedItem
                listbox = getattr(self, "Tab{}_LevelList".format(i))
                keep_names = [item.Name for item in listbox.ItemsSource if item.IsChecked]

                # Get Current Filters / 取得當前篩選器值
                disc_val = getattr(self, "Tab{}_DisciplineFilter".format(i)).SelectedItem
                type_val = getattr(self, "Tab{}_TypeFilter".format(i)).SelectedItem

                # Save to config dict
                config["tab_{}".format(i)] = {
                    "enabled": is_enabled,
                    "template_name": template.Name if template else None,
                    "discipline_filter": disc_val,
                    "view_type_filter": type_val,
                    "keep_levels": keep_names
                }

                # Apply to Revit if enabled
                if is_enabled and template:
                    view_count = self.apply_to_template(template, keep_names)
                    processed_templates.append("{} ({} 張視圖)".format(template.Name, view_count))

        # Save config file
        with io.open(self._config_path, 'w', encoding='utf-8') as f:
            f.write(unicode(json.dumps(config, ensure_ascii=False, indent=4)))

        if processed_templates:
            forms.alert("處理完成！\n已更新樣板：\n" + "\n".join(processed_templates), title="完成")
        else:
            forms.alert("沒有啟用的樣板需要更新。", title="完成")
        self.Close()

    def apply_to_template(self, template, keep_names):
        """
        Apply level isolation to all views currently using the selected template.
        
        [Why this approach / 為什麼這樣設計]:
        Revit API does not propagate individual element-level Hide/Unhide set on the
        View Template itself to child views. Instead, we find all views currently
        using this template and apply the isolation directly to each view.
        This mirrors the proven logic of the IsolateLevels button.
        
        Revit API 的元素級別隱藏設定在「視圖樣板」上，不會自動同步到使用該樣板的子視圖。
        因此改為直接對所有使用此樣板的視圖執行。
        """
        all_levels = FilteredElementCollector(self._doc).OfClass(Level).ToElements()
        
        ids_to_hide = List[ElementId]()
        ids_to_unhide = List[ElementId]()
        
        for lvl in all_levels:
            if lvl.Name in keep_names:
                ids_to_unhide.Add(lvl.Id)
            else:
                ids_to_hide.Add(lvl.Id)
        
        # Find all views using this template / 找出所有套用此樣板的視圖
        all_views = FilteredElementCollector(self._doc).OfClass(View).ToElements()
        target_views = [v for v in all_views 
                        if not v.IsTemplate 
                        and v.ViewTemplateId == template.Id]
        
        count = 0
        for view in target_views:
            try:
                if ids_to_unhide.Count > 0:
                    view.UnhideElements(ids_to_unhide)
                if ids_to_hide.Count > 0:
                    view.HideElements(ids_to_hide)
                count += 1
            except:
                pass  # Skip views that can't be modified
        
        return count  # Return number of views updated for feedback

    def OnCancel(self, sender, e):
        self.Close()

if __name__ == "__main__":
    TemplateLevelManager().show_dialog()
