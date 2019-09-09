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
        self.ctx = ctx
        self.args = args
        self.folder = ph.get_folder_name(ctx.RENDERS_PATH)


    def go(self):
        self.set_scene()
        self.process_elements()


    def process_elements(self):
        ''' define details '''
        details = self.ctx.DETAILS.items()
        elements = self.filter_details(details)
        ''' extend details '''
        for k,d in elements:
            print('\r\n-----------{0}-----------\r\n'.format(k))
            self.process_details(d)


    def filter_details(self,elements):
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

    def process_details(self,detail):
        for variant in detail['variants']:
            detail['filePrefix'] = detail['prefix'] + variant + detail['suffix']
            self.before_render(detail)
            self.render_partial(detail)


    def set_default(self):
        pass

    def set_catchers(self, d):
        for sc in d["shadowCatchers"]:
            print("cather state: ", sc, True)

    def set_excluded(self, d):
        print("object hided: ", d['filePrefix'], False)


    def reset_suffix(self):
        for inc in self.ctx.SCENE['Components']:
            print("object hided: ", inc, True)

    def reset_catchers(self):
        for sc in self.ctx.SCENE['Components']:
            print("cather state: ", sc, False)

    def before_render(self, d):
        self.set_default()
        self.set_catchers(d)
        self.set_excluded(d)

    def render_partial(self, d):
        p = d['filePrefix']
        r = self.ctx.SCENE['Resolution']
        
        for m in d['avaibleMaterials']:
            fp = str.format("{0}_{1}", d["filePrefix"], m["id"])
            ns = ph.get_image_name(self.folder, p, fp, r)
            self.set_material(m,d['type'])
            self.render_detail(ns)
            self.save_small(ns)

    def set_material(self, material, mtype):
        if mtype == 'fabric':
            print("\r\b","-------->" , material, "---------")
        if mtype  == 'plastic':
            print("\r\b","-------->" , material, "---------")
        if mtype  == 'strings':
            print("\r\b","-------->" , material, "---------")

    def save_small(self, ns):
        pass

    def set_scene(self):
        pass

    def render_detail(self, result):
        pass
