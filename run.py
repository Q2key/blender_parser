
import os
import sys

root = os.path.dirname(__file__)
sys.path.append(root)
sys.path.append(root)

#commands
from commands.init_command import InitCommand
from commands.scan_store_command import ScanStoreCommand
from commands.reset_command import ResetCommand
from commands.render_command import RenderCommand
from commands.install_command import InstallCommand

#helpers
from helpers.logger import Logger as Logger
from helpers.arguments_helper import ArgumentsHelper
from instance import Instance

parser = ArgumentsHelper()

parser.add_argument("-m", "--model", type=str, default=False, help="model type | all models")
parser.add_argument("-r", "--reset", action='store_true')
parser.add_argument("-prepare", "--prepare",action="store_true")
parser.add_argument("-store", "--store", action='store_true')
parser.add_argument("-static", "--static", action="store_true")
parser.add_argument("-d", "--debug", action="store_true")
parser.add_argument("-i", "--install", action="store_true")


args = parser.parse_args()

if __name__ == "__main__":
    cmd_stack = list()
    ctx = Instance()
    if args.reset:
        print('reset')
        cmd_stack.append(ResetCommand(ctx, args))
    if args.store:
        print('store')
        cmd_stack.append(ScanStoreCommand(ctx, args))
        cmd_stack.append(RenderCommand(ctx, args))
    if args.static:
        print('static')
        cmd_stack.append(InitCommand(ctx, args))
        cmd_stack.append(RenderCommand(ctx, args))
    if args.install:
        print('install')
        cmd_stack.append(InstallCommand(ctx, args))

    for cmd in cmd_stack:
        cmd.run()
