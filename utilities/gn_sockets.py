import bpy



_USE_PROPERTIES_API = bpy.app.version >= (5, 2, 0)


def _get_socket_value(modifier, identifier: str):
    if _USE_PROPERTIES_API:
        return getattr(modifier.properties.inputs, identifier).value
    else:
        return modifier[identifier]


def _set_socket_value(modifier, identifier: str, value):
    if _USE_PROPERTIES_API:
        getattr(modifier.properties.inputs, identifier).value = value
    else:
        modifier[identifier] = value


def _input_driver_path(modifier_name: str, identifier: str) -> str:
    if _USE_PROPERTIES_API:
        return f'modifiers["{modifier_name}"].properties.inputs.{identifier}.value'
    else:
        return f'modifiers["{modifier_name}"]["{identifier}"]'
