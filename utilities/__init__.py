import bpy



from . import find_node_group

classes = [
    find_node_group.UTMROADS_OT_find_node_group,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
