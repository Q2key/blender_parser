from engine import Engine
import os
class WatchCommand:

    def __init__(self,ctx,args):
        self.ctx = ctx
        self.args = args
        self.materials = list()

    def check(self,f):
        return f.lower().endswith(tuple(self.ctx.SCENE["TexturesFormat"]))

    def search_for_material(self):
        s = self.ctx.STORE_PATH
        f = os.listdir(s)
        t = [ e for e in f if self.check(e) ] 
        r = list()
        for (e,i) in enumerate(t):
            self.materials.append({
            "id" : str.format("dm{0}",e), 
            "texture" : str.format("{0}/{1}",s,e), 
            "map" : False, 
            "type" : "fabric_multy"  
            } )

    def extend_details(self):
        ids = [ m["id"] for m in self.materials ]
        for (k,v) in self.ctx.DETAILS.items():
            v["avaibleMaterialsID"] = ids


    def run(self):
        self.search_for_material()
        self.extend_details()
        print(self.ctx.DETAILS)


