from workers.material_info import MaterialInfo
from workers.colors import Colors
from helpers.process import ProcessHelper as ph
from constants.materials import Materials
import bpy
import os


class PlasticWorker():

    @staticmethod
    def create_img_button_material(m=False):
        mi = MaterialInfo.get_material_info('img_button_material', False)
        cwd = os.getcwd()
        mi['nodes']['MainTexture'].image = bpy.data.images.load(
            "{0}/{1}".format(cwd, m['texture']))
        mi['nodes']['AlphaTexture'].image = bpy.data.images.load(
            "{0}/{1}".format(cwd, m['texture']))
