import os
import sys
import json
import datetime
import bpy

from workers.fabric_worker import FabricWorker
from workers.plastic_worker import PlasticWorker
from workers.strings_worker import StringsWorker
from engine.engine_base import EngineBase
from helpers.process_helper import ProcessHelper as ph


class Engine(EngineBase):

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

    def process_details(self,details):
        for value in details:
            self.render_partial(value)

    def set_catchers(self, d):
        for sc in d["shadowCatchers"]:
            if sc in bpy.data.objects:
                bpy.data.objects[sc].cycles.is_shadow_catcher = True
                bpy.data.objects[sc].hide_render = False

    def set_excluded(self, d):
        for ex in d["included"]:
            if ex in bpy.data.objects:
                bpy.data.objects[ex].hide_render = False

    def set_default(self):
        for (k, v) in bpy.data.objects.items():
            if v.name not in ["Camera", "Lamp", "Lamp_0", "Lamp_1", "Lamp_2", "Lamp_4"]:
                v.hide_render = True
                v.cycles.is_shadow_catcher = False

    def before_render(self, d):
        self.set_default()
        self.set_catchers(d)
        self.set_excluded(d)

    def render_partial(self, d):
        self.before_render(d)
        p = d['filePrefix']
        r = self.ctx.SCENE['Resolution']
        for m in d['avaibleMaterials']:
            fp = str.format("{0}_{1}", p, m["id"])
            ns = ph.get_image_name(self.folder, p, fp, r)
            self.set_material(m,d['type'])
            self.render_detail(ns)
            self.save_small(ns, r)

    def set_material(self, m, mtype):
        if mtype == 'fabric':
            FabricWorker.create_fabric_multy_material(m)
        if mtype == 'plastic':
            PlasticWorker.create_gloss_plastic_material(m)
        if mtype == 'fabric':
            StringsWorker.create_strings_material(m)

    def save_small(self, ns, r):
        ph.save_small(ns, r)

    def set_scene(self):
        bpy.data.scenes["Scene"].render.engine = 'CYCLES'
        bpy.data.scenes["Scene"].render.resolution_x = self.ctx.SCENE["Resolution"]["Big"]["x"]
        bpy.data.scenes["Scene"].render.resolution_y = self.ctx.SCENE["Resolution"]["Big"]["y"]
        bpy.data.scenes["Scene"].render.resolution_percentage = self.ctx.SCENE["Percentage"]

    def render_detail(self, result):
        bpy.context.scene.render.filepath = result['b']
        bpy.ops.render.render(write_still=True)
