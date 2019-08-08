import os
import sys
import json
import datetime
import inspect

from PIL import Image
from engine.engine_base import EngineBase
from helpers.process_helper import ProcessHelper as ph


class Engine(EngineBase):

    def print_caller(fn):
        # print(inspect.stack()[1][3])
        pass

    def __init__(self, ctx, args=False):
        self.print_caller()
        self.ctx = ctx
        self.args = args
        self.folder = ph.get_folder_name(ctx.RENDERS_PATH)


    def go(self):
        self.print_caller()
        self.set_scene()
        self.process_elements()


    def process_elements(self):
        ''' define details '''

        details = self.ctx.DETAILS
        elements = self.filter_details(details).items()
        ''' extend details '''
        for k,d in elements:
            print('\r\n-----------{0}-----------\r\n'.format(k))
            self.process_details(d)


    def filter_details(self,elements):
        self.print_caller()
        if self.args and self.args.model:
            details = dict()
            # Iterate over all the items in dictionary
            for (key, value) in elements:
                if key == self.args.model:
                    details[key] = value
            return details.items()
        return elements  

    def get_material(self, d):
        d['avaibleMaterials'] = [
            e for e in self.ctx.MATERIALS
            if e['id'] in d['avaibleMaterialsID']]

    def process_details(self,details):
        self.print_caller()
        for value in details:
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
        p = d['filePrefix']
        r = self.ctx.SCENE['Resolution']
        
        for m in d['avaibleMaterials']:
            fp = str.format("{0}_{1}", d["filePrefix"], m["id"])
            ns = ph.get_image_name(self.folder, p, fp, r)
            self.set_material(m,d['type'])
            self.render_detail(ns)
            self.save_small(ns)

    def set_material(self, m, materyal_type):
        self.print_caller()
        if materyal_type == 'fabric':
            print("\r\b","-------->" , m, "---------")
        if materyal_type == 'plastic':
            print("\r\b","-------->" , m, "---------")
        if materyal_type == 'strings':
            print("\r\b","-------->" , m, "---------")

    def save_small(self, ns):
        pass

    def set_scene(self):
        self.print_caller()

    def render_detail(self, result):
        self.print_caller()
