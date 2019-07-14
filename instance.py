import os
import sys
import json
import datetime

class Instance:

    def __init__(self):
        self.BLENDER_PATH = "C:/blender"
        self.SRC_PATH = str.format("{0}/src",self.BLENDER_PATH)
        self.RENDERS_PATH = str.format("{0}/renders",self.SRC_PATH)
        self.DETAILS = self.read_config(str.format("{0}/config/details.json",self.SRC_PATH))
        self.MATERIALS = self.read_config(str.format("{0}/config/materials.json",self.SRC_PATH))
        self.SCENE = self.read_config(str.format("{0}/config/scene.json",self.SRC_PATH))


    def read_config(self,path):
        try:
            with open(path) as f:
                return json.loads(f.read())
        except OSError:  
            print ("Creation of the directory %s failed" % path)

    def extend_materials(self,d):
        d['avaibleMaterials'] = [a for a in self.MATERIALS if a['id'] in d['avaibleMaterialsID']]


    def get_folder(self):
        # define the name of the directory to be created
        dt = datetime.datetime.now().strftime("%d_%b_%Y_(%H_%M_%S)")
        path = "{0}/{1}".format(self.RENDERS_PATH,dt)
        try:  
            os.mkdir(path)
        except OSError:  
            print ("Creation of the directory %s failed" % path)
        else:  
            print ("Successfully created the directory %s " % path)
        return path

    def init(self,model):
        if model == 'all':
            [ self.extend_materials(d) for d in self.DETAILS.values()]
        else:
            [ self.extend_materials(self.DETAILS[model]) ]


