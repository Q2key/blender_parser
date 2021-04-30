import os
import sys
import json
import datetime

class Instance:

    def __init__(self):
        core_path = os.getcwd()
        src_path = core_path
        self.SRC_PATH = src_path

        self.STORE_PATH = str.format("{0}/textures/store", src_path)
        self.FABRICS_PATH = str.format("{0}/fabrics", self.STORE_PATH)
        self.BUTTONS_PATH = str.format("{0}/buttons", self.STORE_PATH)
        self.LABEL_PATH = str.format("{0}/label", self.STORE_PATH)
        self.CONFIG_PATH = str.format("{0}/config", src_path)
        self.SCENE_PATH = str.format("{0}/scenes", src_path)
        self.SCENE = self.read_json(
            str.format("{0}/config/scene.json", src_path))
        
        self.RENDERS_PATH = str.format(self.SCENE["RenderStorage"], src_path)
        self.SCENE_STATE_PATH = self.SCENE_PATH + "/state.details.txt"

        self.init_details_config()

    def init_details_config(self):

        path = self.CONFIG_PATH + '/details'
        files = os.listdir(path)

        cfg_list = {}
        for (key, val) in enumerate(files):
            k = val[:len(val) - 5]
            cfg = str.format("{0}/config/{1}/{2}",
                             self.SRC_PATH, 'details', val)
            cfg_list[k] = self.read_json(cfg)

        self.DETAILS = cfg_list

    def read_json(self, path):
        try:
            with open(path) as f:
                return json.loads(f.read())
        except OSError:
            print("Creation of the directory %s failed" % path)
