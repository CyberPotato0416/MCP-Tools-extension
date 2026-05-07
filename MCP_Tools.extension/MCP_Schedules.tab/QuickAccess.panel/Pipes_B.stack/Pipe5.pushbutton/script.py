# -*- coding: utf-8 -*-
# Dynamic title: reads saved pipe type name from config on each Reload
import os, sys as _sys

_lib = os.path.join(
    os.path.dirname(
    os.path.dirname(
    os.path.dirname(
    os.path.dirname(
    os.path.dirname(__file__))))), "lib")
if _lib not in _sys.path:
    _sys.path.append(_lib)

try:
    import quick_access as _qa
    _name = _qa.get_pipe_type_name(4)
    __title__  = _name if _name else "Pipe 5"
except Exception:
    __title__  = "Pipe 5"

__author__ = "Jerry / Antigravity"
__doc__    = "Switch to your predefined favorite pipe type and immediately activate the Draw Pipe command."

from pyrevit import revit, DB, forms
import os
import sys

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
uidoc = revit.uidoc
pipe_index = 4

def place_favorite_pipe():
    target_type_name = quick_access.get_pipe_type_name(pipe_index)

    if not target_type_name:
        forms.alert(
            "Pipe 5 is not configured yet.\nPlease click the Settings button to set up your favorite pipe types.",
            title="Quick Pipe"
        )
        return

    collector = DB.FilteredElementCollector(doc).OfClass(DB.Plumbing.PipeType).WhereElementIsElementType()
    pipe_type = next(
        (pt for pt in collector
         if pt.get_Parameter(DB.BuiltInParameter.SYMBOL_NAME_PARAM).AsString() == target_type_name),
        None
    )

    if not pipe_type:
        forms.alert(
            "Pipe type \'{0}\' not found in this project.\nPlease reconfigure via Settings.".format(target_type_name),
            title="Quick Pipe"
        )
        return

    from Autodesk.Revit.UI import RevitCommandId, PostableCommand
    t = DB.Transaction(doc, "Switch Pipe Type")
    t.Start()
    try:
        doc.SetDefaultElementTypeId(DB.ElementTypeGroup.PipeType, pipe_type.Id)
    except Exception as e:
        print("Failed to set pipe type: {0}".format(e))
    t.Commit()

    try:
        command_id = RevitCommandId.LookupPostableCommandId(PostableCommand.Pipe)
        uidoc.Application.PostCommand(command_id)
    except Exception as e:
        print("Failed to activate Draw Pipe: {0}".format(e))

if __name__ == "__main__":
    place_favorite_pipe()
