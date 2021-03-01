import os
import json
from helpers.process import ProcessHelper


class ScanStoreCommand:

    def __init__(self, ctx, args):
        self.ctx = ctx
        self.args = args
        self.materials = list()

    def check(self, f):
        return f.lower().endswith(tuple(self.ctx.SCENE["TexturesFormat"]))

    def scan(self, path):
        s = path
        f = os.listdir(path)
        t = [e for e in f if self.check(e)]
        m = list()
        for (key, val) in enumerate(t):
            m.append({
                "id": ProcessHelper.get_meterial_name(val),
                "texture": str.format("{0}/{1}", s, val)
            })
        return m

    def update_config(self):
        for (k, v) in self.ctx.DETAILS.items():
            m_type = v['type']
            if m_type == 'fabric':
                m = self.scan(self.ctx.FABRICS_PATH)
                v['available_material'] = m
            if m_type == 'buttons':
                m = self.scan(self.ctx.BUTTONS_PATH)
                v['available_material'] = m
            elif m_type == 'label':
                m = self.scan(self.ctx.LABEL_PATH)
                v['available_material'] = m

            elif m_type == 'preset':
                f = self.scan(self.ctx.FABRICS_PATH)
                v['available_material'] = f

    def run(self):
        self.update_config()
