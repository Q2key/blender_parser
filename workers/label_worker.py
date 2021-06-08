from workers.material_info import MaterialInfo
import bpy


class LabelWorker:

    @staticmethod
    def label_seam_multi_material(m):
        mi = MaterialInfo.get_material_info('dev_material', False)
        mi['nodes']['Image Texture'].image = bpy.data.images.load(m['texture'])
