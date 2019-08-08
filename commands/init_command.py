import os
import json
from helpers.process_helper import ProcessHelper


class InitCommand:

    def __init__(self, ctx, args):
        self.ctx = ctx
        self.args = args

    def run(self):
        self.init_details()

    def init_details(self):
        det = self.ctx.DETAILS2.items()
        mat = self.ctx.MATERIALS2.items()
        for (key,details) in det:
            for detail in details:
                material_key = detail['material']
                detail['avaibleMaterials'] = mat[material_key]
