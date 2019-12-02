class RenderedItentifier:

    def __init__(self,variant="",prefix="",suffix="",mask={}):
        self.suffix = suffix
        self.prefix = prefix
        self.variant = variant
        self.id = prefix + variant + suffix
        self.mask_id = self.get_mask_id(mask)

    def get_mask_id(self,mask):
        if 'details' in mask and self.variant in mask['details']:
            return mask['details'][self.variant]
        return None
