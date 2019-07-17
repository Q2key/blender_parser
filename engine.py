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

    def __init__(self, context):
        self.ctx = context
        self.folder = str.format("{0}/{1}", context.RENDERS_PATH,
                                 datetime.datetime.now().strftime("%d_%b_%Y_(%H_%M_%S)"))


    def go(self):
        self.set_scene()
        self.render_all()

    def render_all(self):
        for d in self.ctx.DETAILS:
            self.render_partial(self.ctx.DETAILS[d])

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
            bpy.data.objects[sc].cycles.is_shadow_catcher = True

    def set_excluded(self, d):
        for ex in d["excludedFromRender"]:
            bpy.data.objects[ex].hide_render = True

    def reset_included(self):
        for inc in self.ctx.SCENE['Components']:
            bpy.data.objects[inc].hide_render = False

    def reset_catchers(self):
        for sc in self.ctx.SCENE['Components']:
            bpy.data.objects[sc].cycles.is_shadow_catcher = False

    def before_render(self, d):
        self.reset_catchers()
        self.reset_included()
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
