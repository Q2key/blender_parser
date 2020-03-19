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
            mkey = v['type']
            if mkey == 'fabric':
                v['available_material'] = mts
            else:
                v['available_material'] = self.ctx.MATERIALS[mkey]
        print(mts)

    def write_config(self, file, data):
        with open(file, mode="w") as f:
            f.write(data)

    def write_dir_tree(self, p):
        subdirs = [x for x in p.split('/') if x.find('.') is -1]
        d = subdirs[0]
        for s in subdirs:
            if s is not d:
                d = '{0}/{1}'.format(d, s)
            if os.path.exists(d):
                print('directory {0} exists'.format(d))
            else:
                print('directory {0} not exists'.format(d))
                os.mkdir(d)

    def flush_config(self):
        for k, v in self.ctx.DETAILS.items():
            file = k.lower() + '.json'
            path = str.format("{0}/_config/_details/{1}",
                              self.ctx.STORE_PATH, file)
            self.write_dir_tree(path)
            self.write_config(path, json.dumps(v, indent=4))

        self.write_config("{0}/_config/scene.json".format(self.ctx.STORE_PATH),
                          json.dumps(self.ctx.SCENE, indent=4))
        self.write_config("{0}/_config/materials.json".format(self.ctx.STORE_PATH),
                          json.dumps(self.ctx.MATERIALS, indent=4))

    def run(self):
        self.search_for_material()
        self.update_config()
        self.flush_config()
