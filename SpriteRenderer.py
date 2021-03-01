bl_info = {
    "name": "Chrono's Directional Sprite Batch Render",
    "author": "Chronicler of Legends",
    "version": (1, 2),
    "blender": (2, 90, 1),
    "location": "Properties > Output > Chrono's Directional Sprite Renderer",
    "description": "Toolset for creating sprites for 2.5d games.",
    "warning": "",
    "doc_url": "https://github.com/chronicleroflegends/DirectionalSpriteBatchRender",
    "category": "Render",
}

# Addon to make sprite rendering for games simple.
# Configured for GZDoom
# Author:  Chronicler of Legends
# Created: 2021
import bpy
from math import pi
import enum

# === Constants =======================================================
frame_style_letter = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
frame_style_number = '1_2_3_4_5_6_7_8_...'
angle_style_doom8 = '12345678'
angle_style_doom16 = '192A3B4C5D6E7F8G'
   
# === Variables =======================================================
frame_style_text = frame_style_letter
angle_style_text = angle_style_doom8

# === Create Operators ================================================

# Make sure we are rendering transparent
def Make_Transparent(context):
    bpy.context.scene.render.film_transparent = True
    
def Set_AA_On(self, context):
    bpy.context.scene.render.filter_size = 1.5
    
def Set_AA_Off(self, context):
    bpy.context.scene.render.filter_size = 0.01
    
def Set_Clockwise(self, context):
    bpy.context.scene.sprite_direction = 1
    
def Set_CClockwise(self, context):
    bpy.context.scene.sprite_direction = -1
    
def Set_Angle_1(context):
    bpy.context.scene.sprite_angles = 1
    
def Set_Angle_8(context):
    bpy.context.scene.sprite_angles = 8
    
def Set_Angle_16(context):
    bpy.context.scene.sprite_angles = 16
    
def Set_FrameStyle_Letter(context):
    bpy.context.scene.sprite_framestyle = 1
    
def Set_FrameStyle_Number(context):
    bpy.context.scene.sprite_framestyle = 2
    
def Set_AngleStyle_Doom8(context):
    bpy.context.scene.sprite_anglestyle = 1

def Set_AngleStyle_Doom16(context):
    bpy.context.scene.sprite_anglestyle = 2
    
def Set_AngleStyle_Simple(context):
    bpy.context.scene.sprite_anglestyle = 3
    
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
    bpy.data.objects[active_object.name].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[active_object.name]
    bpy.data.objects["RotationOrigin"].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects["RotationOrigin"]
    bpy.ops.object.parent_set(type='OBJECT')
    
def Create_SC(self, context):
    # store reference to active object
    active_object = context.active_object
    if active_object is None:
        self.report({"WARNING"}, "No object selected.")
        return {"CANCELLED"}
    # create camera
    bpy.context.scene.cursor.location = active_object.location
    bpy.context.scene.cursor.location[2] = 0
    camera = bpy.ops.object.camera_add(enter_editmode=False, align='WORLD', location=(0, 6.5, 3), rotation=(((pi*-90)/180), ((pi*180)/180), 0), scale=(1, 1, 1))
    bpy.context.active_object.name = 'SpriteCamera'
    target = bpy.ops.object.empty_add(type='SPHERE', align='WORLD', location=(0, 0, 1), scale=(1, 1, 1))
    bpy.context.active_object.name = 'CameraTarget'
    bpy.data.objects['CameraTarget'].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects['CameraTarget']
    bpy.data.objects['SpriteCamera'].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects['SpriteCamera']
    bpy.ops.object.constraint_add_with_targets(type='TRACK_TO')

    
def Do_Render(self, context):
    if(bpy.context.scene.render.film_transparent == False):
        self.report({"WARNING"}, "Background is not set to transparent.")
        return {"CANCELLED"}
    
    # Select the rotation origin
    bpy.ops.object.select_all(action='DESELECT')
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
    angleInc = (((pi * (360/numAngles))/180) * bpy.context.scene.sprite_direction) # Formula (Angle to increase = 360 / steps) then change degrees to radians
    #framename = bpy.context.scene.sprite_framenames[currentFrame]
    #filename = ("%s%s%s%i" % (path, prefix, framename, angle))
    
    # sanity checks
    if (bpy.context.scene.sprite_framestyle == 1):
        if ((endFrame - startFrame) > 26):
            self.report({"WARNING"}, "Too many frames in this animation (26+). Try splitting  it into multiple.")
            return {"CANCELLED"}
    
    #iterate through frames
    for frame in range (startFrame, (endFrame+1)):
        # Decide the frame name
        #framename = bpy.context.scene.sprite_framenames[currentFrame]
        if (bpy.context.scene.sprite_framestyle == 1):
            framename = frame_style_letter[currentFrame]
        if (bpy.context.scene.sprite_framestyle == 2):
            framename = str(currentFrame) + '_'
        
        for angle in range (0, numAngles):
            # Decide the angle name
            if (bpy.context.scene.sprite_anglestyle == 1):
                if (numAngles != 8):
                    self.report({"WARNING"}, "To use this angle style you must use EXACTLY 8 angles")
                    return {"CANCELLED"}
                angleOutput = angle_style_doom8[angle]
            if (bpy.context.scene.sprite_anglestyle == 2):
                if (numAngles != 16):
                    self.report({"WARNING"}, "To use this angle style you must use EXACTLY 16 angles")
                    return {"CANCELLED"}
                angleOutput = angle_style_doom16[angle]
            if (bpy.context.scene.sprite_anglestyle == 3):
                angleOutput = str(angle + 1)

            #Render this frame
            bpy.context.scene.render.filepath = ("%s%s%s%s" % (path, prefix, framename, angleOutput))
            #bpy.context.scene.render.filepath = ("%s%s%s%i" % (path, prefix, frame, angleOutput))
            bpy.ops.render.render(animation=False, write_still=True)
            
            # Rotate the object
            bpy.ops.transform.rotate(value=angleInc, orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=0.620921, use_proportional_connected=False, use_proportional_projected=False)
        
        # Go to next frame
        bpy.context.scene.frame_current += 1
        currentFrame += 1 # do we need this?
    
    # reset frame
    bpy.context.scene.frame_current = startFrame


