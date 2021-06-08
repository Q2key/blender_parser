from workers.material_info import MaterialInfo
import bpy


class FabricWorker:

    @staticmethod
    def create_fabric_multi_material(m, scale):
        shader_scale = [1.3, 1.3, 1.3]
        if scale is not None:
            shader_scale = scale

        mi = MaterialInfo.get_material_info('fabric_material', True)

        shader_node_texture_coordinate = mi['nodes'].new("ShaderNodeTexCoord")
        shader_node_texture_coordinate.location = [-1100, -100]

        shader_node_mapping = mi['nodes'].new("ShaderNodeMapping")
        shader_node_mapping.vector_type = 'TEXTURE'

        shader_node_mapping.inputs[3].default_value[0] = shader_scale[0]
        shader_node_mapping.inputs[3].default_value[1] = shader_scale[1]
        shader_node_mapping.inputs[3].default_value[2] = shader_scale[2]
        shader_node_mapping.location = [-700, -100]

        shader_node_tex_image = mi['nodes'].new("ShaderNodeTexImage")
        shader_node_tex_image.image = bpy.data.images.load(m['texture'])
        shader_node_tex_image.location = [-300, -100]

        shader_node_bsdf_dfiffuse = mi['nodes'].new("ShaderNodeBsdfDiffuse")
        shader_node_bsdf_dfiffuse.use_custom_color = True
        shader_node_bsdf_dfiffuse.color = (200, 200, 200)
        shader_node_bsdf_dfiffuse.location = [0, -100]

        shader_node_output_material = mi['nodes'].new("ShaderNodeOutputMaterial")
        shader_node_output_material.location = [300, -100]

        mi['links'].new(shader_node_texture_coordinate.outputs["UV"], shader_node_mapping.inputs['Vector'])
        mi['links'].new(shader_node_mapping.outputs['Vector'], shader_node_tex_image.inputs["Vector"])
        mi['links'].new(shader_node_tex_image.outputs["Color"], shader_node_bsdf_dfiffuse.inputs['Color'])
        mi['links'].new(shader_node_bsdf_dfiffuse.outputs["BSDF"], shader_node_output_material.inputs['Surface'])

    @staticmethod
    def collar_seam_multi_material(m):
        mi = MaterialInfo.get_material_info('collar_seam_material', False)
        mi['nodes']['Image Texture'].image = bpy.data.images.load(m['texture'])
