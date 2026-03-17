bl_info = {
    "name": "Add a parent",
    "author": "Chebhou",
    "version": (1, 1),
    "blender": (4, 0, 0),
    "description": "Adds a parent for the selected objects",
    "category": "Object",
}

import bpy
from bpy.props import BoolProperty, EnumProperty, StringProperty


def add_parent(self, context):
    selected_obj = context.selected_objects.copy()

    # Snap cursor to the chosen position
    if self.position == 'center':
        bpy.ops.view3d.snap_cursor_to_center()
    elif self.position == 'selected':
        bpy.ops.view3d.snap_cursor_to_selected()
    elif self.position == 'active':
        bpy.ops.view3d.snap_cursor_to_active()
    # 'None' → leave cursor where it is

    bpy.ops.object.empty_add(type=self.type)
    empty = context.object
    empty.name = self.name

    inv_mat = empty.matrix_world.inverted()
    for obj in selected_obj:
        obj.parent = empty
        if self.inverse:
            obj.matrix_parent_inverse = inv_mat


class AddParent(bpy.types.Operator):
    """Create a new Empty and make it the parent of selected objects"""
    bl_idname = "object.add_parent"
    bl_label = "Add a Parent"
    bl_options = {'REGISTER', 'UNDO'}

    # --- properties via annotations (required since Blender 2.8) ---
    type: EnumProperty(
        name="Empty Type",
        description="Shape of the Empty object",
        items=[
            ('PLAIN_AXES',    "Axes",         "Plain axes"),
            ('ARROWS',        "Arrows",       "Arrows"),
            ('SINGLE_ARROW',  "Single Arrow", "Single arrow"),
            ('CIRCLE',        "Circle",       "Circle"),
            ('CUBE',          "Cube",         "Cube"),
            ('SPHERE',        "Sphere",       "Sphere"),
            ('CONE',          "Cone",         "Cone"),
        ],
        default='PLAIN_AXES',
    )

    inverse: BoolProperty(
        name="Set Parent Inverse",
        description="Apply the inverse matrix so objects keep their world transform",
        default=True,
    )

    position: EnumProperty(
        name="Parent Position",
        description="Where to place the new Empty",
        items=[
            ('center',   "World Center",         "Snap to world origin"),
            ('None',     "Cursor Position",      "Use current cursor location"),
            ('selected', "Median Point",         "Snap to median of selection"),
            ('active',   "Active Object",        "Snap to active object"),
        ],
        default='selected',
    )

    name: StringProperty(
        name="Name",
        default="Parent",
    )

    def execute(self, context):
        add_parent(self, context)
        return {'FINISHED'}


# ------------------------------------------------------------------ #
addon_keymaps = []


def register():
    bpy.utils.register_class(AddParent)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='Object Mode', space_type='EMPTY')
        kmi = km.keymap_items.new(AddParent.bl_idname, 'P', 'PRESS')
        addon_keymaps.append((km, kmi))


def unregister():
    bpy.utils.unregister_class(AddParent)

    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()


if __name__ == "__main__":
    register()
