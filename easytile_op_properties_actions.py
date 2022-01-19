import bpy

class EASYTILE_OT_easytile_properties_actions(bpy.types.Operator):
    bl_idname = "easytile.properties_actions"
    bl_label = "EasyTile Properties Actions"
    bl_description = "Perform actions on easytile properties"
    bl_options = {"REGISTER"}

    action: bpy.props.EnumProperty(
        items=(
            ("INC_GRID", "Increase grid", ""),
            ("DEC_GRID", "Decrease grid", ""),
            ("INC_HEIGHT", "Increase height increment", ""),
            ("DEC_HEIGHT", "Decrease height increment", "")))

    def invoke(self, context, event):
        scn = context.scene

        if self.action == "INC_GRID":
            scn.easytile.increase_grid_size()
        elif self.action == "DEC_GRID":
            scn.easytile.decrease_grid_size()
        elif self.action == "INC_HEIGHT":
            scn.easytile.increase_height_increment()
        elif self.action == "DEC_HEIGHT":
            scn.easytile.decrease_height_increment()

        return {"FINISHED"}