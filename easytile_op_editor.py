import bpy
from bpy.types import Operator

import math

import bgl
import gpu
import blf
from bpy_extras import view3d_utils
from gpu_extras import batch
from mathutils import geometry, Vector, Matrix, Euler
import numpy as np

class EASYTILE_OT_editor_operator(Operator):
    bl_idname = "easytile.editor"
    bl_label = "EasyTile"
    bl_description = "Tile meshes easily."
    bl_options = {"REGISTER", "UNDO"}

    def __init__(self):
        self.shader = gpu.shader.from_builtin("3D_UNIFORM_COLOR")
        self.rotation = 0
        self.placed_points = []
        self.cursor_pos = (0, 0, 0)
        self.batch = None
        self.mouse_pressed = False
        self.tile_collection = None

    def ensure_tile_collection_exists(self, context):
        tile_col = bpy.data.collections.get("EasyTileTiles")
        if tile_col is None:
            tile_col = bpy.data.collections.new("EasyTileTiles")
        if not context.scene.user_of_id(tile_col):
            context.collection.children.link(tile_col)
        self.tile_collection = tile_col

    def create_tile_batch(self, context):
        selected_tile = context.scene.easytile.get_tile()
        if selected_tile is None:
            self.batch = None
            return

        tile_mesh = selected_tile.data
        tile_mesh.calc_loop_triangles()
        verts = [ pos.co for pos in tile_mesh.vertices ]
        indices = [ tuple(poly.vertices) for poly in tile_mesh.loop_triangles ]

        self.batch = batch.batch_for_shader(self.shader, "TRIS", {"pos": verts}, indices)

    def rotate(self):
        self.rotation += 90
        if self.rotation > 360:
            self.rotation = 90

    def inverse_rotate(self):
        self.rotation -= 90
        if self.rotation < 0:
            self.rotation = 270

    @classmethod
    def poll(cls, context):
        return (context.active_object is not None and context.active_object.mode == "OBJECT" \
            and len(context.scene.easytile.tiles) > 0)

    def invoke(self, context, event):
        args = (self, context)
        self.register_handlers(args, context)
        self.create_tile_batch(context)
        self.ensure_tile_collection_exists(context)

        context.window_manager.modal_handler_add(self)

        return {"RUNNING_MODAL"}

    def modal(self, context, event):
        if context.area:
            context.area.tag_redraw()

        self.cursor_pos = self.get_cursor_plane_position(event, context)

        if event.type == "MOUSEMOVE":
            if self.mouse_pressed and self.cursor_pos not in self.placed_points:
                self.instantiate_tile(context, self.cursor_pos)

        if event.alt and event.type == "WHEELUPMOUSE":
            context.scene.easytile.height += context.scene.easytile.get_height_increment()
        elif event.alt and event.type == "WHEELDOWNMOUSE":
            context.scene.easytile.height -= context.scene.easytile.get_height_increment()

        if event.type == "ESC":
            return self.finish(context)

        if event.value == "PRESS":
            if event.type == "LEFTMOUSE":
                self.mouse_pressed = True
                self.placed_points.clear()
                pos = self.get_cursor_plane_position(event, context)
                self.instantiate_tile(context, pos)
                return {"RUNNING_MODAL"}

            if event.type == "RIGHTMOUSE":
                if event.alt:
                    # reverse direction
                    self.inverse_rotate()
                else:
                    # rotate
                    self.rotate()
                return {"RUNNING_MODAL"}

            if event.type == "MINUS":
                if event.alt:
                    context.scene.easytile.decrease_height_increment()
                else:
                    context.scene.easytile.decrease_grid_size()
                return {"RUNNING_MODAL"}

            if event.type == "EQUAL":
                if event.alt:
                    context.scene.easytile.increase_height_increment()
                else:
                    context.scene.easytile.increase_grid_size()
                return {"RUNNING_MODAL"}

        if event.value == "RELEASE":
            if event.type == "LEFTMOUSE":
                self.placed_points.clear()
                self.mouse_pressed = False

        return {"PASS_THROUGH"}

    def finish(self, context):
        self.unregister_handlers(context)
        return {"FINISHED"}

    def instantiate_tile(self, context, pos):
        selected_tile = context.scene.easytile.get_tile()
        if selected_tile is None:
            return

        self.placed_points.append(pos)

        instantiated_tile = bpy.data.objects.new(f"{selected_tile.name}_tile", selected_tile.data)
        instantiated_tile.location = pos
        instantiated_tile.rotation_euler = Euler((0.0, 0.0, math.radians(self.rotation)))
        self.tile_collection.objects.link(instantiated_tile)
        bpy.ops.ed.undo_push()

    def get_cursor_plane_position(self, event, context):
        region = context.region
        region_3d = context.space_data.region_3d

        mouse_coord = (event.mouse_region_x, event.mouse_region_y)

        # get vector from viewport
        origin = view3d_utils.region_2d_to_origin_3d(region, region_3d, mouse_coord)
        direction = view3d_utils.region_2d_to_vector_3d(region, region_3d, mouse_coord)

        # get intersection on plane
        plane_origin = Vector((0.0, 0.0, context.scene.easytile.height))
        plane_up = Vector((0.0, 0.0, 1.0))
        plane_intersect = geometry.intersect_line_plane(origin, origin + direction, plane_origin, plane_up)
        plane_intersect = self.snap_to_grid(plane_intersect, context)

        return plane_intersect
        

    def snap_to_grid(self, vec, context):
        grid_dimension = context.scene.easytile.get_grid_dimension()
        half_dimension = grid_dimension * 0.5  # to center within grid cell
        vec.x = math.floor(vec.x / grid_dimension) * grid_dimension + half_dimension
        vec.y = math.floor(vec.y / grid_dimension) * grid_dimension + half_dimension
        vec.z = context.scene.easytile.height
        return vec
        

    def register_handlers(self, args, context):
        self.draw_handle_2d = bpy.types.SpaceView3D.draw_handler_add(
            self.draw_callback_2d, args, "WINDOW", "POST_PIXEL")
        self.draw_handle_3d = bpy.types.SpaceView3D.draw_handler_add(
            self.draw_callback_3d, args, "WINDOW", "POST_VIEW"
        )

        self.draw_event = context.window_manager.event_timer_add(0.1, window=context.window)

    def unregister_handlers(self, context):
        context.window_manager.event_timer_remove(self.draw_event)
        self.draw_event = None
        
        bpy.types.SpaceView3D.draw_handler_remove(self.draw_handle_2d, "WINDOW")
        self.draw_handle_2d = None

        bpy.types.SpaceView3D.draw_handler_remove(self.draw_handle_3d, "WINDOW")
        self.draw_handle_3d = None

    def get_tile_matrix(self, context):
        region_3d = context.space_data.region_3d

        trans_mat = Matrix.Translation(self.cursor_pos)
        rot_mat = Matrix.Rotation(math.radians(self.rotation), 4, "Z")

        return region_3d.view_matrix @ trans_mat @ rot_mat

    def draw_callback_2d(self, op, context):
        region = context.region

        xt = int(region.width / 2.0)
        text = "Drawing tiles (ESC to exit)"

        blf.size(0, 24, 72)
        blf.position(0, xt - blf.dimensions(0, text)[0] / 2, 60 , 0)
        blf.draw(0, text) 

    def draw_callback_3d(self, op, context):
        if self.batch is None:
            return

        bgl.glEnable(bgl.GL_BLEND)
        self.shader.bind()
        self.shader.uniform_float("color", (1.0, 1.0, 1.0, 0.3))
        trans_mat = self.get_tile_matrix(context)
        gpu.matrix.push()
        gpu.matrix.load_matrix(trans_mat)
        self.batch.draw(self.shader)
        gpu.matrix.pop()