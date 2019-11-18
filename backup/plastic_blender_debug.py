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


def create_plastic_material(mat_name='plastic_material', map=False, texture=False, cleanBefore=True):
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


def create_fabric_material(mat_name='fabric_material', map=False, texture=False, cleanBefore=True):
    ''' set material '''
    mi = get_material_info('fabric_material',True)

    # shaderNodeTexImage
    shaderNodeTextureCoordinate = mi['nodes'].new("ShaderNodeTexCoord")
    shaderNodeTextureCoordinate.location = [-1100, -100]

    # shaderMapper
    shaderNodeMapping = mi['nodes'].new("ShaderNodeMapping")
    shaderNodeMapping.vector_type = 'TEXTURE'

    # выставляем скалирование текстуры под нормали сцены
    shaderNodeMapping.scale[0] = 0.8
    shaderNodeMapping.scale[1] = 1.6
    shaderNodeMapping.scale[2] = 0.8
    shaderNodeMapping.location = [-700, -100]

    # shaderNodeTexImage
    shaderNodeTexImage = mi['nodes'].new("ShaderNodeTexImage")
    shaderNodeTexImage.location = [-300, -100]

    # shaderNodeBsdfDfiffuseWidth
    shaderNodeBsdfDfiffuse = mi['nodes'].new("ShaderNodeBsdfDiffuse")
    shaderNodeBsdfDfiffuse.use_custom_color = True
    shaderNodeBsdfDfiffuse.color = (200, 200, 200)
    shaderNodeBsdfDfiffuse.location = [0, -100]

    # shaderNodeOutputMaterial
    shaderNodeOutputMaterial = mi['nodes'].new("ShaderNodeOutputMaterial")
    shaderNodeOutputMaterial.location = [300, -100]

    # link up
    mi['links'].new(shaderNodeTextureCoordinate.outputs["UV"],shaderNodeMapping.inputs['Vector'])
    mi['links'].new(shaderNodeMapping.outputs['Vector'],shaderNodeTexImage.inputs["Vector"])
    mi['links'].new(shaderNodeTexImage.outputs["Color"],shaderNodeBsdfDfiffuse.inputs['Color'])
    mi['links'].new(shaderNodeBsdfDfiffuse.outputs["BSDF"],shaderNodeOutputMaterial.inputs['Surface'])


def create_strings_material(m=False):
    ''' set material '''

    mi = get_material_info('strings_material', True)
    bd1 = mi['nodes'].new("ShaderNodeBsdfDiffuse")
    bd1.location = [0, 0]
    om = mi['nodes'].new("ShaderNodeOutputMaterial")
    om.location = [200, 0]

    mi['links'].new(bd1.outputs['BSDF'], om.inputs['Surface'])
