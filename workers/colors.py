class Colors:
    def __init__(self):
        self.black = (0,0,0,1)
        self.azure = (1, 0.8749, 0.8749, 1)
        self.azureLight = (1, 0.977174, 0.910533, 1)
        self.white = (1,1,1,1)
        self.gray = (0.2,0.2,0.2,1)

    @staticmethod
    def get_color(col_id):
        colors = { "black" : (0,0,0,1) }
        if col_id in colors:
            return colors[col_id]
        else:
            return (1, 0.8749, 0.8749, 1)
