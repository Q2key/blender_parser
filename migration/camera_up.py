import bpy

def set_camera():
    c = bpy.data.objects["Camera"]
    #location
    c.location[0] = 0
    c.location[1] = -6.5
    c.location[2] = 0
    #position
    c.rotation_euler[0] = 1.5708
    c.rotation_euler[1] = 0
    c.rotation_euler[2] = 0
    #scale
    c.scale[0] = 1
    c.scale[1] = 1
    c.scale[2] = 1


set_camera()