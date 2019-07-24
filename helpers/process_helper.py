import datetime
import os

class ProcessHelper:

    @staticmethod
    def get_folder_name(root):
        dt = datetime.datetime.now()
        ft = dt.strftime("%d_%b_%Y_(%H_%M_%S)")
        pt = root + "/" + ft
        return pt

    @staticmethod
    def get_image_name(root):
        pass
    
    @staticmethod
    def make_folder_by_detail(detail_code):
        pass
