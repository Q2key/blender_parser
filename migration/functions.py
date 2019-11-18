import bpy


def delete_duplicates():
    mats = bpy.data.materials
    for obj in bpy.data.objects:
        for slt in obj.material_slots:
            part = slt.name.rpartition('.')
            print(slt.name)
            if part[2].isnumeric() and part[0] in mats:
                print(slt.name)
                slt.material = mats.get(part[0])

def update_name(detail_scene_name,result_name):
    #check for object exists
    found = detail_scene_name in bpy.data.objects
    if found:
        #select object
        bpy.data.objects[detail_scene_name].select = True
        for obj in bpy.context.selected_objects:
            if obj.name == detail_scene_name:
                obj.name = result_name
                obj.data.name = result_name
        #deselect object
        bpy.data.objects[result_name].select = False
            
def update_material(detail_scene_name='', material=''):
    found = detail_scene_name in bpy.data.objects
    if found:
        for obj in bpy.data.objects:
            if (obj.type == 'MESH' or obj.type == 'CURVE') and obj.name == detail_scene_name:
                obj.data.materials[0].name = material
                

def update_camera(obj_camera_name):
    found = obj_camera_name in bpy.data.objects
    if found:
        c = bpy.data.objects[obj_camera_name]
        #location
        c.location[0] = 0
        c.location[1] = -6.5
        c.location[2] = 0
        #position
        c.rotation_euler[0] = 1.5708
        c.rotation_euler[1] = 0
        c.rotation_euler[2] = 0
        #scale
        c.scale[0] = 1
        c.scale[1] = 1
        c.scale[2] = 1

def update_light(obj_lamp_name):
    found = obj_lamp_name in bpy.data.objects
    if found:
        l = bpy.data.objects[obj_lamp_name]
        #location
        l.location[0] = 0
        l.location[1] = -6.5
        l.location[2] = 0
        #position
        l.rotation_euler[0] = 1.5708
        l.rotation_euler[1] = 0
        l.rotation_euler[2] = 0
        #scale
        l.scale[0] = 1
        l.scale[1] = 1
        l.scale[2] = 1


def register_detail(detail_scene_name,result_name,result_material):
    update_material(detail_scene_name,result_material)
    update_name(detail_scene_name,result_name)

def deselect_all():
    for obj in bpy.data.objects:
        obj.hide = True
        obj.hide_render = True

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
    shaderNodeMapping.scale[1] = 0.8
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



FABRIC_MATERIAL = 'fabric_material'
STRINGS_MATERIAL = 'strings_material'
PLASTIC_MATERIAL = 'plastic_material'



#materials
create_plastic_material()
create_strings_material()
create_fabric_material()

register_detail('V_1_collar','collarMao',FABRIC_MATERIAL)
register_detail('V_1_button','collarMaoButton',PLASTIC_MATERIAL)
register_detail('V_1_external_stand','collarMaoExternalStand',FABRIC_MATERIAL)
register_detail('V_1_internal_stand','collarMaoInternalStand',FABRIC_MATERIAL)
register_detail('V_1_seam_external_stand','collarMaoSeamExternalStand',STRINGS_MATERIAL)
register_detail('V_1_seam_internal_stand','collarMaoSeamInternalStand',STRINGS_MATERIAL)
register_detail('V_1_seam_collar','collarMaoSeam',STRINGS_MATERIAL)

register_detail('V_2_collar','collarMandarin',FABRIC_MATERIAL)
register_detail('V_2_button','collarMandarinButton',PLASTIC_MATERIAL)
register_detail('V_2_external_stand','collarMandarinExternalStand',FABRIC_MATERIAL)
register_detail('V_2_internal_stand','collarMandarinInternalStand',FABRIC_MATERIAL)
register_detail('V_2_seam_external_stand','collarMandarinSeamExternalStand',STRINGS_MATERIAL)
register_detail('V_2_seam_internal_stand','collarMandarinSeamInternalStand',STRINGS_MATERIAL)
register_detail('V_2_seam_collar','collarMandarinSeam',STRINGS_MATERIAL)

register_detail('V_3_collar','collarKing',FABRIC_MATERIAL)
register_detail('V_3_button','collarKingButton',PLASTIC_MATERIAL)
register_detail('V_3_external_stand','collarKingExternalStand',FABRIC_MATERIAL)
register_detail('V_3_internal_stand','collarKingInternalStand',FABRIC_MATERIAL)
register_detail('V_3_seam_external_stand','collarKingSeamExternalStand',STRINGS_MATERIAL)
register_detail('V_3_seam_internal_stand','collarKingSeamInternalStand',STRINGS_MATERIAL)
register_detail('V_3_seam_collar','collarKingSeam',STRINGS_MATERIAL)

