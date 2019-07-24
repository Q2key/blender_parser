import os
import sys
import json
import datetime
import bpy

from PIL import Image

from workers.fabric_worker import FabricWorker 
from workers.plastic_worker import PlasticWorker 
from workers.strings_worker import StringsWorker


class Engine:

    def __init__(self, ctx, args=False):
        self.ctx = ctx
        self.args = args
        self.folder = str.format("{0}/{1}", ctx.RENDERS_PATH,
                                 datetime.datetime.now().strftime("%d_%b_%Y_(%H_%M_%S)"))

    def extend_materials(self,d):
        d['avaibleMaterials'] = [ m for m in self.ctx.MATERIALS if m['id'] in d['avaibleMaterialsID'] ]

    def go(self):
        self.set_scene()
        self.filter_details()
        self.extend_details()
        self.process_details()

    def filter_details(self):
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
        vls = self.ctx.DETAILS.values()
        [ self.get_material(d) for d in vls ]

    def process_details(self):
        itms = self.ctx.DETAILS.items()
        for key,value in itms:
            self.render_partial(value)


    def get_folder(self):
        # define the name of the directory to be created
        dt = datetime.datetime.now().strftime("%d_%b_%Y_(%H_%M_%S)")
        path = "{0}/{1}".format(self.ctx.RENDERS_PATH, dt)
        try:
            os.mkdir(path)
        except OSError:
            print("Creation of the directory %s failed" % path)
        else:
            print("Successfully created the directory %s " % path)
        return path

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
        for (k,v) in bpy.data.objects.items():
            if v.name not in ["Camera","Lamp_0","Lamp_1","Lamp_2","Lamp_4"]:
                v.hide_render = True
                v.cycles.is_shadow_catcher = False

    def before_render(self, d):
        self.set_default()
        self.set_catchers(d)
        self.set_excluded(d)

    def render_partial(self, d):
        self.before_render(d)
        for m in d['avaibleMaterials']:
            file_prefix = str.format("{0}_{1}",d["filePrefix"], m["id"])
            b = str.format("{0}/{1}_b.png", self.folder,file_prefix)
            s = str.format("{0}/{1}_s.png", self.folder,file_prefix)
            self.set_material(m)
            self.render_detail(b)
            self.save_small(b,s)

    def set_material(self, m):
        if m['type'] == 'fabric_multy':
            FabricWorker.create_fabric_multy_material(m)
        if m['type'] == 'plastic_glossy':
            PlasticWorker.create_gloss_plastic_material(m)
        if m['type'] == 'strings_base':
            StringsWorker.create_strings_material(m)


    def save_small(self,b,s):
        img = Image.open(b)
        new_width  = self.ctx.SCENE["Resolution"]["Small"]["x"]
        new_height = self.ctx.SCENE["Resolution"]["Small"]["y"]
        img = img.resize((new_width, new_height), Image.ANTIALIAS)
        img.save(s)


    def set_scene(self):
        bpy.data.scenes["Scene"].render.engine = 'CYCLES'
        bpy.data.scenes["Scene"].render.resolution_x = self.ctx.SCENE["Resolution"]["Big"]["x"]
        bpy.data.scenes["Scene"].render.resolution_y = self.ctx.SCENE["Resolution"]["Big"]["y"]
        bpy.data.scenes["Scene"].render.resolution_percentage = self.ctx.SCENE["Percentage"]

    def render_detail(self, result):
        bpy.context.scene.render.filepath = result
        bpy.ops.render.render(write_still=True)
