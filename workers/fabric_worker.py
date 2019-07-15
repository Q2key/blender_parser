from workers.material_worker import MaterialWorker
import bpy

class FabricWorker():


    @staticmethod
    def create_fabric_multy_material(mat_name='fabric_material', map=False, texture=False, cleanBefore=False):
        ''' set material '''

        mi = MaterialWorker.get_material_info(mat_name,True)

        # shaderNodeTexImage
        shaderNodeTexImage = mi['nodes'].new("ShaderNodeTexImage")
        shaderNodeTexImage.image = bpy.data.images.load(texture)
        shaderNodeTexImage.use_custom_color = True
        shaderNodeTexImage.color = (200, 200, 200)
        shaderNodeTexImage.location = [-300, -100]

        # shaderNodeTexImageMap
        shaderNodeTexImageMap = mi['nodes'].new("ShaderNodeTexImage")
        shaderNodeTexImageMap.image = bpy.data.images.load(map)
        shaderNodeTexImageMap.use_custom_color = True
        shaderNodeTexImageMap.color = (180, 180, 0)
        shaderNodeTexImageMap.location = [0, -300]

        # shaderNodeBsdfDfiffuseWidth
        shaderNodeBsdfDfiffuse = mi['nodes'].new("ShaderNodeBsdfDiffuse")
        shaderNodeBsdfDfiffuse.use_custom_color = True
        shaderNodeBsdfDfiffuse.color = (200, 200, 200)
        shaderNodeBsdfDfiffuse.location = [0, -100]

        # shaderNodeOutputMaterial
        shaderNodeOutputMaterial = mi['nodes'].new("ShaderNodeOutputMaterial")
        shaderNodeOutputMaterial.use_custom_color = True
        shaderNodeOutputMaterial.color = (200, 200, 200)
        shaderNodeOutputMaterial.location = [300, -100]

        # link up
        mi['links'].new(shaderNodeTexImage.outputs["Color"],
                  shaderNodeBsdfDfiffuse.inputs['Color'])
        mi['links'].new(shaderNodeBsdfDfiffuse.outputs["BSDF"],
                  shaderNodeOutputMaterial.inputs['Surface'])
        mi['links'].new(shaderNodeTexImageMap.outputs["Color"],
                  shaderNodeOutputMaterial.inputs['Displacement'])
