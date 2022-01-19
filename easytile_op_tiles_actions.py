import bpy

class EASYTILE_OT_tiles_actions(bpy.types.Operator):
    """Move items up and down, add and remove"""
    bl_idname = "easytile.tiles_actions"
    bl_label = "Tile actions"
    bl_description = "Move items up and down, add and remove"
    bl_options = {"REGISTER", "UNDO"}

    action: bpy.props.EnumProperty(
        items=(
            ("UP", "Up", ""),
            ("DOWN", "Down", ""),
            ("REMOVE", "Remove", ""),
            ("ADD", "Add", "")))

    def invoke(self, context, event):
        scn = context.scene
        idx = scn.easytile.tile_index

        try:
            item = scn.easytile.tiles[idx]
        except IndexError:
            pass
        else:
            if self.action == "DOWN" and idx < len(scn.easytile.tiles) - 1:
                scn.easytile.tiles.move(idx, idx+1)
                scn.easytile.tile_index += 1

            elif self.action == "UP" and idx >= 1:
                scn.easytile.tiles.move(idx, idx-1)
                scn.easytile.tile_index -= 1

            elif self.action == "REMOVE":
                scn.easytile.tiles.remove(idx)
                if scn.easytile.tile_index == 0:
                    scn.easytile.tile_index = 0
                else:
                    scn.easytile.tile_index -= 1

        if self.action == "ADD":
            if not isinstance(context.active_object.data, bpy.types.Mesh):
                return {"CANCELLED"}

            for obj in context.selected_objects:
                item = scn.easytile.tiles.add()
                item.ref = obj
            
            scn.easytile.tile_index = (len(scn.easytile.tiles)-1)

        return {"FINISHED"}