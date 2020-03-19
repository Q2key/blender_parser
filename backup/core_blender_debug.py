import os
import sys
import json
import datetime
import bpy


def read_config(path):
    try:
        with open(path) as f:
            return json.loads(f.read())
    except OSError:  
        print ("Creation of the directory %s failed" % path)


def extend_materials(d):
    d['available_material'] = [a for a in MATERIALS if a['id'] in d['available_material_id']]

def render_all():
    for d in DETAILS:
        render_partial(DETAILS[d])

def get_folder():
    # define the name of the directory to be created
    dt = datetime.datetime.now().strftime("%d_%b_%Y_(%H_%M_%S)")
    path = "{0}/{1}".format(RENDERS_PATH,dt)
    try:  
        os.mkdir(path)
    except OSError:  
        print ("Creation of the directory %s failed" % path)
    else:  
        print ("Successfully created the directory %s " % path)
    return path

def set_catchers(d):
    ''' set shadow catchers for element '''
    for sc in d["shadow_catchers"]:
         bpy.data.objects[sc].cycles.is_shadow_catcher = True

def set_excluded(d):
    ''' exclude from render '''
    for ex in d["excludedFromRender"]:
        bpy.data.objects[ex].hide_render = True

def reset_suffix():
    ''' include all componens before render '''
    for inc in ["Body","Collar_inner","Collar_outer","Sleeve","Strings"]:
        bpy.data.objects[inc].hide_render = False

def reset_catchers():
    ''' set shadow catchers for element '''
    for sc in ["Body","Collar_inner","Collar_outer","Sleeve","Strings"]:
         bpy.data.objects[sc].cycles.is_shadow_catcher = False

def before_render(d):
    ''' prepare scene before interation '''
    reset_catchers()
    reset_suffix()
    set_catchers(d)
    set_excluded(d)

def render_partial(d):
    before_render(d)
    for m in d['available_material']:
        r = str.format("{0}/{1}_{2}.png",FOLDER,d["file_id"],m["id"])
        set_material(m)
        render_detail(r)
    pass

def set_material(mat):
    if mat['type'] == 'fabric_multy':
        create_fabric_multy_material('fabric_material',False,mat['texture'],True)

def create_fabric_multy_material(mat_name='fabric_material', map=False, texture=False, cleanBefore=False):
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

def set_scene():
    bpy.data.scenes["Scene"].render.resolution_x = SCENE["Resolution"]["x"]
    bpy.data.scenes["Scene"].render.resolution_y = SCENE["Resolution"]["y"]
    bpy.data.scenes["Scene"].render.resolution_percentage = SCENE["Percentage"]


def render_detail(result):
    bpy.context.scene.render.filepath = result
    bpy.ops.render.render(write_still=True)


def init():
    try:
        args = list(reversed(sys.argv))
        idx = args.index("--")
    except ValueError:
        params = []
    else:
        params = args[:idx][::-1]

    if len(params) > 0 :
        mode = 'all'
    else:
        mode = params[0]

    if mode == 'all':
        [ extend_materials(d) for d in DETAILS.values()]
    else:
        [ extend_materials(DETAILS[mode]) ]

if __name__ == "__main__":
    BLENDER_PATH = "C:/blender"
    SRC_PATH = str.format("{0}/src",BLENDER_PATH)
    RENDERS_PATH = str.format("{0}/renders",SRC_PATH)
    DETAILS = read_config(str.format("{0}/config/details.json",SRC_PATH))
    MATERIALS = read_config(str.format("{0}/config/materials.json",SRC_PATH))
    SCENE = read_config(str.format("{0}/config/scene.json",SRC_PATH))
    FOLDER = get_folder()

init()
set_scene()
render_all()