import datetime
import os
from PIL import Image

class ProcessHelper:

    @staticmethod
    def get_folder_name(root):
        dt = datetime.datetime.now()
        ft = dt.strftime("%d_%b_%Y_(%H_%M_%S)")
        pt = root + "/" + ft
        return pt

    @staticmethod
    def get_image_name(root,pref,res):
        s = str.format("{0}x{1}",res['Small']['x'],res['Small']['y']) 
        b = str.format("{0}x{1}",res['Big']['x'],res['Big']['y'])
        return {
            "s" : str.format("{0}/{1}_{2}.png",root, pref,s),
            "b" : str.format("{0}/{1}_{2}.png",root, pref,b)
        }
    
    @staticmethod
    def make_folder_by_detail(detail_code):
        pass

    @staticmethod
    def save_small(ns,res):
        img = Image.open(ns['b'])
        new_width  = res["Small"]["x"]
        new_height = res["Small"]["y"]
        img = img.resize((new_width, new_height), Image.ANTIALIAS)
        img.save(ns['s'])
