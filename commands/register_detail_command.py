import os
import json
from helpers.process_helper import ProcessHelper


class RegisterDetailCommand:

    def __init__(self, ctx, args):
        self.ctx = ctx
        self.args = args

    def run(self):
        self.add_detail_to_cfg()

    def add_detail_to_cfg(self):
        conf = {}
        detailRoot = self.args.configFamily
        hasKey = self.args.configFamily in self.ctx.DETAILS
        if hasKey:
            vv = self.args.variant
            dd = self.ctx.DETAILS[detailRoot]['variants']
            conf['suffix'] = self.args.suffix
            conf['prefix'] = self.args.prefix
            conf['configFamily'] = self.args.configFamily
            conf['variants'] = self.extend_variants(dd,vv) 

        conf_json = json.dumps(conf, sort_keys=True, indent=4)
        self.write_confg(self.ctx.CONFIG_PATH + '\\'  + self.args.configFamily + '_ext.json',conf_json)

    def extend_variants(self,variants,new_variant):
        if new_variant not in variants:
            variants.append(new_variant)
        return variants

    def write_confg(self,name,data):
        with open(name, mode="w") as f:
            f.write(data)


    def apply_material(self):
        pass
