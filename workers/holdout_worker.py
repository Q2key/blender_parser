from workers.material_info import MaterialInfo
from helpers.process import ProcessHelper as ph
import bpy


class HoldoutWorker:

    @staticmethod
    def create_holdout_material():
        mi = MaterialInfo.get_material_info('holdout_material', True)

        shader_node_holdout = mi['nodes'].new("ShaderNodeHoldout")
        shader_node_holdout.location = [0, -100]

        shader_node_output_material = mi['nodes'].new("ShaderNodeOutputMaterial")
        shader_node_output_material.location = [300, -100]

        mi['links'].new(shader_node_holdout.outputs["Holdout"], shader_node_output_material.inputs['Surface'])

    @staticmethod
    def apply_holdout_material(obj):
        obj.data.materials[0] = bpy.data.materials.get('holdout_material')

    @staticmethod
    def restore_material(obj, detail_name, details_state_json):
        m = ph.read_json(details_state_json)
        obj.data.materials[0] = bpy.data.materials.get(m[detail_name])
