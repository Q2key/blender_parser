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
    cmd_stack = list()
    ctx = Instance()

    if args.reset:
        cmd_stack.append(ResetCommand(ctx,args))
    if args.watch:
        cmd_stack.append(WatchCommand(ctx,args))
    if args.exec:
        cmd_stack.append(RenderCommand(ctx,args))
    for cmd in cmd_stack:
        cmd.run()

