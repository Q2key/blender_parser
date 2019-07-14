import os
import sys
os.sys.path.append(os.getcwd())
os.sys.path.append(str.format("{0}/src",os.getcwd()))

from instance import Instance
from argparser import ArgumentParserForBlender
from engine import Engine

parser = ArgumentParserForBlender()
parser.add_argument("-m", "--model", type=str, default="all", help="Number of desired quacks")
args = parser.parse_args()

if __name__ == "__main__":
    instance = Instance()
    instance.init(args.model)

    engine = Engine(instance)
    engine.go()