# Create Operators
class Make_Transparent_Operator(bpy.types.Operator):
    """Set the render to have a transparent background"""
    bl_idname = "spriterender.settransparent"
    bl_label = "Set render transparent"

    def execute(self, context):
        Make_Transparent(context)
        return {'FINISHED'}
    
class Set_Angle_1_Operator(bpy.types.Operator):
    """Only render from 1 direction"""
    bl_idname = "spriterender.setangle1"
    bl_label = "1 DIR"

    def execute(self, context):
        Set_Angle_1(context)
        return {'FINISHED'}
    
class Set_Angle_8_Operator(bpy.types.Operator):
    """Render from 8 directions (default Doom)"""
    bl_idname = "spriterender.setangle8"
    bl_label = "8 DIR"

    def execute(self, context):
        Set_Angle_8(context)
        return {'FINISHED'}
    
class Set_Angle_16_Operator(bpy.types.Operator):
    """Render from 16 directions (ZDoom)"""
    bl_idname = "spriterender.setangle16"
    bl_label = "16 DIR"

    def execute(self, context):
        Set_Angle_16(context)
        return {'FINISHED'}
    
class Set_FrameStyle_Letter_Operator(bpy.types.Operator):
    """Set frame naming to letters (MAX 26 FRAMES)"""
    bl_idname = "spriterender.setframestyleletter"
    bl_label = "Letter"
    
    def execute(self, context):
        Set_FrameStyle_Letter(context)
        return {'FINISHED'}
    
class Set_FrameStyle_Number_Operator(bpy.types.Operator):
    """Set frame naming to numbers"""
    bl_idname = "spriterender.setframestylenumber"
    bl_label = "Number"
    
    def execute(self, context):
        Set_FrameStyle_Number(context)
        return {'FINISHED'}
    
class Set_AngleStyle_Doom8_Operator(bpy.types.Operator):
    """Set angle naming to doom 8 sided default (ZDoom)"""
    bl_idname = "spriterender.setanglestyledoom8"
    bl_label = "Doom 8 Dir"

    def execute(self, context):
        Set_AngleStyle_Doom8(context)
        return {'FINISHED'}
    
class Set_AngleStyle_Doom16_Operator(bpy.types.Operator):
    """Set angle naming to doom 16 sided default (ZDoom)"""
    bl_idname = "spriterender.setanglestyledoom16"
    bl_label = "Doom 16 Dir"

    def execute(self, context):
        Set_AngleStyle_Doom16(context)
        return {'FINISHED'}
    
class Set_AngleStyle_Simple_Operator(bpy.types.Operator):
    """Set angle naming to simple numbered"""
    bl_idname = "spriterender.setanglestylesimple"
    bl_label = "Simple"

    def execute(self, context):
        Set_AngleStyle_Simple(context)
        return {'FINISHED'}
    
class Do_Render_Operator(bpy.types.Operator):
    """Render the animation with current settings"""
    bl_idname = "spriterender.render"
    bl_label = "Render"

    def execute(self, context):
        Do_Render(self, context)
        return {'FINISHED'}
    
class Create_RO_Operator(bpy.types.Operator):
    """Create and set up Rotation Origin"""
    bl_idname = "spriterender.createro"
    bl_label = "Create RotationOrigin"
    
    def execute(self, context):
        Create_RO(self, context)
        return {'FINISHED'}
    
class Create_SC_Operator(bpy.types.Operator):
    """Create and set up Sprite Camera"""
    bl_idname = "spriterender.createsc"
    bl_label = "Create SpriteCamera"
    
    def execute(self, context):
        Create_SC(self, context)
        return {'FINISHED'}
    
class Set_AA_On_Operator(bpy.types.Operator):
    """Set Anti-Aliasing(filter-size) to default"""
    bl_idname = "spriterender.setaaon"
    bl_label = "AA On"
    
    def execute(self, context):
        Set_AA_On(self, context)
        return {'FINISHED'}

