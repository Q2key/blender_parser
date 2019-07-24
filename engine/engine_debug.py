import os
import sys
import json
import datetime
import inspect

from PIL import Image
from engine.engine_base import EngineBase

class Engine(EngineBase):

    def print_caller(fn):
        #print(inspect.stack()[1][3])
        pass

    def __init__(self, ctx, args=False):
        self.print_caller()
        self.ctx = ctx
        self.args = args
        self.folder = str.format("{0}/{1}", ctx.RENDERS_PATH,
                                 datetime.datetime.now().strftime("%d_%b_%Y_(%H_%M_%S)"))

    def extend_materials(self,d):
        self.print_caller()
        d['avaibleMaterials'] = [m for m in self.ctx.MATERIALS if m['id'] in d['avaibleMaterialsID'] ]

    def go(self):
        self.print_caller()
        self.set_scene()
        self.filter_details()
        self.extend_details()
        self.process_details()

    def filter_details(self):
        self.print_caller()
        if self.args and self.args.model:
            details = dict()
            # Iterate over all the items in dictionary
            itms = self.ctx.DETAILS.items()
            for (key, value) in itms:
                if key == self.args.model:
                    details[key] = value
            self.ctx.DETAILS = details

    def get_material(self,d):
        d['avaibleMaterials'] = [
            e for e in self.ctx.MATERIALS 
                if e['id'] in d['avaibleMaterialsID']]

    def extend_details(self):
        self.print_caller()
        vls = self.ctx.DETAILS.values()
        [ self.get_material(d) for d in vls ]

    def process_details(self):
        self.print_caller()
        itms = self.ctx.DETAILS.items()
        for key,value in itms:
            self.render_partial(value)

    def set_default(self):
        self.print_caller()

    def set_catchers(self, d):
        self.print_caller()
        for sc in d["shadowCatchers"]:
            print("cather state: ", sc, True)
            print("object hided: ", sc, False)


    def set_excluded(self, d):
        self.print_caller()
        for ex in d["included"]:
            print("object hided: ", ex, False)

    def reset_included(self):
        self.print_caller()
        for inc in self.ctx.SCENE['Components']:
            print("object hided: ", inc, True)

    def reset_catchers(self):
        self.print_caller()
        for sc in self.ctx.SCENE['Components']:
            print("cather state: ", sc, False)

    def before_render(self, d):
        self.print_caller()
        self.set_default()
        self.set_catchers(d)
        self.set_excluded(d)

    def render_partial(self, d):
        self.print_caller()
        self.before_render(d)
        for m in d['avaibleMaterials']:
            file_prefix = str.format("{0}_{1}",d["filePrefix"], m["id"])
            b = str.format("{0}/{1}_b.png", self.folder,file_prefix)
            s = str.format("{0}/{1}_s.png", self.folder,file_prefix)
            self.set_material(m)
            self.render_detail(b)
            self.save_small(b,s)

    def set_material(self, m):
        self.print_caller()
        if m['type'] == 'fabric_multy':
            pass
        if m['type'] == 'plastic_glossy':
            pass
        if m['type'] == 'strings_base':
            pass


    def save_small(self,b,s):
        self.print_caller()


    def set_scene(self):
        self.print_caller()

    def render_detail(self, result):
        self.print_caller()