from workers.material_info import MaterialInfo
import bpy

import os
class LabelWorker():

    @staticmethod
    def label_seam_multy_material(m):
        cwd = os.getcwd()
        mi = MaterialInfo.get_material_info('dev_material', False)
        mi['nodes']['Image Texture'].image = bpy.data.images.load(cwd + "/" + m['texture'])
