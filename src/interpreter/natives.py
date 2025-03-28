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
        return input()

    def arity(self):
        return 0


class NativeInputInt(Callable):
    def call(self, interpreter, args):
        return int(input())

    def arity(self):
        return 0


class NativeInputFloat(Callable):
    def call(self, interpreter, args):
        return float(input())

    def arity(self):
        return 0


class NativeParseInt(Callable):
    def call(self, interpreter, args):
        return int(args[0])

    def arity(self):
        return 1


class NativeSplit(Callable):
    def call(self, interpreter, args):
        if args[1] == "":
            return args[0].split()
        return args[0].split(args[1])

    def arity(self):
        return 2


class NativeParseFloat(Callable):
    def call(self, interpreter, args):
        return float(args[0])

    def arity(self):
        return 1


def define_natives(env: Environment):
    env.define("print", NativePrint())
    env.define("len", NativeLen())
    env.define("range", NativeRange())
    env.define("input", NativeInput())
    env.define("input_int", NativeInputInt())
    env.define("input_float", NativeInputFloat())
    env.define("parse_int", NativeParseInt())
    env.define("parse_float", NativeParseFloat())
    env.define("split", NativeSplit())