register_detail('V_4_collar','collarCutaway',FABRIC_MATERIAL)
register_detail('V_4_button','collarCutawayButton',PLASTIC_MATERIAL)
register_detail('V_4_external_stand','collarCutawayExternalStand',FABRIC_MATERIAL)
register_detail('V_4_internal_stand','collarCutawayInternalStand',FABRIC_MATERIAL)
register_detail('V_4_seam_external_stand','collarCutawaySeamExternalStand',STRINGS_MATERIAL)
register_detail('V_4_seam_internal_stand','collarCutawaySeamInternalStand',STRINGS_MATERIAL)
register_detail('V_4_seam_collar','collarCutawaySeam',STRINGS_MATERIAL)

register_detail('V_5_collar','collarKent',FABRIC_MATERIAL)
register_detail('V_5_button','collarKentButton',PLASTIC_MATERIAL)
register_detail('V_5_external_stand','collarKentExternalStand',FABRIC_MATERIAL)
register_detail('V_5_internal_stand','collarKentInternalStand',FABRIC_MATERIAL)
register_detail('V_5_seam_external_stand','collarKentSeamExternalStand',STRINGS_MATERIAL)
register_detail('V_5_seam_internal_stand','collarKentSeamInternalStand',STRINGS_MATERIAL)
register_detail('V_5_seam_collar','collarKentSeam',STRINGS_MATERIAL)


register_detail('V_6_collar','collarWindsor',FABRIC_MATERIAL)
register_detail('V_6_button','collarWindsorButton',PLASTIC_MATERIAL)
register_detail('V_6_external_stand','collarWindsorExternalStand',FABRIC_MATERIAL)
register_detail('V_6_internal_stand','collarWindsorInternalStand',FABRIC_MATERIAL)
register_detail('V_6_seam_external_stand','collarWindsorSeamExternalStand',STRINGS_MATERIAL)
register_detail('V_6_seam_internal_stand','collarWindsorSeamInternalStand',STRINGS_MATERIAL)
register_detail('V_6_seam_collar','collarWindsorSeam',STRINGS_MATERIAL)


register_detail('V_7_collar','collarRoma',FABRIC_MATERIAL)
register_detail('V_7_button','collarRomaButton',PLASTIC_MATERIAL)
register_detail('V_7_external_stand','collarRomaExternalStand',FABRIC_MATERIAL)
register_detail('V_7_internal_stand','collarRomaInternalStand',FABRIC_MATERIAL)
register_detail('V_7_seam_external_stand','collarRomaSeamExternalStand',STRINGS_MATERIAL)
register_detail('V_7_seam_internal_stand','collarRomaSeamInternalStand',STRINGS_MATERIAL)
register_detail('V_7_seam_collar','collarRomaSeam',STRINGS_MATERIAL)

register_detail('V_8_collar','collarWingTip',FABRIC_MATERIAL)
register_detail('V_8_button','collarWingTipButton',PLASTIC_MATERIAL)
register_detail('V_8_external_stand','collarWingTipExternalStand',FABRIC_MATERIAL)
register_detail('V_8_internal_stand','collarWingTipInternalStand',FABRIC_MATERIAL)
register_detail('V_8_seam_external_stand','collarWingTipSeamExternalStand',STRINGS_MATERIAL)
register_detail('V_8_seam_internal_stand','collarWingTipSeamInternalStand',STRINGS_MATERIAL)
register_detail('V_8_seam_collar','collarWingTipSeam',STRINGS_MATERIAL)

register_detail('V_9_collar','collarColorado',FABRIC_MATERIAL)
register_detail('V_9_button','collarColoradoButton',PLASTIC_MATERIAL)
register_detail('V_9_external_stand','collarColoradoExternalStand',FABRIC_MATERIAL)
register_detail('V_9_internal_stand','collarColoradoInternalStand',FABRIC_MATERIAL)
register_detail('V_9_seam_external_stand','collarColoradoSeamExternalStand',STRINGS_MATERIAL)
register_detail('V_9_seam_internal_stand','collarColoradoSeamInternalStand',STRINGS_MATERIAL)
register_detail('V_9_seam_collar','collarColoradoSeam',STRINGS_MATERIAL)

register_detail('V_10_collar','collarColoradoMini',FABRIC_MATERIAL)
register_detail('V_10_button','collarColoradoMiniButton',PLASTIC_MATERIAL)
register_detail('V_10_external_stand','collarColoradoMiniExternalStand',FABRIC_MATERIAL)
register_detail('V_10_internal_stand','collarColoradoMiniInternalStand',FABRIC_MATERIAL)
register_detail('V_10_seam_external_stand','collarColoradoMiniSeamExternalStand',STRINGS_MATERIAL)
register_detail('V_10_seam_internal_stand','collarColoradoMiniSeamInternalStand',STRINGS_MATERIAL)
register_detail('V_10_seam_collar','collarColoradoMiniSeam',STRINGS_MATERIAL)

register_detail('V_11_collar','collarVintageClub',FABRIC_MATERIAL)
register_detail('V_11_button','collarVintageClubButton',PLASTIC_MATERIAL)
register_detail('V_11_external_stand','collarVintageClubExternalStand',FABRIC_MATERIAL)
register_detail('V_11_internal_stand','collarVintageClubInternalStand',FABRIC_MATERIAL)
register_detail('V_11_seam_external_stand','collarVintageClubSeamExternalStand',STRINGS_MATERIAL)
register_detail('V_11_seam_internal_stand','collarVintageClubSeamInternalStand',STRINGS_MATERIAL)
register_detail('V_11_seam_collar','collarVintageClubSeam',STRINGS_MATERIAL)

