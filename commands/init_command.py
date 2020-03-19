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
        det = self.ctx.DETAILS.items()
        mat = self.ctx.MATERIALS
        for (key,details) in det:
            for detail in details:
                material_key = detail['type']
                detail['available_material'] = mat[material_key]

