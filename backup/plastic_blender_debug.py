import bpy

def get_material_info(mat_name,cleanBefore):
    ''' get material, nodes and links for creating material '''
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
        
    return { "mat" : mat, "nodes" : nodes, "links" : links }


def create_gloss_plastic_material(mat_name='plastic', map=False, texture=False, cleanBefore=False):
    ''' set material '''
    
    mi = get_material_info(mat_name,cleanBefore)

    lw = mi['nodes'].new("ShaderNodeLayerWeight")
    lw.location = [0, -200]

    bd1 = mi['nodes'].new("ShaderNodeBsdfDiffuse")
    bd1.location = [ 0 , -350]
    bd1.inputs[0].default_value = (1, 0.8749, 0.8749, 1)

    bd2 = mi['nodes'].new("ShaderNodeBsdfDiffuse")
    bd2.location = [ 0 , -500]
    bd2.inputs[0].default_value = (1, 0.977174, 0.910533, 1)

    fr = mi['nodes'].new("ShaderNodeFresnel")
    fr.location = [ 200,  -200]
    fr.inputs['IOR'].default_value = 2

    ms1 = mi['nodes'].new("ShaderNodeMixShader")
    ms1.location = [200, -350]

    bg = mi['nodes'].new("ShaderNodeBsdfGlossy")
    bg.location = [200, -500]
    bg.inputs[1].default_value = 0.3

    ms2 = mi['nodes'].new("ShaderNodeMixShader")
    ms2.location = [400, -350]

    om = mi['nodes'].new("ShaderNodeOutputMaterial")
    om.location = [600, -350]
    
    mi['links'].new(lw.outputs['Fresnel'],ms1.inputs[0])
    mi['links'].new(bd1.outputs['BSDF'],ms1.inputs[1])
    mi['links'].new(bd2.outputs['BSDF'],ms1.inputs[2])
    mi['links'].new(fr.outputs['Fac'],ms2.inputs[0])
    mi['links'].new(ms1.outputs['Shader'],ms2.inputs[1])
    mi['links'].new(bg.outputs['BSDF'],ms2.inputs[2])
    mi['links'].new(ms2.outputs['Shader'],om.inputs['Surface'])
    

create_gloss_plastic_material()