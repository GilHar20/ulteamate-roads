import bpy



class UTMROADS_UL_roads_connections_list(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        road_row = layout.row()
        
        label_text = str(index + 1) + ": " + item.curve_object.name
        road_row.label(text = label_text, icon = 'LINKED')
        
        operator_row = road_row.row(align = True)
        select = operator_row.operator("utmroads.select_connected_road", text = "", icon = 'RESTRICT_SELECT_OFF', emboss = False)
        select.index = index


class UTMROADS_PT_road_setup_panel(bpy.types.Panel):
    bl_label = "ULTEAMMATE Roads"
    bl_idname = "UTMROADS_PT_road_setup_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ULTEAMMATE"

        
    def draw(self, context):
        layout = self.layout

        main_box = layout.box()
        main_box.label(text="Road Setup:", icon = 'ADD')

        setup_column = main_box.column(align = True)
        setup_column.operator("utmroads.draw_roads", text = "Draw New Road", icon = 'GREASEPENCIL')
        setup_column.operator("utmroads.convert_curve_to_road", text = "Convert Active Curve to Road", icon = 'MOD_CURVE_TO_TUBE')
        setup_column.operator("utmroads.sync_from_geometry_nodes", text = "Sync from Geometry Nodes", icon = 'NODE')
        setup_column.operator("utmroads.sync_from_modifier_stack", text = "Sync from Modifier Stack", icon = 'MODIFIER')



class UTMROADS_PT_road_settings_panel(bpy.types.Panel):
    bl_label = "Road Settings"
    bl_idname = "UTMROADS_PT_road_settings_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ULTEAMMATE"
    bl_parent_id = "UTMROADS_PT_road_setup_panel"


    @classmethod
    def poll(self, context):
        active_object = context.view_layer.objects.active
        if not active_object:
            return False
        if active_object.utm_road.is_utm_road and active_object.type == 'CURVE':
            return True
        else:
            return False
        
    def draw(self, context):
        layout = self.layout
        active_object = context.view_layer.objects.active
        road_data = active_object.utm_road

        road_box = layout.box()
        road_box.label(text = "Road Settings: ")
        column = road_box.column(align = True)
        column.prop(road_data, "lane_number")
        column.prop(road_data, "lane_width")

        connection_box = layout.box()
        connection_box.label(text = "Connections: ")

        connection_row = connection_box.row(align = True)
        connection_row.template_list(
            "UTMROADS_UL_roads_connections_list",
            "UTMROADS_roads_connections_list",
            road_data,
            "road_connections",
            road_data,
            "active_connection_index",
            rows = 4
        )

        left_column = connection_row.column()
        add_remove_column = left_column.column(align = True)
        add_remove_column.operator("utmroads.add_road_connection", text = "", icon = 'ADD')


        #active_connection_index = active_object.active_connection_index
        #current_connection = road_data.road_connections[active_connection_index]
