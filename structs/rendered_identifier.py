class RenderedItentifier:

    def __init__(self,variant="",prefix="",suffix=""):
        self.suffix = suffix
        self.prefix = prefix
        self.variant = variant
        self.scene_name = suffix + variant + prefix 

    def __get_scene_name(self):
        pass