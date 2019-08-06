from workers.material_info import MaterialInfo
import bpy

class FabricWorker():

    @staticmethod
    def create_fabric_multy_material(m):
        ''' set material '''

        mi = MaterialInfo.get_material_info('fabric_material',True)

        # shaderNodeTexImage
        shaderNodeTextureCoordinate = mi['nodes'].new("ShaderNodeTexCoord")
        shaderNodeTextureCoordinate.use_custom_color = True
        shaderNodeTextureCoordinate.color = (200, 200, 200)
        shaderNodeTextureCoordinate.location = [-700, -100]

        # shaderNodeTexImage
        shaderNodeTexImage = mi['nodes'].new("ShaderNodeTexImage")
        shaderNodeTexImage.image = bpy.data.images.load(m['texture'])
        shaderNodeTexImage.use_custom_color = True
        shaderNodeTexImage.color = (200, 200, 200)
        shaderNodeTexImage.location = [-300, -100]

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
        mi['links'].new(shaderNodeTextureCoordinate.outputs["UV"],
            shaderNodeTexImage.inputs['Vector'])
        mi['links'].new(shaderNodeTexImage.outputs["Color"],
                  shaderNodeBsdfDfiffuse.inputs['Color'])
        mi['links'].new(shaderNodeBsdfDfiffuse.outputs["BSDF"],
                  shaderNodeOutputMaterial.inputs['Surface'])
