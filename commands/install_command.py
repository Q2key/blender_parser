import os
import json
from helpers.process_helper import ProcessHelper


class InstallCommand:

    def __init__(self, ctx, args):
        self.ctx = ctx
        self.args = args

    def run(self):
        config_dict = {}
        vars_by_parent = self.ctx.SCELETON['detailVariants']
        for cfg in self.ctx.SCELETON['configPresets']:
            f = cfg['configFile']
            p = cfg['parent']
            if f not in config_dict:
                config_dict[file] = []
            variants = vars_by_parent[p]

        print(config_dict)


    def init_cfg(self):
        pass

