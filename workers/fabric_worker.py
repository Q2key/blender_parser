from workers.material_info import MaterialInfo
import bpy

class FabricWorker():

    @staticmethod
    def create_fabric_multy_material(m):
        ''' set material '''

        mi = MaterialInfo.get_material_info('fabric_material',True)

        # shaderNodeTexImage
        shaderNodeTexImage = mi['nodes'].new("ShaderNodeTexImage")
        shaderNodeTexImage.image = bpy.data.images.load(m['texture'])
        shaderNodeTexImage.use_custom_color = True
        shaderNodeTexImage.color = (200, 200, 200)
        shaderNodeTexImage.location = [-300, -100]

        # shaderNodeTexImageMap
        shaderNodeTexImageMap = mi['nodes'].new("ShaderNodeTexImage")
        shaderNodeTexImageMap.image = bpy.data.images.load(m['map'])
        shaderNodeTexImageMap.use_custom_color = True
        shaderNodeTexImageMap.color = (180, 180, 0)
        shaderNodeTexImageMap.location = [0, -300]

        # shaderNodeBsdfDfiffuseWidth
        shaderNodeBsdfDfiffuse = mi['nodes'].new("ShaderNodeBsdfDiffuse")
        shaderNodeBsdfDfiffuse.use_custom_color = True
        shaderNodeBsdfDfiffuse.color = (200, 200, 200)
        shaderNodeBsdfDfiffuse.location = [0, -100]

        # shaderNodeNormalMap
        shaderNodeNormalMap = mi['nodes'].new("ShaderNodeNormalMap")
        shaderNodeNormalMap.use_custom_color = True
        shaderNodeNormalMap.color = (200, 200, 200)
        shaderNodeNormalMap.location = [0, -100]

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
        mi['links'].new(shaderNodeTexImageMap.outputs["Color"],
                  shaderNodeNormalMap.inputs['Color'])
        mi['links'].new(shaderNodeNormalMap.outputs["Normal"],
                  shaderNodeBsdfDfiffuse.inputs['Normal'])

