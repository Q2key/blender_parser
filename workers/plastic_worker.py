from workers.material_info import MaterialInfo
from workers.colors import Colors
from helpers.process_helper import ProcessHelper as ph
from constants.materials import Materials
import bpy


class PlasticWorker():

    @staticmethod
    def create_gloss_plastic_material(m=False):
        ''' set material '''

        mi = MaterialInfo.get_material_info('plastic_material', True)
        lw = mi['nodes'].new("ShaderNodeLayerWeight")
        lw.location = [0, -200]

        bd1 = mi['nodes'].new("ShaderNodeBsdfDiffuse")
        bd1.location = [0, -350]


        bd2 = mi['nodes'].new("ShaderNodeBsdfDiffuse")
        bd2.location = [0, -500]

        if m is not None:
            c = m['color']
            rgb = ph.hex2col(c, True, 2)
            bd1.inputs[0].default_value = rgb
            bd2.inputs[0].default_value = rgb
        else:
            bd2.inputs[0].default_value = (0, 0, 0, 1)
            bd2.inputs[0].default_value = (0, 0, 0, 1)

        fr = mi['nodes'].new("ShaderNodeFresnel")
        fr.location = [200,  -200]
        fr.inputs['IOR'].default_value = 1.5
        

        ms1 = mi['nodes'].new("ShaderNodeMixShader")
        ms1.location = [200, -350]

        bg = mi['nodes'].new("ShaderNodeBsdfGlossy")
        bg.location = [200, -500]
        bg.inputs[1].default_value = 0.3

        ms2 = mi['nodes'].new("ShaderNodeMixShader")
        ms2.location = [400, -350]

        om = mi['nodes'].new("ShaderNodeOutputMaterial")
        om.location = [600, -350]

        mi['links'].new(lw.outputs['Fresnel'], ms1.inputs[0])
        mi['links'].new(bd1.outputs['BSDF'], ms1.inputs[1])
        mi['links'].new(bd2.outputs['BSDF'], ms1.inputs[2])
        mi['links'].new(fr.outputs['Fac'], ms2.inputs[0])
        mi['links'].new(ms1.outputs['Shader'], ms2.inputs[1])
        mi['links'].new(bg.outputs['BSDF'], ms2.inputs[2])
        mi['links'].new(ms2.outputs['Shader'], om.inputs['Surface'])