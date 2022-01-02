bl_info = {
    "name" : "EasyTile",
    "author" : "Figglewatts",
    "description" : "Simple tiling of meshes.",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "View3D",
    "warning" : "",
    "category" : "Generic"
}

import bpy

from .easytile_op_editor import EASYTILE_OT_editor_operator
from .easytile_panel_editor import EASYTILE_PT_editor_panel, EASYTILE_UL_tiles
from .easytile_properties import EASYTILE_TileRef, EASYTILE_Properties
from .easytile_op_tiles_actions import EASYTILE_OT_tiles_actions
from .easytile_op_properties import EASYTILE_OT_easytile_properties_actions

classes = (
    EASYTILE_TileRef,
    EASYTILE_Properties,
    EASYTILE_OT_tiles_actions,
    EASYTILE_OT_easytile_properties_actions,
    EASYTILE_UL_tiles,
    EASYTILE_PT_editor_panel, 
    EASYTILE_OT_editor_operator, 
)

keymaps = []

def register():
    from bpy.utils import register_class
    for clss in classes:
        register_class(clss)

    # keymap
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name="Object Mode", space_type="EMPTY")
        kmi = km.keymap_items.new(EASYTILE_OT_editor_operator.bl_idname, "T", "PRESS", ctrl=True, shift=True)

        keymaps.append((km, kmi))

    bpy.types.Scene.easytile = bpy.props.PointerProperty(type=EASYTILE_Properties)


def unregister():
    from bpy.utils import unregister_class
    for clss in reversed(classes):
        unregister_class(clss)

    for km, kmi in keymaps:
        km.keymap_items.remove(kmi)
    keymaps.clear()

    del bpy.types.Scene.easytile
