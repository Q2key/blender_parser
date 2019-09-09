class InitConfigCommand:
    
    def __init__(self, ctx, args):
        self.ctx = ctx
        self.args = args

    def run(self):
        print(self.args)
