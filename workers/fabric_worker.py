from workers.material_info import MaterialInfo
import bpy

class FabricWorker():

    @staticmethod
    def create_fabric_multy_material(m, scale):
        ''' set material '''

        shader_scale = [1.3, 1.3, 1.3]
        if scale != None:
            shader_scale = scale

        mi = MaterialInfo.get_material_info('fabric_material',True)

        # shaderNodeTexImage
        shaderNodeTextureCoordinate = mi['nodes'].new("ShaderNodeTexCoord")
        shaderNodeTextureCoordinate.location = [-1100, -100]

         # shaderMapper
        shaderNodeMapping = mi['nodes'].new("ShaderNodeMapping")
        shaderNodeMapping.vector_type = 'TEXTURE'

        # выставляем скалирование текстуры
        shaderNodeMapping.inputs[3].default_value[0] = shader_scale[0]
        shaderNodeMapping.inputs[3].default_value[1] = shader_scale[1]
        shaderNodeMapping.inputs[3].default_value[2] = shader_scale[2]
        shaderNodeMapping.location = [-700, -100]

        # shaderNodeTexImage
        shaderNodeTexImage = mi['nodes'].new("ShaderNodeTexImage")
        shaderNodeTexImage.image = bpy.data.images.load(m['texture'])
        shaderNodeTexImage.location = [-300, -100]

        # shaderNodeBsdfDfiffuseWidth
        shaderNodeBsdfDfiffuse = mi['nodes'].new("ShaderNodeBsdfDiffuse")
        shaderNodeBsdfDfiffuse.use_custom_color = True
        shaderNodeBsdfDfiffuse.color = (200, 200, 200)
        shaderNodeBsdfDfiffuse.location = [0, -100]

        # shaderNodeOutputMaterial
        shaderNodeOutputMaterial = mi['nodes'].new("ShaderNodeOutputMaterial")
        shaderNodeOutputMaterial.location = [300, -100]

        # link up
        mi['links'].new(shaderNodeTextureCoordinate.outputs["UV"],shaderNodeMapping.inputs['Vector'])
        mi['links'].new(shaderNodeMapping.outputs['Vector'],shaderNodeTexImage.inputs["Vector"])
        mi['links'].new(shaderNodeTexImage.outputs["Color"],shaderNodeBsdfDfiffuse.inputs['Color'])
        mi['links'].new(shaderNodeBsdfDfiffuse.outputs["BSDF"],shaderNodeOutputMaterial.inputs['Surface'])


    @staticmethod
    def collar_seam_multy_material(m):
        mi = MaterialInfo.get_material_info('collar_seam_material',False)
        mi['nodes']['Image Texture'].image = bpy.data.images.load(m['texture'])
        