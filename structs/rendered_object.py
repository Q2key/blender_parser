class RenderedObject:

    def __init__(self,detail_identifier,
        material_identifier,shadow_catchers=[],mask={}):
        self.catchers = shadow_catchers
        self.detail = detail_identifier
        self.material = material_identifier
        self.mask = mask