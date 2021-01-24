from workers.material_info import MaterialInfo
from workers.colors import Colors
from helpers.process import ProcessHelper as ph
from os import sys
import bpy


class HoldoutWorker():

    @staticmethod
    def create_holdout_material():
        ''' set material '''

        mi = MaterialInfo.get_material_info('holdout_material',True)

        shaderNodeHoldout = mi['nodes'].new("ShaderNodeHoldout")
        shaderNodeHoldout.location = [0, -100]

        shaderNodeOutputMaterial = mi['nodes'].new("ShaderNodeOutputMaterial")
        shaderNodeOutputMaterial.location = [300, -100]

        # link up
        mi['links'].new(shaderNodeHoldout.outputs["Holdout"],shaderNodeOutputMaterial.inputs['Surface'])


    @staticmethod
    def apply_holdout_material(obj):
        obj.data.materials[0] = bpy.data.materials.get('holdout_material')

    @staticmethod
    def restore_material(obj, material):
        m = ''
        if (material == 'fabric'):
            m = 'fabric_material'
        if material == 'buttons':
            m = 'img_button_material'

        obj.data.materials[0] = bpy.data.materials.get(m)
