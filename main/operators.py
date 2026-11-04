import bpy
from nodebpy import geometry as g
from ..utilities.find_node_group import link_gn_from_library



def _style_group_io_nodes(node_tree, color):
    for node in node_tree.nodes:
        if node.bl_idname in {"NodeGroupInput", "NodeGroupOutput"}:
            node.use_custom_color = True
            node.color = color



# ----------------
# Operators: Roads
# ----------------

class UTMROADS_OT_draw_road(bpy.types.Operator):
    bl_idname = "utmroads.draw_roads"
    bl_label = "Draw roads curve"
    bl_description = "Create a curve object and enter edit mode to draw the intial curve"
    bl_options = {"REGISTER", "UNDO", "INTERNAL"}

    road_name: bpy.props.StringProperty(
        name="Road Name",
        description="Name of the road",
        default="road",
    )
    lane_number: bpy.props.IntProperty(
        name="Lane Number",
        description="Number of lanes in the road",
        default=2,
        min=1,
    )
    lane_width: bpy.props.FloatProperty(
        name="Lane Width",
        description="Width of ALL lanes of the road",
        default=3.0,
        min=0.1,
    )

    def _create_base_road(self, road_object):
        road_name = road_object.name
        modifier_name = ".UTM.ROADS_" + road_name + "_GN"

        initialize_ng, error = link_gn_from_library("ULT.TRAVERSAL_RoadInitialize_GN")
        if error:
            return error
        generate_ng, error = link_gn_from_library("ULT.TRAVERSAL_RoadGenerate_GN")
        if error:
            return error

        with g.tree(modifier_name, clear=True, is_modifier=True) as tree:
            initialize = g.Group()
            initialize.node.node_tree = initialize_ng
            generate = g.Group()
            generate.node.node_tree = generate_ng

            initialize.node.inputs[4].default_value = road_object.utm_road.lane_number
            initialize.node.inputs[5].default_value = road_object.utm_road.lane_width
            # median
            # shoulders
            #initialize.node.inputs[?].default_value = road_object.utm_road.road_material
            #initialize.node.inputs[?].default_value = road_object.utm_road.sidewalk_material

            (
                tree.inputs.geometry("Geometry")
                >> initialize
                >> generate
                >> tree.outputs.geometry("Geometry")
            )
            _style_group_io_nodes(tree.tree, (0.208, 0.608, 0.219))
            node_group = tree.tree

        existing = road_object.modifiers.get(modifier_name)
        if existing is not None and existing.type == "NODES":
            existing.node_group = node_group
        else:
            mod = road_object.modifiers.new(name=modifier_name, type="NODES")
            mod.node_group = node_group
        return modifier_name

    def execute(self, context):
        if bpy.context.mode != "OBJECT":
            self.report({'INFO'}, "You need to be in object mode!")
            return{"CANCELLED"}

        bpy.ops.object.select_all(action='DESELECT')

        bpy.ops.curve.primitive_bezier_curve_add(radius=1, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        new_curve = context.view_layer.objects.active

        new_curve.utm_road.is_utm_road = True
        new_curve.name = self.road_name
        new_curve.utm_road.lane_number = self.lane_number
        new_curve.utm_road.lane_width = self.lane_width
        try:
            self._create_base_road(new_curve)
        except RuntimeError as exc:
            self.report({"ERROR"}, str(exc))
            return {"CANCELLED"}

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.curve.select_all(action='SELECT')
        bpy.ops.curve.delete(type='VERT')

        bpy.ops.view3d.view_axis(type = 'TOP')
        bpy.ops.wm.tool_set_by_id(name="builtin.draw")
        #bpy.ops.object.origin_set(type = 'ORIGIN_GEOMETRY')
        
        return{"FINISHED"}
    
    def invoke(self, context, event):
        title = "New Road Settings"
        return context.window_manager.invoke_props_dialog(self, title = title)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "road_name", placeholder = "Road Name")
        layout.prop(self, "lane_number", placeholder = "Lane Number")
        layout.prop(self, "lane_width", placeholder = "Lane Width")


class UTMROADS_OT_convert_curve_to_road(bpy.types.Operator):
    bl_idname = "utmroads.convert_curve_to_road"
    bl_label = "Convert curve to road"
    bl_description = "Convert a curve object to a valid road"
    bl_options = {"REGISTER", "UNDO", "INTERNAL"}

    road_name: bpy.props.StringProperty(
        name="Road Name",
        description="Name of the road",
        default="road",
    )
    lane_number: bpy.props.IntProperty(
        name="Lane Number",
        description="Number of lanes in the road",
        default=2,
        min=1,
    )
    lane_width: bpy.props.FloatProperty(
        name="Lane Width",
        description="Width of ALL lanes of the road",
        default=3.0,
        min=0.1,
    )

    def execute(self, context):
        if bpy.context.mode != "OBJECT":
            self.report({'INFO'}, "You need to be in object mode!")
            return{"CANCELLED"}

        new_curve = context.view_layer.objects.active
        if new_curve.type != 'CURVE':
            self.report({'INFO'}, "You can only convert curves to roads!")
            return{"CANCELLED"}

        new_curve.utm_road.is_utm_road = True
        new_curve.name = self.road_name
        new_curve.utm_road.lane_number = self.lane_number
        new_curve.utm_road.lane_width = self.lane_width
        try:
            _create_base_road(new_curve)
        except RuntimeError as exc:
            self.report({"ERROR"}, str(exc))
            return {"CANCELLED"}

        return{"FINISHED"}
    
    def invoke(self, context, event):
        title = "New Road Settings"
        return context.window_manager.invoke_props_dialog(self, title = title)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "road_name", placeholder = "Road Name")
        layout.prop(self, "lane_number", placeholder = "Lane Number")
        layout.prop(self, "lane_width", placeholder = "Lane Width")


class UTMROADS_OT_sync_from_geometry_nodes(bpy.types.Operator):
    bl_idname = "utmroads.sync_from_geometry_nodes"
    bl_label = "Sync road from geometry nodes"
    bl_description = "Sync the road data from a selected geometry nodes modifier"
    bl_options = {"REGISTER", "UNDO", "INTERNAL"}


    def execute(self, context):
        self.report({'INFO'}, "Not implemented yet!")
        return{"FINISHED"}


class UTMROADS_OT_sync_from_modifier_stack(bpy.types.Operator):
    bl_idname = "utmroads.sync_from_modifier_stack"
    bl_label = "Sync road from modifier stack"
    bl_description = "Sync the road data hirerchy from the object's modifier stack"
    bl_options = {"REGISTER", "UNDO", "INTERNAL"}


    def execute(self, context):
        self.report({'INFO'}, "Not implemented yet!")
        return{"FINISHED"}