from engine.engine_prod import Engine

class RenderCommand:

    def __init__(self,ctx,args):
        self.ctx = ctx
        self.args = args

    def run(self):
            engine = Engine(self.ctx,self.args)
            engine.go()

