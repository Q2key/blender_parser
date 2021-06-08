import os
import sys

root = os.path.dirname(__file__)
sys.path.append(root)
sys.path.append(root)

# commands
from commands.scan_store_command import ScanStoreCommand
from commands.render_command import RenderCommand
from commands.forget_command import ForgetCommand

# helpers
from helpers.arguments import ArgumentsHelper
from instance import Instance

parser = ArgumentsHelper()

parser.add_argument("-m", "--model", action='append', default=None)
parser.add_argument("-v", "--version", default=None)
parser.add_argument("-s", "--store", action='store_true')
parser.add_argument("-f", "--forget", action='store_true')
parser.add_argument("-d", "--debug", action="store_true")

args = parser.parse_args()

if __name__ == "__main__":
    cmd_stack = list()
    ctx = Instance()

    if args.store:
        cmd_stack.append(ScanStoreCommand(ctx, args))
        cmd_stack.append(RenderCommand(ctx, args))
    if args.forget:
        cmd_stack.append(ForgetCommand(ctx, args))

    for cmd in cmd_stack:
        cmd.run()
