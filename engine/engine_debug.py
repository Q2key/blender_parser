import os
import sys
import json
import datetime
import inspect

from PIL import Image
from engine.engine_base import EngineBase
from helpers.process_helper import ProcessHelper as ph
from structs.rendered_object import RenderedObject
from structs.rendered_identifier import RenderedItentifier
from structs.rendered_material import RenderedMaterial
from structs.rendered_mask import RenderedMask


class Engine(EngineBase):

    def __init__(self, ctx, args=False):
        self.ctx = ctx
        self.args = args
        self.folder = ph.get_folder_name(ctx.RENDERS_PATH)

    def go(self):
        self.set_scene()
        self.process_elements()

    def prepare(self):
        pass

    def process_elements(self):
        #define details
        details = self.ctx.DETAILS.items()
        elements = self.filter_details(details)
        #extend details
        for k, d in elements:
            print('\r\n{0}\r\n'.format(k))
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
        sc = d['shadow_catchers']
        vs = d['variants']
        am = d['available_material']
        rm = RenderedMask(d['masks'])

        for v in vs:
            # identifier
            oi = RenderedItentifier(
                variant=v,
                prefix=d['prefix'],
                suffix=d['suffix'],
                mask_details=rm.details
            )

            # material
            mi = RenderedMaterial(type=d['type'])
            # object
            ro = RenderedObject(oi, mi, sc)

            self.before_render(ro)
            self.render_partial(ro, am)

    def set_default(self):
        pass

    def set_catchers(self, ro):
        for sc in ro.catchers:
            print("cather state: ", sc, True)

    def preprocess_details(self, ro):
        print("object hided: ", ro.detail.id, False)
        if ro.detail.mask_id is not None:
            print("object hided: ", ro.detail.id, False)

    def reset_suffix(self):
        for inc in self.ctx.SCENE['Components']:
            print("object hided: ", inc, True)

    def reset_catchers(self):
        for sc in self.ctx.SCENE['Components']:
            print("cather state: ", sc, False)

    def before_render(self, ro):
        self.set_default()
        self.preprocess_details(ro)

    def render_partial(self, rendering_object, avalible_materials):
        d_id = rendering_object.detail.id
        t = rendering_object.material.type
        r = self.ctx.SCENE['Resolution']

        for m in avalible_materials:
            m_id = m["id"]
            fp = str.format("{0}_{1}", d_id, m_id)

            ns = ph.get_image_name(self.folder, d_id, fp, r)
            self.set_material(m, t)
            self.render_detail(ns)
            self.save_small(ns)

    def set_material(self, material, mtype):
        if mtype == 'fabric':
            pass
        if mtype == 'plastic':
            pass
        if mtype == 'strings':
            pass

    def save_small(self, ns):
        pass

    def set_scene(self):
        pass

    def render_detail(self, result):
        pass
