import bpy

class EASYTILE_UL_tiles(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        ref = item.ref
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.prop(ref, "name", text="", emboss=False, icon_value=layout.icon(ref))

        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon_value=layout.icon(ref))

    def invoke(self, context, event):
        pass

class EASYTILE_PT_editor_panel(bpy.types.Panel):
    bl_idname = "EASYTILE_PT_editor_panel"
    bl_label = "EasyTile"
    bl_category = "EasyTile"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        scn = context.scene

        rows = 2
        row = layout.row()
        row.template_list("EASYTILE_UL_tiles", "easytile_tiles_list", scn.easytile, "tiles", scn.easytile, "tile_index", 
            rows=rows)

        col = row.column(align=True)
        col.operator("easytile.tiles_actions", icon='ADD', text="").action = 'ADD'
        col.operator("easytile.tiles_actions", icon='REMOVE', text="").action = 'REMOVE'
        col.separator()
        col.operator("easytile.tiles_actions", icon='TRIA_UP', text="").action = 'UP'
        col.operator("easytile.tiles_actions", icon='TRIA_DOWN', text="").action = 'DOWN'

        row = layout.row()
        row.operator("easytile.properties_actions", icon="REMOVE", text="").action = "DEC_GRID"
        row.label(text=f"Grid size: {scn.easytile.get_grid_dimension()}")
        row.operator("easytile.properties_actions", icon="ADD", text="").action = "INC_GRID"

        row = layout.row()
        row.operator("easytile.properties_actions", icon="REMOVE", text="").action = "DEC_HEIGHT"
        row.label(text=f"Height increment: {scn.easytile.get_height_increment()}")
        row.operator("easytile.properties_actions", icon="ADD", text="").action = "INC_HEIGHT"

        row = layout.row()
        row.prop(scn.easytile, "height", text="Tile Height")

        row = layout.row()
        row.operator("easytile.editor", text="Draw tiles")