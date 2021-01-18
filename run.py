
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
from commands.register_detail_command import RegisterDetailCommand
from commands.make_web_config_command import MakeWebConfigCommand

#helpers
from helpers.logger import Logger as Logger
from helpers.arguments import ArgumentsHelper
from instance import Instance

parser = ArgumentsHelper()

parser.add_argument("-m", "--model", action='append', default=None, help="model || all models")
parser.add_argument("-v", "--version", type=str, default=None)
parser.add_argument("-r", "--reset", action='store_true')
parser.add_argument("-prepare", "--prepare",action="store_true")
parser.add_argument("-store", "--store", action='store_true')
parser.add_argument("-static", "--static", action="store_true")
parser.add_argument("-d", "--debug", action="store_true")
parser.add_argument("-i", "--install", action="store_true")
parser.add_argument("-wc", "--webconfig", action="store_true")

#register command
parser.add_argument("--register", action='store_true')
parser.add_argument("--scene_name", type=str)
parser.add_argument("--prefix", type=str)
parser.add_argument("--suffix", type=str,default='')
parser.add_argument("--variant", type=str)
parser.add_argument("--material", type=str)
parser.add_argument("--configFamily", type=str)


args = parser.parse_args()

if __name__ == "__main__":
    cmd_stack = list()
    ctx = Instance()

    print(args)

    if args.register:
        cmd_stack.append(RegisterDetailCommand(ctx,args))
    if args.reset:
        cmd_stack.append(ResetCommand(ctx, args))
    if args.store:
        cmd_stack.append(ScanStoreCommand(ctx, args))
        cmd_stack.append(RenderCommand(ctx, args))
    if args.static:
        cmd_stack.append(InitCommand(ctx, args))
        cmd_stack.append(RenderCommand(ctx, args))
    if args.install:
        cmd_stack.append(InstallCommand(ctx, args))
    if args.webconfig:
        cmd_stack.append(MakeWebConfigCommand(ctx, args))

    for cmd in cmd_stack:
        cmd.run()
