from workers.material_info import MaterialInfo
from workers.colors import Colors
import bpy

class StringsWorker():

    @staticmethod
    def create_strings_material(m=False):
        ''' set material '''
        mi = MaterialInfo.get_material_info('fabric_strings',True)

        bd1 = mi['nodes'].new("ShaderNodeBsdfDiffuse")
        bd1.location = [ 0 , 0]

        c = m['color']
        bd1.inputs[0].default_value = (c['R'], c['G'], c['B'], c['A'])

        om = mi['nodes'].new("ShaderNodeOutputMaterial")
        om.location = [200, 0]
        
        mi['links'].new(bd1.outputs['BSDF'],om.inputs['Surface'])
