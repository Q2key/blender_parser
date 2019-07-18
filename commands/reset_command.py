from engine import Engine
class ResetCommand:

    def __init__(self,ctx,args):
        self.ctx = ctx
        self.args = args
    
    def run(self,ctx,args):
        print("reset")
