import bpy
from bpy.props import StringProperty, BoolProperty, FloatProperty, PointerProperty


# -------------------------------------------------------------
#   PROPERTY GROUP
# -------------------------------------------------------------
class G2Props(bpy.types.PropertyGroup):
    name: StringProperty(
        name="Name",
        maxlen=64,
        default="",
        description="Ghoul2 surface or tag name"
    )

    shader: StringProperty(
        name="Shader",
        maxlen=64,
        default="",
        description="Shader assigned to this surface"
    )

    tag: BoolProperty(
        name="Tag",
        default=False,
        description="Marks object as a Ghoul2 tag"
    )

    off: BoolProperty(
        name="Off",
        default=False,
        description="Surface initially disabled"
    )

    scale: FloatProperty(
        name="Scale",
        default=100.0,
        min=0.0,
        subtype='PERCENTAGE',
        description="Skeleton scale (armature only)"
    )


# -------------------------------------------------------------
#   PROPERTY CHECK HELPERS
# -------------------------------------------------------------
def hasG2MeshProperties(obj):
    return hasattr(obj, "g2_prop") and obj.g2_prop is not None


def hasG2ArmatureProperties(obj):
    return hasattr(obj, "g2_prop") and obj.g2_prop is not None


# -------------------------------------------------------------
#   UI PANEL
# -------------------------------------------------------------
class G2PropertiesPanel(bpy.types.Panel):
    bl_label = "Ghoul 2 Properties"
    bl_idname = "OBJECT_PT_g2_prop"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj and obj.type in {"MESH", "ARMATURE"}

    def draw(self, context):
        layout = self.layout
        obj = context.active_object

        if not hasattr(obj, "g2_prop"):
            layout.label(text="No G2 props found.")
            return

        props = obj.g2_prop

        if obj.type == "MESH":
            layout.operator("object.remove_g2_properties")
            layout.prop(props, "name")
            layout.prop(props, "shader")

            row = layout.row()
            row.prop(props, "tag")
            row.prop(props, "off")

        elif obj.type == "ARMATURE":
            layout.operator("object.remove_g2_properties")
            layout.prop(props, "scale")


# -------------------------------------------------------------
#   REGISTRATION
# -------------------------------------------------------------
classes = (
    G2Props,
    G2PropertiesPanel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Object.g2_prop = PointerProperty(type=G2Props)


def unregister():
    del bpy.types.Object.g2_prop
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
