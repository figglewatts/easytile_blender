import bpy

class EASYTILE_TileRef(bpy.types.PropertyGroup):
    ref: bpy.props.PointerProperty(name="Object", type=bpy.types.Object)

class EASYTILE_Properties(bpy.types.PropertyGroup):
    tiles: bpy.props.CollectionProperty(name="Tile Collection", type=EASYTILE_TileRef)
    tile_index: bpy.props.IntProperty()
    grid_size: bpy.props.IntProperty(default=1)
    height: bpy.props.FloatProperty(default=0)
    height_increment: bpy.props.IntProperty(default=1)
    
    def get_tile(self):
        if self.tile_index < 0:
            return None

        try:
            return self.tiles[self.tile_index].ref
        except IndexError:
            return None

    def update_grid(self):
        bpy.context.space_data.overlay.grid_scale = self.get_grid_dimension()

    def update_height(self):
        height_inc = self.get_height_increment()
        self.height = round(self.height / height_inc) * height_inc

    def increase_grid_size(self):
        if self.grid_size == -2:
            # roll over to non-fractional
            self.grid_size = 1
        elif self.grid_size > 0:
            # otherwise, increase the grid size non-fractionally
            self.grid_size *= 2
        elif self.grid_size < 0:
            # otherwise, increase the grid size fractionally
            self.grid_size /= 2
        self.update_grid()

    def increase_height_increment(self):
        if self.height_increment == -2:
            # roll over to non-fractional
            self.height_increment = 1
        elif self.height_increment > 0:
            # otherwise, increase the grid size non-fractionally
            self.height_increment *= 2
        elif self.height_increment < 0:
            # otherwise, increase the grid size fractionally
            self.height_increment /= 2
        self.update_height()

    def decrease_grid_size(self):
        if self.grid_size == 1:
            # roll over to fractional
            self.grid_size = -2
        elif self.grid_size > 0:
            # otherwise, decrease the grid size non-fractionally
            self.grid_size /= 2
        elif self.grid_size < 0:
            # otherwise, decrease the grid size fractionally
            self.grid_size *= 2
        self.update_grid()

    def decrease_height_increment(self):
        if self.height_increment == 1:
            # roll over to fractional
            self.height_increment = -2
        elif self.height_increment > 0:
            # otherwise, decrease the grid size non-fractionally
            self.height_increment /= 2
        elif self.height_increment < 0:
            # otherwise, decrease the grid size fractionally
            self.height_increment *= 2
        self.update_height()

    def get_grid_dimension(self):
        if self.grid_size > 0:
            # non-fractional
            return self.grid_size
        else:
            # fractional
            return 1.0 / -self.grid_size

    def get_height_increment(self):
        if self.height_increment > 0:
            # non-fractional
            return self.height_increment
        else:
            # fractional
            return 1.0 / -self.height_increment