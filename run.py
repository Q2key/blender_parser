import os
import sys

os.sys.path.append(os.getcwd())
os.sys.path.append(str.format("{0}/src",os.getcwd()))

from instance import Instance
from argparser import ArgumentParserForBlender
from engine import Engine

parser = ArgumentParserForBlender()
parser.add_argument("-m", "--model", type=str, default=False, help="model type | all models")
args = parser.parse_args()

if __name__ == "__main__":
    instance = Instance()
    engine = Engine(instance,args)
    engine.go()


