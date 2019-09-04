import os
import sys
import json
import datetime

class Instance:


    def __init__(self):
        core_path = os.getcwd()
        src_path = core_path
        self.SRC_PATH = src_path
        self.RENDERS_PATH = str.format("{0}/renders",src_path)
        self.STORE_PATH = str.format("{0}/textures/store",src_path)
        self.CONFIG_PATH = str.format("{0}/config",src_path)
        self.SCENE = self.read_config(str.format("{0}/config/scene.json",src_path))
        
        self.init_config('details')
        self.init_config('materials')


    def init_config(self,config_type):

        path = self.CONFIG_PATH + '/' + config_type
        files = os.listdir(path)

        cfg_list = {}
        for (key, val) in enumerate(files):
            k = val[:len(val) - 5]
            cfg = str.format("{0}/config/{1}/{2}",self.SRC_PATH,config_type,val)
            cfg_list[k] = self.read_config(cfg)
        
        if config_type == 'details':
            self.DETAILS = cfg_list
        if config_type == 'materials' :
            self.MATERIALS = cfg_list

    def read_config(self,path): 
        try:
            with open(path) as f:
                return json.loads(f.read())
        except OSError:  
            print ("Creation of the directory %s failed" % path)