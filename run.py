import os
import sys

os.sys.path.append(os.getcwd())
os.sys.path.append(str.format("{0}/src",os.getcwd()))

from instance import Instance
from argparser import ArgumentParserForBlender
from commands.render_command import RenderCommand
from commands.reset_command import ResetCommand
from commands.watch_command import WatchCommand

parser = ArgumentParserForBlender()

parser.add_argument("-m", "--model", type=str, default=False, help="model type | all models")
parser.add_argument("-r", "--reset", action='store_true')
parser.add_argument("-w", "--watch", action='store_true')
parser.add_argument("-e", "--exec", action="store_true")

args = parser.parse_args()

if __name__ == "__main__":
    cmd = None
    if args.reset:
        cmd = ResetCommand(Instance(),args)
    if args.watch:
        cmd = WatchCommand(Instance(),args)
    if args.exec:
        cmd = RenderCommand(Instance(),args)
    cmd.run()
