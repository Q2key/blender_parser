import os
import sys

os.sys.path.append(os.getcwd())
os.sys.path.append(str.format("{0}/src",os.getcwd()))

from instance import Instance
from argparser import ArgumentParserForBlender
from commands.render_command import RenderCommand
from commands.reset_command import ResetCommand

parser = ArgumentParserForBlender()
parser.add_argument("-e", "--exec", type=str,default='render',help="execute command")
parser.add_argument("-m", "--model", type=str, default=False, help="model type | all models")
parser.add_argument("-r", "--reset", action='store_true')
args = parser.parse_args()

if __name__ == "__main__":
    if args.exec == 'render':
        c = RenderCommand(Instance(),args)
        c.run()
    if args.reset:
        c = ResetCommand(Instance(),args)
        c.run()



