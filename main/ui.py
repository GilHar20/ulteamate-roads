import bpy



class UTMROADS_PT_control_panel(bpy.types.Panel):
    bl_label = "ULTEAMMATE Roads"
    bl_idname = "UTMROADS_PT_main_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ULTEAMMATE"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        main_box = layout.box()
        main_button = main_box.label(text = "The first thing!")