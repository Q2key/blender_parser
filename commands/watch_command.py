import os
import json


class WatchCommand:

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
        for (key,val) in enumerate(t):
            m.append({
                "id": str.format("[{0}]", val),
                "texture": str.format("{0}/{1}", s, val),
                "map": False,
                "type": "fabric_multy"
            })
        return m

    def extend_details(self):
        mts = self.search_for_material()
        ids = [ m["id"] for m in mts]
        for (k, v) in self.ctx.DETAILS.items():
            if v["textured"]:
                v["avaibleMaterialsID"] = ids
        self.ctx.MATERIALS.extend(mts)
    
    def write_config(self,file,data):
        with open(str.format("{0}/_config/{1}",self.ctx.STORE_PATH,file),mode="w") as f:
            f.write(data)

    def flush_config(self):
        self.write_config("details.json",json.dumps(self.ctx.DETAILS,indent=4))
        self.write_config("scene.json",json.dumps(self.ctx.SCENE,indent=4))
        self.write_config("app.json",json.dumps(self.ctx.APP,indent=4))
        self.write_config("materials.json",json.dumps(self.ctx.MATERIALS,indent=4))


    def run(self):
        self.search_for_material()
        self.extend_details()
        self.flush_config()