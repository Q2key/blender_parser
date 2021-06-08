from workers.material_info import MaterialInfo
import bpy


class PlasticWorker:

    @staticmethod
    def create_img_button_material(m=False):
        mi = MaterialInfo.get_material_info('img_button_material', False)
        mi['nodes']['MainTexture'].image = bpy.data.images.load(m['texture'])
        mi['nodes']['AlphaTexture'].image = bpy.data.images.load(m['texture'])
