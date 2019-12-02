class RenderedItentifier:

    def __init__(self,variant="",prefix="",suffix=""):
        self.suffix = suffix
        self.prefix = prefix
        self.variant = variant
        self.id = prefix + variant + suffix 
            
    def __get_scene_name(self):
        pass