bl_info = {
    "name": "ULTEAMMATE Roads",
    "version": (0, 1, 0),
    "blender": (5, 3, 0),
    "author": "Gilad Harnik",
    "location": "View3D > Sidebar > ULTEAMMATE > ULTEAMMATE Roads",
    "description": "Spline based procedural roads toolkit",
    "category": "3D View",
    "git_url": "https://github.com/GilHar20/ulteamate-roads.git",
    "git_branch": "main",
    "git_commit": "main",
    "tracker_url": "https://github.com/GilHar20/ulteamate-roads/issues",
    "doc_url": "https://github.com/GilHar20/ulteamate-roads",
}

import sys
from pathlib import Path

import bpy

_nodebpy_src = Path(__file__).resolve().parent / "nodebpy-main" / "nodebpy-main" / "src"
if _nodebpy_src.is_dir():
    _nodebpy_src_str = str(_nodebpy_src)
    if _nodebpy_src_str not in sys.path:
        sys.path.insert(0, _nodebpy_src_str)

from . import main
from . import utilities


class UTMROADS_AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    asset_library_name: bpy.props.StringProperty(
        name = "Asset Library",
        description = "Name of the asset library to link node groups from",
        default = "ULTEAMMATE"
    )

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box.label(text="Asset library", icon="ASSET_MANAGER")
        box.prop(self, "asset_library_name")


def register():
    bpy.utils.register_class(UTMROADS_AddonPreferences)
    utilities.register()
    main.register()


def unregister():
    main.unregister()
    utilities.unregister()
    bpy.utils.unregister_class(UTMROADS_AddonPreferences)



if __name__ == "__main__":
    register()