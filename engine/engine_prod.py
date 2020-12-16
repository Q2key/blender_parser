import os
import sys
import json
import datetime
import bpy

from workers.fabric_worker import FabricWorker
from workers.plastic_worker import PlasticWorker
from workers.strings_worker import StringsWorker
from workers.label_worker import LabelWorker
from engine.engine_base import EngineBase

from helpers.process_helper import ProcessHelper as ph
from helpers.stop_watch import StopWatch
from helpers.stat_helper import StatHelper


class Engine(EngineBase):

    def __init__(self, ctx, args=False):
        self.ctx = ctx
        self.args = args
        self.folder = ph.get_folder_name(ctx.RENDERS_PATH, args)
        self.stat_helper = StatHelper()
        self.timer = StopWatch()

    def prepare(self):
        print('prepare')

    def go(self):
        self.timer.watch_start()
        self.set_scene()
        self.process_elements()
        self.timer.watch_stop()
        self.timer.print_diff()
        self.stat_helper.print_count()

    def process_elements(self):
        # define details
        details = self.ctx.DETAILS.items()
        elements = self.filter_details(details)
        # extend details
        for k, d in elements:
            print('\r\n:{0}\r\n'.format(k))
            self.process_details(d)

    def filter_details(self, elements):
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

    def process_details(self, d):
        if len(d['variants']) > 0:
            for v in d['variants']:
                d['file_id'] = d['prefix'] + v + d['suffix']
                d['variant'] = v
                print("PROCESSING DETAIL:")
                self.before_render(d)
                self.render_partial(d)
        else:
            d['file_id'] = d['prefix'] + d['suffix']
            self.before_render(d)
            self.render_partial(d)

    def preprocess_details(self, d):

        d_name = d['file_id']
        v_name = d['variant']

        for obj in bpy.data.objects:
            n = obj.name
            is_included = bool(d['included']) and n in d['included'][v_name]
            is_catcher = bool(d['shadow_catchers']
                              ) and n in d['shadow_catchers']
            is_target = (n == d_name)

            if is_catcher:
                obj.cycles.is_shadow_catcher = True
                obj.hide_render = False
                print('Detail {0} : Catcher {1}'.format(n, True))

            if is_target:
                obj.hide_render = False
                print('Detail {0} : Target {1}'.format(n, True))

            if is_included:
                obj.hide_render = False
                print('Detail {0} : Included {1}'.format(n, True))

    def set_default(self):
        for (k, v) in bpy.data.objects.items():
            if v.name not in ["Camera", "Lamp", "Lamp_0"]:
                v.hide_render = True
                v.cycles.is_shadow_catcher = False

    def before_render(self, d):
        self.set_default()
        self.preprocess_details(d)

    def render_partial(self, d):
        self.before_render(d)
        p = d['file_id']
        r = self.ctx.SCENE['Resolution']

        sp = str.format("{0}/{1}", self.folder, p)
        ph.make_folder_by_detail(sp)
        dat_file = ph.read_dat_file(sp)

        for m in d['available_material']:
            m_id = m["id"]
            if m["id"] in dat_file:
                print(str.format("{0} HAS ALREADY EXISTS", m_id))
                continue

            fp = str.format("{0}_{1}", p, m_id)
            ns = ph.get_image_name(self.folder, p, fp, r)

            self.set_material(m, d)
            self.render_detail(ns)
            self.save_small(ns, r)
            self.list_pop(sp, m_id)

    def set_material(self, material, detail):
        print(" S E T ")
        if detail['type'] == 'fabric':
            FabricWorker.create_fabric_multy_material(material)
            FabricWorker.collar_seam_multy_material(material)
        if detail['type'] == 'plastic':
            pass
        if detail['type'] == 'label':
            LabelWorker.label_seam_multy_material(material)
            pass
        if detail['type'] == 'buttons':
            PlasticWorker.create_img_button_material(material)

    def save_big(self, ns, r):
        ph.save_big(ns, r)

    def save_small(self, ns, r):
        ph.save_small(ns, r)

    def list_pop(self, path, entity):
        ph.write_stats(path, entity)

    def set_scene(self):
        s = self.ctx.SCENE
        r = s["Resolution"]
        l = r['Loseless']
        p = s["Percentage"]
        c = s["Compression"]

        bpy.data.scenes["Scene"].render.engine = 'CYCLES'
        bpy.data.scenes["Scene"].render.resolution_x = l["x"]
        bpy.data.scenes["Scene"].render.resolution_y = l["y"]
        bpy.data.scenes["Scene"].render.resolution_percentage = p
        bpy.data.scenes["Scene"].render.image_settings.compression = c

    def render_detail(self, result):
        bpy.context.scene.render.filepath = result['b']
        bpy.ops.render.render(write_still=True)
