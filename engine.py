import os
import sys
import json
import datetime
import bpy

from workers.fabric_worker import FabricWorker 

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
        ''' set shadow catchers for element '''
        for sc in d["shadowCatchers"]:
            bpy.data.objects[sc].cycles.is_shadow_catcher = True

    def set_excluded(self, d):
        ''' exclude from render '''
        for ex in d["excludedFromRender"]:
            bpy.data.objects[ex].hide_render = True

    def reset_included(self):
        ''' include all componens before render '''
        for inc in ["Body", "Collar_inner", "Collar_outer", "Sleeve", "Strings"]:
            bpy.data.objects[inc].hide_render = False

    def reset_catchers(self):
        ''' set shadow catchers for element '''
        for sc in ["Body", "Collar_inner", "Collar_outer", "Sleeve", "Strings"]:
            bpy.data.objects[sc].cycles.is_shadow_catcher = False

    def before_render(self, d):
        ''' prepare scene before interation '''
        self.reset_catchers()
        self.reset_included()
        self.set_catchers(d)
        self.set_excluded(d)

    def render_partial(self, d):
        self.before_render(d)
        for m in d['avaibleMaterials']:
            r = str.format("{0}/{1}_{2}.png", self.folder,
                           d["filePrefix"], m["id"])
            self.set_material(m)
            self.render_detail(r)
        pass

    def set_material(self, mat):
        if mat['type'] == 'fabric_multy':
            FabricWorker.create_fabric_multy_material(
                'fabric_material', mat['map'], mat['texture'], True)

    def set_scene(self):
        bpy.data.scenes["Scene"].render.resolution_x = self.ctx.SCENE["Resolution"]["x"]
        bpy.data.scenes["Scene"].render.resolution_y = self.ctx.SCENE["Resolution"]["y"]
        bpy.data.scenes["Scene"].render.resolution_percentage = self.ctx.SCENE["Percentage"]

    def render_detail(self, result):
        bpy.context.scene.render.filepath = result
        bpy.ops.render.render(write_still=True)
