import bpy



from . import properties, operators, ui

classes = [
    ui.UTMROADS_PT_control_panel
]



def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)