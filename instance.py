import os
import sys
import json
import datetime

class Instance:

    def __init__(self):
        core_path = os.getcwd()
        src_path = str.format("{0}/src",core_path)
        self.RENDERS_PATH = str.format("{0}/renders",src_path)
        self.STORE_PATH = str.format("{0}/textures/store",src_path)
        self.DETAILS = self.read_config(str.format("{0}/config/details.json",src_path))
        self.MATERIALS = self.read_config(str.format("{0}/config/materials.json",src_path))
        self.SCENE = self.read_config(str.format("{0}/config/scene.json",src_path))

    def read_config(self,path):
        try:
            with open(path) as f:
                return json.loads(f.read())
        except OSError:  
            print ("Creation of the directory %s failed" % path)

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


