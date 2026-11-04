import bpy
from nodebpy import geometry as g
from ..utilities.find_node_group import link_gn_from_library



# --------------------------------
# Operators: road operators
# --------------------------------

class UTMROADS_OT_select_road_curve(bpy.types.Operator):
    bl_idname = "utmroads.select_road_curve"
    bl_label = "Select road curve"
    bl_description = "Select the current road curve object"
    bl_options = {"REGISTER", "UNDO", "INTERNAL"}


    def execute(self, context):

        return{"FINISHED"}



# --------------------------------
# Operators: road operators
# --------------------------------

class UTMROADS_OT_add_road_connection(bpy.types.Operator):
    bl_idname = "utmroads.add_road_connection"
    bl_label = "Add road connection"
    bl_description = "Add a new road connection to the road"
    bl_options = {"REGISTER", "UNDO", "INTERNAL"}

    def _connect_roads(self, current_road, connecting_road):
        modifier_name = "UTM.ROADS_" + current_road.name + "_GN"
        modifier = current_road.modifiers.get(modifier_name)
        if not modifier or modifier.type != "NODES" or modifier.node_group is None:
            return "Road modifier not found"

        node_group = modifier.node_group

        connect_ng, error = link_gn_from_library("ULT.TRAVERSAL_RoadConnect_GN")
        if error:
            return error

        initialize = generate = None
        for node in node_group.nodes:
            if node.bl_idname in {"NodeGroupInput", "NodeGroupOutput"}:
                continue
            node_tree = getattr(node, "node_tree", None)
            if node_tree is None:
                continue
            if node.node_tree.name == "ULT.TRAVERSAL_RoadInitialize_GN":
                initialize = node
            elif node.node_tree.name == "ULT.TRAVERSAL_RoadGenerate_GN":
                generate = node
        if not initialize or not generate:
            return "Initialize or Generate group node missing in modifier tree"

        for link in list(node_group.links):
            if link.to_node == generate:
                node_group.links.remove(link)

        with g.tree(node_group, clear=False, arrange=None):
            connect = g.Group()
            connect.node.node_tree = connect_ng
            connect.node.inputs[1].default_value = connecting_road
            g.Group._from_node(initialize) >> connect >> g.Group._from_node(generate)
        return "Road connected successfully"

    def execute(self, context):
        current_road = context.view_layer.objects.active
        connecting_road = context.window_manager.utmroads_select_object
        if not connecting_road:
            self.report({"INFO"}, "You have to select an object")
            return{"CANCELLED"}
        if connecting_road == current_road:
            self.report({"ERROR"}, "the connected road cannot be the current active road. A road cannot connect to itself!")
            return{"CANCELLED"}
        if not connecting_road.utm_road.is_utm_road or not connecting_road.type == 'CURVE':
            self.report({"ERROR"}, "The selected object is not a valid road")
            return{"CANCELLED"}

        new_connection = current_road.utm_road.road_connections.add()
        new_connection.curve_object = connecting_road

        result = self._connect_roads(current_road, connecting_road)
        if result:
            self.report({'INFO'}, str(result))

        context.window_manager.utmroads_select_object = None
        context.view_layer.objects.active = current_road
        current_road.update_tag()

        return{"FINISHED"}

    def invoke(self, context, event):
        title = "Select Object"
        return context.window_manager.invoke_props_dialog(self, title = title)
    
    def draw(self, context):
        layout = self.layout
        layout.prop(context.window_manager, "utmroads_select_object", text = "Select Object")


class UTMROADS_OT_select_connected_road(bpy.types.Operator):
    bl_idname = "utmroads.select_connected_road"
    bl_label = "Select connected road"
    bl_description = "Select the current connected road object"
    bl_options = {"REGISTER", "UNDO", "INTERNAL"}


    index : bpy.props.IntProperty(options = {"HIDDEN"}, default = 0)

    def execute(self, context):
        active_object = context.view_layer.objects.active

        bpy.ops.object.select_all(action='DESELECT')
        context.view_layer.objects.active = active_object.utm_road.road_connections[self.index].curve_object
        active_object.utm_road.road_connections[self.index].curve_object.select_set(True)
        
        return{"FINISHED"}