import os
import sys
import json
import datetime
import bpy

class Engine:
    
    def __init__(self,context):
        self.ctx = context
        self.folder = str.format("{0}/{1}",context.RENDERS_PATH,
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
        path = "{0}/{1}".format(self.ctx.RENDERS_PATH,dt)
        try:  
            os.mkdir(path)
        except OSError:  
            print ("Creation of the directory %s failed" % path)
        else:  
            print ("Successfully created the directory %s " % path)
        return path

    def set_catchers(self,d):
        ''' set shadow catchers for element '''
        for sc in d["shadowCatchers"]:
            bpy.data.objects[sc].cycles.is_shadow_catcher = True

    def set_excluded(self,d):
        ''' exclude from render '''
        for ex in d["excludedFromRender"]:
            bpy.data.objects[ex].hide_render = True

    def reset_included(self):
        ''' include all componens before render '''
        for inc in ["Body","Collar_inner","Collar_outer","Sleeve","Strings"]:
            bpy.data.objects[inc].hide_render = False

    def reset_catchers(self):
        ''' set shadow catchers for element '''
        for sc in ["Body","Collar_inner","Collar_outer","Sleeve","Strings"]:
            bpy.data.objects[sc].cycles.is_shadow_catcher = False

    def before_render(self,d):
        ''' prepare scene before interation '''
        self.reset_catchers()
        self.reset_included()
        self.set_catchers(d)
        self.set_excluded(d)

    def render_partial(self,d):
        self.before_render(d)
        for m in d['avaibleMaterials']:
            r = str.format("{0}/{1}_{2}.png",self.folder,d["filePrefix"],m["id"])
            self.set_material(m)
            self.render_detail(r)
        pass

    def set_material(self,mat):
        if mat['type'] == 'fabric_multy':
            self.create_fabric_multy_material('fabric_material',False,mat['texture'],True)

    def create_fabric_multy_material(self,mat_name='fabric_material', map=False, texture=False, cleanBefore=False):
        ''' set material '''
        # get material or create new with same name
        mat = (bpy.data.materials.get(mat_name) or
            bpy.data.materials.new(mat_name))

        # define using nodes
        mat.use_nodes = True

        # define nodes tree
        nt = mat.node_tree
        nt.name = 'ntg'
        nodes = nt.nodes
        links = nt.links

        # clear nodes
        if cleanBefore:
            nodes.clear()

        # shaderNodeTexImage
        shaderNodeTexImage = nodes.new("ShaderNodeTexImage")
        shaderNodeTexImage.image = bpy.data.images.load(texture)
        shaderNodeTexImage.use_custom_color = True
        shaderNodeTexImage.color = (200, 200, 200)
        shaderNodeTexImage.location = [-300, -100]

        if map is not False:
            # shaderNodeTexImage
            shaderNodeTexImageMap = nodes.new("ShaderNodeTexImage")
            shaderNodeTexImageMap.image = bpy.data.images.load(map)
            shaderNodeTexImageMap.use_custom_color = True
            shaderNodeTexImageMap.color = (180, 180, 0)
            shaderNodeTexImageMap.location = [0, -300]

        # shaderNodeBsdfDfiffuseWidth
        shaderNodeBsdfDfiffuse = nodes.new("ShaderNodeBsdfDiffuse")
        shaderNodeBsdfDfiffuse.use_custom_color = True
        shaderNodeBsdfDfiffuse.color = (200, 200, 200)
        shaderNodeBsdfDfiffuse.location = [0, -100]

        # shaderNodeOutputMaterial
        shaderNodeOutputMaterial = nodes.new("ShaderNodeOutputMaterial")
        shaderNodeOutputMaterial.use_custom_color = True
        shaderNodeOutputMaterial.color = (200, 200, 200)
        shaderNodeOutputMaterial.location = [300, -100]

        # link up
        links.new(shaderNodeTexImage.outputs["Color"],
                shaderNodeBsdfDfiffuse.inputs['Color'])
        links.new(shaderNodeBsdfDfiffuse.outputs["BSDF"],
                shaderNodeOutputMaterial.inputs['Surface'])
        if map is not False:
            links.new(shaderNodeTexImageMap.outputs["Color"],
                    shaderNodeOutputMaterial.inputs['Displacement'])


    def set_scene(self):
        bpy.data.scenes["Scene"].render.resolution_x = self.ctx.SCENE["Resolution"]["x"]
        bpy.data.scenes["Scene"].render.resolution_y = self.ctx.SCENE["Resolution"]["y"]
        bpy.data.scenes["Scene"].render.resolution_percentage = self.ctx.SCENE["Percentage"]


    def render_detail(self,result):
        bpy.context.scene.render.filepath = result
        bpy.ops.render.render(write_still=True)

