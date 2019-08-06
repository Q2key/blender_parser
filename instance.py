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
        self.DETAILS2 = {}

        self.DETAILS2['BODY'] = self.read_config(str.format("{0}/config/details/body.json",src_path))
        self.DETAILS2['BUTTONS'] = self.read_config(str.format("{0}/config/details/buttons.json",src_path))

        #Воротники
        self.DETAILS2['COLLARS_INTERNAL'] = self.read_config(str.format("{0}/config/details/collarsInternal.json",src_path))
        self.DETAILS2['COLLARS_INTERNAL_STRINGS'] = self.read_config(str.format("{0}/config/details/collarsInternalStrings.json",src_path))
        self.DETAILS2['COLLARS'] = self.read_config(str.format("{0}/config/details/collars.json",src_path))

        #Манжеты
        self.DETAILS2['CUFFS'] = self.read_config(str.format("{0}/config/details/cuffs.json",src_path))
        self.DETAILS2['CUFFS_BUTTONS'] = self.read_config(str.format("{0}/config/details/cuffsButtons.json",src_path))
        self.DETAILS2['CUFFS_INTERNAL'] = self.read_config(str.format("{0}/config/details/cuffsInternal.json",src_path))
        self.DETAILS2['CUFFS_STRINGS'] = self.read_config(str.format("{0}/config/details/cuffsStrings.json",src_path))


        self.DETAILS2['STRINGS'] = self.read_config(str.format("{0}/config/details/strings.json",src_path))

        self.COLLARS = self.read_config(str.format("{0}/config/details/collars.json",src_path))
        self.MATERIALS = self.read_config(str.format("{0}/config/materials.json",src_path))
        self.SCENE = self.read_config(str.format("{0}/config/scene.json",src_path))


    def read_config(self,path): 
        try:
            with open(path) as f:
                return json.loads(f.read())
        except OSError:  
            print ("Creation of the directory %s failed" % path)