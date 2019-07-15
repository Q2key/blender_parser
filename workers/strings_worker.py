from workers.material_worker import MaterialWorker
import bpy

from workers.material_worker import MaterialWorker

class StringsWorker():

    @staticmethod
    def create_strings_material(m=False):
        ''' set material '''

        mi = MaterialWorker.get_material_info('strings_material',True)

        bd1 = mi['nodes'].new("ShaderNodeBsdfDiffuse")
        bd1.location = [ 0 , 0]
        bd1.inputs[0].default_value = (0, 0, 0, 1)

        om = mi['nodes'].new("ShaderNodeOutputMaterial")
        om.location = [200, 0]
        
        mi['links'].new(bd1.outputs['BSDF'],om.inputs['Surface'])
