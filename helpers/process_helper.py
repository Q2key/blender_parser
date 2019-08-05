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
    def get_image_name(root,subfold,file,res):
        s = 's' #str.format("{0}x{1}",res['Small']['x'],res['Small']['y']) 
        b = 'b' #str.format("{0}x{1}",res['Big']['x'],res['Big']['y'])
        return {
            "s" : str.format("{0}/{1}/{2}_{3}.png",root,subfold,file,s),
            "b" : str.format("{0}/{1}/{2}_{3}.png",root,subfold,file,b)
        }
    
    @staticmethod
    def make_folder_by_detail(detail_code):
        pass

    @staticmethod
    def get_meterial_name(raw):
        spl = raw.split('.')
        if len(spl) > 0:
            return spl[0].strip()
        return raw.strip()


    @staticmethod
    def save_small(ns,res):
        img = Image.open(ns['b'])
        new_width  = res["Small"]["x"]
        new_height = res["Small"]["y"]
        img = img.resize((new_width, new_height), Image.ANTIALIAS)
        img.save(ns['s'])

    @staticmethod
    def get_camel(raw):
        cml = '';
        spl = raw.split('_')
        cml_array = []
        for i in range(len(spl)):
            s = spl[i]
            if i > 0:
                l = s[:1].upper()
                s = s[:0] + l + s[1:]
            cml_array.append(s)
        return "".join(cml_array)
