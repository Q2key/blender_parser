class RenderedObject:

    def __init__(self,object_identifier,
        material_identifier,shadow_catchers=[]):
        self.catchers = shadow_catchers
        self.detail = object_identifier
        self.material = material_identifier