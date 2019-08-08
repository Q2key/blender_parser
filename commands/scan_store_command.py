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
        mts = self.search_for_material()
        for (k, v) in self.ctx.DETAILS.items():
            for d in v:
                mkey = d['type']
                if mkey == 'fabric':
                    d['avaibleMaterials'] = mts
                else:
                    d['avaibleMaterials'] = self.ctx.MATERIALS[mkey]

        print(mts)

    def write_config(self, file, data):
        with open(file, mode="w") as f:
            f.write(data)

    def flush_config(self):
        for k,v in self.ctx.DETAILS.items():
            file = k.lower() + '.json'
            path = str.format("{0}/_config/_details/{1}", self.ctx.STORE_PATH, file)
            self.write_config(path, json.dumps(v, indent=4))
        
        self.write_config("{0}/_config/scene.json".format(self.ctx.STORE_PATH),json.dumps(self.ctx.SCENE, indent=4))
        self.write_config("{0}/_config/materials.json".format(self.ctx.STORE_PATH),json.dumps(self.ctx.MATERIALS, indent=4))

    def run(self):
        self.search_for_material()
        self.update_config()
        self.flush_config()
