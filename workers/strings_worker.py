from workers.material_info import MaterialInfo
from workers.colors import Colors
from helpers.process_helper import ProcessHelper as ph
from os import sys
import bpy

class StringsWorker():

    @staticmethod
    def create_strings_material(m=False):
        ''' set material '''

        mi = MaterialInfo.get_material_info('fabric_strings',True)

        bd1 = mi['nodes'].new("ShaderNodeBsdfDiffuse")
        bd1.location = [ 0 , 0]

        c = m['color']
        rgb = ph.hex2col(c,True,2)


        bd1.inputs[0].default_value = (rgb[0], rgb[1], rgb[2], rgb[3])
        

        om = mi['nodes'].new("ShaderNodeOutputMaterial")
        om.location = [200, 0]
        
        mi['links'].new(bd1.outputs['BSDF'],om.inputs['Surface'])