register_detail('V_12_collar','collarVintageClubMini',FABRIC_MATERIAL)
register_detail('V_12_button','collarVintageClubMiniButton',PLASTIC_MATERIAL)
register_detail('V_12_external_stand','collarVintageClubMiniExternalStand',FABRIC_MATERIAL)
register_detail('V_12_internal_stand','collarVintageClubMiniInternalStand',FABRIC_MATERIAL)
register_detail('V_12_seam_external_stand','collarVintageClubMiniSeamExternalStand',STRINGS_MATERIAL)
register_detail('V_12_seam_internal_stand','collarVintageClubMiniSeamInternalStand',STRINGS_MATERIAL)
register_detail('V_12_seam_collar','collarVintageClubMiniSeam',STRINGS_MATERIAL)

register_detail('V_13_collar','collarLondoner',FABRIC_MATERIAL)
register_detail('V_13_button','collarLondonerButton',PLASTIC_MATERIAL)
register_detail('V_13_external_stand','collarLondonerExternalStand',FABRIC_MATERIAL)
register_detail('V_13_internal_stand','collarLondonerInternalStand',FABRIC_MATERIAL)
register_detail('V_13_seam_external_stand','collarLondonerSeamExternalStand',STRINGS_MATERIAL)
register_detail('V_13_seam_internal_stand','collarLondonerSeamInternalStand',STRINGS_MATERIAL)
register_detail('V_13_seam_collar','collarLondonerSeam',STRINGS_MATERIAL)

#cuffs
register_detail('M_1_button','cuffOneButtonButton',PLASTIC_MATERIAL)
register_detail('M_1_external_cuff','cuffOneButtonExternal',FABRIC_MATERIAL)
register_detail('M_1_internal_cuff','cuffOneButtonInternal',FABRIC_MATERIAL)
register_detail('M_1_strings_cuff','cuffOneButtonStrings',STRINGS_MATERIAL)

register_detail('M_2_button','cuffRoundedButton',PLASTIC_MATERIAL)
register_detail('M_2_external_cuff','cuffRoundedExternal',FABRIC_MATERIAL)
register_detail('M_2_internal_cuff','cuffRoundedInternal',FABRIC_MATERIAL)
register_detail('M_2_strings_cuff','cuffRoundedStrings',STRINGS_MATERIAL)

register_detail('M_3_button','cuffRegulatedButton',PLASTIC_MATERIAL)
register_detail('M_3_external_cuff','cuffRegulatedExternal',FABRIC_MATERIAL)
register_detail('M_3_internal_cuff','cuffRegulatedInternal',FABRIC_MATERIAL)
register_detail('M_3_strings_cuff','cuffRegulatedStrings',STRINGS_MATERIAL)

register_detail('M_4_button','cuffTwoButtonsButton',PLASTIC_MATERIAL)
register_detail('M_4_external_cuff','cuffTwoButtonsExternal',FABRIC_MATERIAL)
register_detail('M_4_internal_cuff','cuffTwoButtonsInternal',FABRIC_MATERIAL)
register_detail('M_4_strings_cuff','cuffTwoButtonsStrings',STRINGS_MATERIAL)

register_detail('M_5_button','cuffFrenchButton',PLASTIC_MATERIAL)
register_detail('M_5_external_cuff','cuffFrenchExternal',FABRIC_MATERIAL)
register_detail('M_5_internal_cuff','cuffFrenchInternal',FABRIC_MATERIAL)
register_detail('M_5_strings_cuff','cuffFrenchStrings',STRINGS_MATERIAL)

register_detail('M_6_button_','cuffStraightButton',PLASTIC_MATERIAL)
register_detail('M_6_external_cuff','cuffStraightExternal',FABRIC_MATERIAL)
register_detail('M_6_internal_cuff','cuffStraightInternal',FABRIC_MATERIAL)
register_detail('M_6_strings_cuff','cuffStraightStrings',STRINGS_MATERIAL)

#body
register_detail('body_shirt','bodyShirt',FABRIC_MATERIAL)
register_detail('strings_body','bodyShirtStrings',STRINGS_MATERIAL)
register_detail('button_body','bodyShirtButton',PLASTIC_MATERIAL)
register_detail('_Body_shirt_logo','bodyShirtLogo',FABRIC_MATERIAL)
register_detail('_Body_shirt_internal_','bodyShirtInternal',FABRIC_MATERIAL)

#pocket
register_detail('Karman_body','pocket',FABRIC_MATERIAL)
register_detail('Karman_strings','pocketStrings',STRINGS_MATERIAL)

#scene
update_camera('Camera')
update_light('Lamp')

#post processing
delete_duplicates()
deselect_all()