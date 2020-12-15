import os
import json
from helpers.process_helper import ProcessHelper


class ScanStoreCommand:

    def __init__(self, ctx, args):
        self.ctx = ctx
        self.args = args
        self.materials = list()

    def check(self, f):
        return f.lower().endswith(tuple(self.ctx.SCENE["TexturesFormat"]))

    def search_for_material(self):
        s = self.ctx.STORE_PATH
        f = os.listdir(s)
        t = [e for e in f if self.check(e)]
        m = list()
        for (key, val) in enumerate(t):
            m.append({
                "id": ProcessHelper.get_meterial_name(val),
                "texture": str.format("{0}/{1}", s, val)
            })
        return m

    def update_config(self):
        m = self.search_for_material()
        for (k, v) in self.ctx.DETAILS.items():
            mkey = v['type']
            if mkey == 'fabric':
                v['available_material'] = m
            elif bool(mkey) and mkey in self.ctx.MATERIALS:
                v['available_material'] = self.ctx.MATERIALS[mkey]
            elif mkey == 'vendor':
                v['available_material'] = 'vendor'
            elif mkey == 'buttons':
                v['available_material'] = 'buttons'

    def write_config(self, file, data):
        with open(file, mode="w") as f:
            f.write(data)

    def run(self):
        self.search_for_material()
        self.update_config()
