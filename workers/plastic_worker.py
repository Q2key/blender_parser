from workers.material_info import MaterialInfo
from workers.colors import Colors
from helpers.process_helper import ProcessHelper as ph
from constants.materials import Materials
import bpy


class PlasticWorker():

    @staticmethod
    def create_img_button_material(m=False):
        print("\r\n BUTTONS ")
        mi = MaterialInfo.get_material_info('img_button_material', False)
        mi['nodes']['Image Texture'].image = bpy.data.images.load(m['texture'])