from parser.environment import Environment
from parser.grammar.expression import Callable


class NativePrint(Callable):
    def call(self, args):
        print(args)

    def arity(self):
        return 1


class NativeLen(Callable):
    def call(self, args):
        return len(args)

    def arity(self):
        return 1


def define_natives(globals: Environment):
    globals.assign("print", NativePrint())
    globals.assign("len", NativeLen())
