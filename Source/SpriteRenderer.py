# Addon to make sprite rendering for games simple.
# Configured for GZDoom
# Author:  Chronicler of Legends
# Created: 2021
import bpy
from math import pi

# === Variables =======================================================


# === Create Operators ================================================

# Make sure we are rendering transparent
def Make_Transparent(context):
    bpy.context.scene.render.film_transparent = True
    
def Set_Angle_1(context):
    bpy.context.scene.sprite_angles = 1
    
def Set_Angle_8(context):
    bpy.context.scene.sprite_angles = 8
    
def Set_Angle_16(context):
    bpy.context.scene.sprite_angles = 16
    
def Create_RO(self, context):
    # store reference to active object
    active_object = context.active_object
    if active_object is None:
        self.report({"WARNING"}, "No object selected.")
        return {"CANCELLED"}
    # create an empty manipulator on the ground
    bpy.context.scene.cursor.location = active_object.location
    bpy.context.scene.cursor.location[2] = 0
    bpy.ops.object.empty_add(type='CIRCLE', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
    bpy.context.active_object.name = 'RotationOrigin'
    bpy.ops.transform.rotate(value=1.5708, orient_axis='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=0.620921, use_proportional_connected=False, use_proportional_projected=False)
    bpy.ops.transform.resize(value=(6.5, 6.5, 6.5), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=0.620921, use_proportional_connected=False, use_proportional_projected=False)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    # parent the object
    bpy.data.objects[active_object].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[active_object]
    bpy.data.objects["RotationOrigin"].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects["RotationOrigin"]
    bpy.ops.object.parent_set(type='OBJECT')
    
def Do_Render(self, context):
    # Select the rotation origin
    try:
        bpy.data.objects["RotationOrigin"].select_set(True)
        bpy.context.view_layer.objects.active = bpy.data.objects['RotationOrigin']
    except:
        self.report({"WARNING"}, "Object 'RotationOrigin' not found.")
        return {"CANCELLED"}
    
    # set initial values
    currentFrame = 0
    #angle = 0
    startFrame = bpy.context.scene.frame_start
    endFrame = bpy.context.scene.frame_end
    path = bpy.context.scene.sprite_export_path
    prefix = bpy.context.scene.sprite_prefix
    numAngles = bpy.context.scene.sprite_angles
    angleInc = ((pi * (360/numAngles))/180) # Formula (Angle to increase = 360 / steps) then change degrees to radians
    #framename = bpy.context.scene.sprite_framenames[currentFrame]
    #filename = ("%s%s%s%i" % (path, prefix, framename, angle))
    
    # sanity checks
    if ((endFrame - startFrame) > 26):
        self.report({"WARNING"}, "Too many frames in this animation (26+). Try splitting  it into multiple.")
        return {"CANCELLED"}
    else:
        #iterate through frames
        for frame in range (startFrame, (endFrame+1)):
            framename = bpy.context.scene.sprite_framenames[currentFrame]
            
            for angle in range (0, numAngles):
                # Render this frame
                angleOutput = angle + 1
                bpy.context.scene.render.filepath = ("%s%s%s%i" % (path, prefix, framename, angleOutput))
                #bpy.context.scene.render.filepath = ("%s%s%s%i" % (path, prefix, frame, angleOutput))
                bpy.ops.render.render(animation=False, write_still=True)
                
                # Rotate the object
                bpy.ops.transform.rotate(value=angleInc, orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=0.620921, use_proportional_connected=False, use_proportional_projected=False)
            
            # Go to next frame
            bpy.context.scene.frame_current += 1
            currentFrame += 1
        
        # reset frame
        bpy.context.scene.frame_current = startFrame

## SETTING UP THE LOOPS!!!

# Create Operators
class Make_Transparent_Operator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "spriterender.settransparent"
    bl_label = "Set render background to transparent"

    def execute(self, context):
        Make_Transparent(context)
        return {'FINISHED'}
    
class Set_Angle_1_Operator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "spriterender.setangle1"
    bl_label = "1 DIR"

    def execute(self, context):
        Set_Angle_1(context)
        return {'FINISHED'}
    
class Set_Angle_8_Operator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "spriterender.setangle8"
    bl_label = "8 DIR"

    def execute(self, context):
        Set_Angle_8(context)
        return {'FINISHED'}
    
class Set_Angle_16_Operator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "spriterender.setangle16"
    bl_label = "16 DIR"

    def execute(self, context):
        Set_Angle_16(context)
        return {'FINISHED'}
    
class Do_Render_Operator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "spriterender.render"
    bl_label = "Render the current animation"

    def execute(self, context):
        Do_Render(self, context)
        return {'FINISHED'}
    
class Create_RO_Operator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "spriterender.createro"
    bl_label = "Create and assign rotation origin"
    
    def execute(self, context):
        Create_RO(self, context)
        return {'FINISHED'}


# === Create Panel ====================================================
class SpriteRenderPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Sprite Renderer"
    bl_idname = "SCENE_PT_layout"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "output"

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        
        row = layout.row()
        row.scale_y = 1.0
        row.operator("spriterender.settransparent")
        
        row = layout.row()
        row.scale_y = 1.0
        row.operator("spriterender.createro")
        row.label(text="not working")
        
        row = layout.row()
        row.prop(context.scene, 'sprite_export_path')
        
        row = layout.row()
        row.prop(context.scene, 'sprite_prefix')
        
        row = layout.row()
        row.label(text="Angles to render:")
        row.operator("spriterender.setangle1")
        row.operator("spriterender.setangle8")
        row.operator("spriterender.setangle16")
        row = layout.row()
        row.prop(context.scene, 'sprite_angles')

        row = layout.row(align=True)
        row.prop(context.scene, 'sprite_framenames')

        row = layout.row(align=True)
        row.label(text="Timeline frames to render:")
        row.prop(scene, "frame_start")
        row.prop(scene, "frame_end")

        # Execute render
        row = layout.row()
        row.scale_y = 3.0
        row.operator("spriterender.render")



spriterenderer_classes = [
    Make_Transparent_Operator,
    Set_Angle_1_Operator,
    Set_Angle_8_Operator,
    Set_Angle_16_Operator,
    Do_Render_Operator,
    Create_RO_Operator,
    SpriteRenderPanel
]

# Register
def register():
    # Properties
    bpy.types.Scene.sprite_export_path = bpy.props.StringProperty(
        name = 'Sprite Export Path',
        subtype = 'DIR_PATH',
        default = '//'
    )
    bpy.types.Scene.sprite_prefix = bpy.props.StringProperty(
        name = 'Sprite Prefix',
        default = 'SPRI'
    )
    bpy.types.Scene.sprite_angles = bpy.props.IntProperty(
        name = 'Custom Angles',
        default = 8,
    )
    bpy.types.Scene.sprite_framenames = bpy.props.StringProperty(
        name = "Frame names",
        default = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    )
    # Classes
    for blender_class in spriterenderer_classes:
        bpy.utils.register_class(blender_class)

def unregister():
    # Properties
    del bpy.types.Scene.sprite_export_path
    del bpy.types.Scene.sprite_angles
    del bpy.types.Scene.sprite_prefix
    del bpy.types.Scene.sprite_framenames
    # Classes
    for blender_class in spriterenderer_classes:
        bpy.utils.unregister_class(blender_class)

if __name__ == "__main__":
    register()
