from parser.environment import Environment
from parser.grammar.functions import Callable


class NativePrint(Callable):
    def call(self, interpreter, args):
        print(args[0])

    def arity(self):
        return 1


class NativeLen(Callable):
    def call(self, interpreter, args):
        return len(args[0])

    def arity(self):
        return 1


class NativeRange(Callable):
    def call(self, interpreter, args):
        start = args[0]
        end = args[1]
        return list(range(start, end))

    def arity(self):
        return 2


class NativeInput(Callable):
    def call(self, interpreter, args):
        return input(args[0])

    def arity(self):
        return 1


class NativeInputInt(Callable):
    def call(self, interpreter, args):
        return int(input(args[0]))

    def arity(self):
        return 1


def define_natives(env: Environment):
    env.define("print", NativePrint())
    env.define("len", NativeLen())
    env.define("range", NativeRange())
