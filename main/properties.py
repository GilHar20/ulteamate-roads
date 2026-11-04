import bpy



class UTMROADS_PG_lane_route(bpy.types.PropertyGroup):
    self_lane : bpy.props.IntProperty(
        name = "Self Lane",
        description = "The lane on current road to re-route",
        default = 0,
        min = 0,
        max = 100
    )

    connectiong_lane : bpy.props.IntProperty(
        name = "Connecting Lane",
        description = "The lane on connecting road to route to",
        default = 0,
        min = 0,
        max = 100
    )


class UTMROADS_PG_road_connection(bpy.types.PropertyGroup):
    curve_object : bpy.props.PointerProperty(
        name = "Connecting Road",
        description = "The road object connecting to current (self) road object",
        type = bpy.types.Object
    )

    lane_routes : bpy.props.CollectionProperty(
        name = "Road Connections",
        description = "List of all roads connecting to currnet (self) road",
        type = UTMROADS_PG_lane_route
    )


class UTMROADS_PG_road(bpy.types.PropertyGroup):
    def _update_base_curve_name(self, context):
        self.curve_object.name = self.name

    name : bpy.props.StringProperty(
        name = "Road Name",
        description = "Name of the road",
        default = "road",
        update = _update_base_curve_name
    )

    is_utm_road : bpy.props.BoolProperty(
        name = "Valid UTM Road",
        description = "Whether the road is a valid UTM road",
        default = False
    )
    
    lane_number : bpy.props.IntProperty(
        name = "Lane Number",
        description = "Number of lanes in the road",
        default = 2
    )

    lane_width : bpy.props.FloatProperty(
        name = "Lane Width",
        description = "Width of ALL lanes of the road",
        default = 3.0
    )

    road_material : bpy.props.PointerProperty(
        name = "Road Material",
        description = "",
        type = bpy.types.Material
    )

    sidewalk_material : bpy.props.PointerProperty(
        name = "Sidewalk Material",
        description = "",
        type = bpy.types.Material
    )

    road_connections : bpy.props.CollectionProperty(
        name = "Road Connections",
        description = "List of all roads connecting to currnet (self) road",
        type = UTMROADS_PG_road_connection
    )

    active_connection_index : bpy.props.IntProperty(
        name = "Active Connection Index",
        default = 0,
        min = 0,
        max = 10000
    )