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
                "texture": str.format("{0}/{1}", s, val),
                "map": False,
                "type": "fabric_multy"
            })
        return m

    def update_config(self):
        mts = self.search_for_material()
        ids = [m["id"] for m in mts]
        for (k, v) in self.ctx.DETAILS2.items():
            for d in v:
                material_key = d['material']
                d['avaibleMaterials'] = mts
                self.ctx.MATERIALS2[material_key] = mts

    def write_config(self, file, data):
        with open(file, mode="w") as f:
            f.write(data)

    def flush_config(self):
        for k,v in self.ctx.DETAILS2.items():
            file = k.lower() + '.json'
            path = str.format("{0}/_config/_details/{1}", self.ctx.STORE_PATH, file)
            self.write_config(path, json.dumps(v, indent=4))
        
        self.write_config("{0}/_config/scene.json".format(self.ctx.STORE_PATH),json.dumps(self.ctx.SCENE, indent=4))
        self.write_config("{0}/_config/materials.json".format(self.ctx.STORE_PATH),json.dumps(self.ctx.MATERIALS, indent=4))

    def run(self):
        self.search_for_material()
        self.update_config()
        self.flush_config()
