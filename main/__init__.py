import bpy



from . import properties, properties_operators, operators, ui

classes = [
    properties.UTMROADS_PG_lane_route,
    properties.UTMROADS_PG_road_connection,
    properties.UTMROADS_PG_road,

    properties_operators.UTMROADS_OT_select_road_curve,
    properties_operators.UTMROADS_OT_select_connected_road,
    properties_operators.UTMROADS_OT_add_road_connection,

    operators.UTMROADS_OT_draw_road,
    operators.UTMROADS_OT_convert_curve_to_road,
    operators.UTMROADS_OT_sync_from_geometry_nodes,
    operators.UTMROADS_OT_sync_from_modifier_stack,

    ui.UTMROADS_UL_roads_connections_list,
    ui.UTMROADS_PT_road_setup_panel,
    ui.UTMROADS_PT_road_settings_panel,
]



def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Object.utm_road = bpy.props.PointerProperty(type = properties.UTMROADS_PG_road)
    bpy.types.WindowManager.utmroads_select_object = bpy.props.PointerProperty(
        type = bpy.types.Object,
        name = "Select Object",
        description = "Temporary object picker for Select Object dialog",
    )



def unregister():
    if hasattr(bpy.types.Object, "utm_road"):
        delattr(bpy.types.Object, "utm_road")

    if hasattr(bpy.types.WindowManager, "utmroads_select_object"):
        del bpy.types.WindowManager.utmroads_select_object

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)