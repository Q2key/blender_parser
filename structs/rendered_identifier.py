class RenderedItentifier:

    def __init__(self,variant="",prefix="",suffix="",mask_details={}):
        self.suffix = suffix
        self.prefix = prefix
        self.variant = variant
        self.id = prefix + variant + suffix
        self.mask_id = self.get_mask_id(mask_details)

    def get_mask_id(self,mask_details):
        v = self.variant
        if v in mask_details:
            return mask_details[v]
        return None
