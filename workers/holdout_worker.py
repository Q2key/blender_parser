from workers.material_info import MaterialInfo
from workers.colors import Colors
from helpers.process import ProcessHelper as ph
from os import sys
import bpy


class HoldoutWorker():

    @staticmethod
    def apply_holdout_material(obj):
        ''' set material '''
        obj.data.materials[0] = bpy.data.materials.get('holdout_material')
