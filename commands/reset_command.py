from engine import Engine
class ResetCommand:
    
    def run(self,ctx,args):
            engine = Engine(ctx,args)
            engine.go()
