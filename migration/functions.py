import bpy

def normalize_object_name(needle,name):
    for (k,v) in bpy.data.objects.items():
        if k == needle:
            bpy.data.objects[k].name = name


def normalize_material_name(needle,name):
    for obj in bpy.data.objects:
        for slt in obj.material_slots:
            print(slt.name)
            if needle == slt.name:
                print(needle)
                slt.material.name = name
                
                
def delete_duplicates():
    mats = bpy.data.materials
    for obj in bpy.data.objects:
        for slt in obj.material_slots:
            part = slt.name.rpartition('.')
            print(slt.name)
            if part[2].isnumeric() and part[0] in mats:
                print(slt.name)
                slt.material = mats.get(part[0])


