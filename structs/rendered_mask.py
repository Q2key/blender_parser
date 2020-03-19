class RenderedMask:
    def __init__(self,mask):
        self.details = self.get_details(mask)
        self.layer_index = 1

    def get_details(self,mask):
        if 'details' in mask:
            return mask['details']
        return {}