class Set_AA_Off_Operator(bpy.types.Operator):
    """Set Anti-Aliasing(filter-size) to minimum(0.01)"""
    bl_idname = "spriterender.setaaoff"
    bl_label = "AA Off"
    
    def execute(self, context):
        Set_AA_Off(self, context)
        return {'FINISHED'}
    
class Set_Clockwise_Operator(bpy.types.Operator):
    """Set rotation direction to clockwise"""
    bl_idname = "spriterender.setcw"
    bl_label = "Clockwise"
    
    def execute(self, context):
        Set_Clockwise(self, context)
        return {'FINISHED'}
    
class Set_CClockwise_Operator(bpy.types.Operator):
    """Set rotation direction to conter-clockwise"""
    bl_idname = "spriterender.setccw"
    bl_label = "Counter-Clockwise"
    
    def execute(self, context):
        Set_CClockwise(self, context)
        return {'FINISHED'}



# === Create Panel ====================================================
class SpriteRenderPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Chrono's Directional Sprite Renderer"
    bl_idname = "SCENE_PT_layout"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "output"

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        resolution = context.scene.render
        
        row = layout.row()
        row.scale_y = 1.0
        row.operator("spriterender.settransparent")
        
        row = layout.row()
        row.scale_y = 1.0
        row.operator("spriterender.createro")
        
        row = layout.row()
        row.scale_y = 1.0
        row.operator("spriterender.createsc")
        
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
        row.label(text="Frame Style:")
        if (bpy.context.scene.sprite_framestyle == 1):
            row.label(text="Letter (max 26 frames)")
            row.label(text=frame_style_letter)
        if (bpy.context.scene.sprite_framestyle == 2):
            row.label(text="Number")
            row.label(text="%s" %(frame_style_number))
            
        row = layout.row(align=True)
        row.operator("spriterender.setframestyleletter")
        row.operator("spriterender.setframestylenumber")
        
        row = layout.row(align=True)
        row.label(text="Angle Style:")
        if (bpy.context.scene.sprite_anglestyle == 1):
            row.label(text="Doom 8 Dir")
            row.label(text=angle_style_doom8)
        if (bpy.context.scene.sprite_anglestyle == 2):
            row.label(text="Doom 16 Dir")
            row.label(text=angle_style_doom16)
        if (bpy.context.scene.sprite_anglestyle == 3):
            row.label(text="Simple")
            row.label(text="1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 ...")
            
        row = layout.row(align=True)
        row.operator("spriterender.setanglestyledoom8")
        row.operator("spriterender.setanglestyledoom16")
        row.operator("spriterender.setanglestylesimple")
        #row.label(text=angle_style_text)
        
        #row.prop(context.scene, 'sprite_framenames')

        row = layout.row(align=True)
        row.label(text="Animation:")
        row.prop(scene, "frame_start")
        row.prop(scene, "frame_end")
        
        row = layout.row(align=True)
        row.label(text="Resolution:")
        row.prop(resolution, "resolution_x")
        row.prop(resolution, "resolution_y")
        
        row = layout.row(align=True)
        row.label(text="Anti-aliasing (filter size)")
        row.label(text=str(bpy.context.scene.render.filter_size))
        row = layout.row(align=True)
        row.operator("spriterender.setaaon")
        row.operator("spriterender.setaaoff")
        
        row = layout.row(align=True)
        row.label(text="Direction:")
        if (bpy.context.scene.sprite_direction == 1):
            row.label(text="Clockwise")
        else:
            row.label(text="Counter-Clockwise")
        row.operator("spriterender.setcw")
        row.operator("spriterender.setccw")

        # Execute render
        row = layout.row()
        row.scale_y = 3.0
        row.operator("spriterender.render")



spriterenderer_classes = [
    Make_Transparent_Operator,
    Set_Angle_1_Operator,
    Set_Angle_8_Operator,
    Set_Angle_16_Operator,
    Set_FrameStyle_Letter_Operator,
    Set_FrameStyle_Number_Operator,
    Set_AngleStyle_Doom8_Operator,
    Set_AngleStyle_Doom16_Operator,
    Set_AngleStyle_Simple_Operator,
    Do_Render_Operator,
    Create_RO_Operator,
    Create_SC_Operator,
    SpriteRenderPanel,
    Set_AA_On_Operator,
    Set_AA_Off_Operator,
    Set_Clockwise_Operator,
    Set_CClockwise_Operator
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
    bpy.types.Scene.sprite_anglenames = bpy.props.StringProperty(
        name = "Angle names",
        default = '12345678'
    )
    bpy.types.Scene.sprite_framestyle = bpy.props.IntProperty(
        name = 'Frame Style',
        default = 1,
    )
    bpy.types.Scene.sprite_anglestyle = bpy.props.IntProperty(
        name = 'Angle Style',
        default = 1,
    )
    bpy.types.Scene.sprite_direction = bpy.props.IntProperty(
        name = 'Rotation Direction',
        default = 1,
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
