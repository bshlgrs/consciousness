from z3 import *

set_param(proof=True)


Quale = DeclareSort('Quale')
Color = DeclareSort('Color')

f = Function("f", Color, Quale)
g = Function("g", Color, Quale)

xColor = Const("xColor", Color)
yColor = Const("yColor", Color)

Red = Const("Red", Color)
Blue = Const("Blue", Color)
Green = Const("Green", Color)

xQuale = Const("xQuale", Quale)

Quale1 = Const("Quale1", Quale)
Quale2 = Const("Quale2", Quale)
Quale3 = Const("Quale3", Quale)

class Z3Helper:
    @staticmethod
    def enumerate_type_completely(type, options):
        blah = Const("blah", type)
        return And(
            ForAll([blah], Or(*[blah == option for option in options])),
            Distinct(options)
        )

    @staticmethod
    def myforall(types, claim):
        args = claim.__code__.co_varnames
        assert len(types) == len(args)
        arg_vars = [Const(arg, type) for (arg, type) in zip(args, types)]
        return ForAll(arg_vars, claim(*arg_vars))

print Z3Helper.myforall([Color], lambda x: x == Red)

axioms = [
    Z3Helper.myforall([Color, Color], lambda x, y: (x == y) == (f(x) == f(y))),
    Z3Helper.myforall([Color, Color], lambda x, y: (x == y) == (g(x) == g(y))),
    Z3Helper.enumerate_type_completely(Color, [Red, Green, Blue]),
    Z3Helper.enumerate_type_completely(Quale, [Quale1, Quale2, Quale3]),
    Not(Z3Helper.myforall([Color], lambda x: f(x) == g(x)))]

solver = Solver()
solver.add(axioms)

## Inverted spectrum
print solver.check()
print solver.model()
print solver.model().eval(f(Green))
print solver.model().eval(g(Green))

