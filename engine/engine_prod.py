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

    def prepare(self):
        print('prepare')

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
        d['available_material'] = [
            e for e in self.ctx.MATERIALS
            if e['id'] in d['available_material_id']]

    def process_details(self,d):
        if len(d['variants']) > 0:
            for v in d['variants']:
                d['file_id'] = d['prefix'] + v + d['suffix']
                d['variant'] = v
                self.before_render(d)
                self.render_partial(d)
        else :
            d['file_id'] = d['prefix'] + d['suffix']
            self.before_render(d,v)
            self.render_partial(d)

    def preprocess_details(self, d):

        d_name = d['file_id']
        v_name = d['variant']

        #toggle mask mode
        mask_mode = self.ctx.SCENE['mask_mode_on']
        self.set_layer_mask_state(mask_mode)
 
        for obj in bpy.data.objects:
            n = obj.name
            #checking displaying
            is_mask = bool(d['masks']) and n in d['masks'][v_name]
            is_included = bool(d['included']) and n in d['included'][v_name]
            is_catcher = bool(d['shadow_catchers']) and n in d['shadow_catchers']
            is_target = (n == d_name)

            if is_catcher:
                obj.cycles.is_shadow_catcher = True
                obj.layers[0] = True
                obj.layers[1] = False
                obj.hide_render = False
                print('Detail {0} : Catcher {1}'.format(n, True))

            if is_target:
                obj.layers[0] = True
                obj.layers[1] = False
                obj.hide_render = False
                print('Detail {0} : Target {1}'.format(n, True))
            
            if is_included:
                obj.layers[0] = True
                obj.layers[1] = False
                obj.hide_render = False
                print('Detail {0} : Included {1}'.format(n, True))

            if is_mask:
                obj.layers[0] = False
                obj.layers[1] = True
                obj.hide_render = False
                print('Detail {0} : Mask {1}'.format(n, True))
        #exit()
        
    
    def set_default(self):
        self.set_layer_mask_state(False)
        for (k, v) in bpy.data.objects.items():
            if v.name not in ["Camera", "Lamp", "Lamp_0"]:
                v.hide_render = True
                v.cycles.is_shadow_catcher = False

    def set_layer_mask_state(self,state):
        bpy.data.scenes['Scene'].render.layers['RenderLayer'].layers_zmask[1] = state

    def before_render(self, d):
        self.set_default()
        self.preprocess_details(d)

    def render_partial(self, d):
        self.before_render(d)
        p = d['file_id']
        r = self.ctx.SCENE['Resolution']

        #если хотим использовать только один материал
        if d['available_material'] == 'vendor':
            fp = str.format("{0}_vendor", p)
            ns = ph.get_image_name(self.folder, p, fp, r)
            self.render_detail(ns)
            self.save_small(ns, r)

        else:
            for m in d['available_material']:
                fp = str.format("{0}_{1}", p, m["id"])
                ns = ph.get_image_name(self.folder, p, fp, r)
                self.set_material(m,d)
                self.render_detail(ns)
                self.save_small(ns, r)


    def set_material(self, material, detail):
        if detail['type'] == 'fabric':
            FabricWorker.create_fabric_multy_material(material)
        if detail['type'] == 'plastic':
            PlasticWorker.create_gloss_plastic_material(material)
        if detail['type'] == 'strings':
            StringsWorker.create_strings_material(material)

    def save_big(self, ns, r):
        ph.save_big(ns, r)

    def save_small(self, ns, r):
        ph.save_small(ns, r)

    def set_scene(self):
        bpy.data.scenes["Scene"].render.engine = 'CYCLES'
        bpy.data.scenes["Scene"].render.resolution_x = self.ctx.SCENE["Resolution"]["Loseless"]["x"]
        bpy.data.scenes["Scene"].render.resolution_y = self.ctx.SCENE["Resolution"]["Loseless"]["y"]
        bpy.data.scenes["Scene"].render.resolution_percentage = self.ctx.SCENE["Percentage"]
        bpy.data.scenes["Scene"].render.image_settings.compression = self.ctx.SCENE["Compression"]

    def render_detail(self, result):
        bpy.context.scene.render.filepath = result['b']
        bpy.ops.render.render(write_still=True)
