from z3 import *

set_param(proof=True)


Quale = DeclareSort('Quale')
Color = DeclareSort('Color')
Human = DeclareSort('Human')


Red = Const("Red", Color)
Blue = Const("Blue", Color)
Green = Const("Green", Color)

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

def inverted_spectrum():
    f = Function("f", Color, Quale)
    g = Function("g", Color, Quale)

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

def inverted_spectrum_2():
    # We have this thing called "vision". For every human, it converts a color to a quale.
    vision = Function("vision", Human, Color, Quale)

    # For all humans, the experiences of viewing color1 and color2 are the same
    # iff color1 == color2.
    human_vision_axiom = Z3Helper.myforall([Human, Color, Color],
        lambda observer, color1, color2:
            (color1 == color2) == (vision(observer, color1) == vision(observer, color2))
    )

    # So we give the theorem prover all our axioms:
    axioms = [
        # there are exactly three colors, red green and blue
        Z3Helper.enumerate_type_completely(Color, [Red, Green, Blue]),
        # there are three qualia, numbers 1, 2, and 3
        Z3Helper.enumerate_type_completely(Quale, [Quale1, Quale2, Quale3]),
        human_vision_axiom,

        # Now we assert that it's not true that for all pairs of humans and colors,
        # the humans see them the same way.
        Not(Z3Helper.myforall([Human, Human, Color],
            lambda h1, h2, c: vision(h1, c) == vision(h2, c)))
    ]

    solver = Solver()
    solver.add(axioms)

    # We check if the axioms are consistent:
    print solver.check() # it responds "sat", meaning that the axioms are satisfiable
    print solver.model() # it prints a model of the axioms. To wit:

    """
        [Blue = Color!val!2,
         Quale3 = Quale!val!2,
         Quale1 = Quale!val!0,
         Quale2 = Quale!val!1,
         c!0 = Color!val!0,
         Green = Color!val!1,
         h1!2 = Human!val!0,
         Red = Color!val!0,
         h2!1 = Human!val!1,
         k!35 = [Color!val!1 -> Color!val!1,
                 Color!val!2 -> Color!val!2,
                 else -> Color!val!0],
         vision!37 = [(Human!val!1, Color!val!0) -> Quale!val!0,
                      (Human!val!1, Color!val!1) -> Quale!val!1,
                      (Human!val!0, Color!val!2) -> Quale!val!1,
                      (Human!val!0, Color!val!1) -> Quale!val!0,
                      else -> Quale!val!2],
         vision = [else -> vision!37(k!36(Var(0)), k!35(Var(1)))],
         k!36 = [Human!val!1 -> Human!val!1, else -> Human!val!0]]
    """

    # This is constructing two humans, h1!2 and h2!1.
    # In the definition of vision!37, you can see that when Human!val!1 sees
    # Color!val!0, they get Quale!val!0. But when Human!val!0 sees it, they get
    # Quale!val!2.

    # So the theorem prover has thought of inverted spectra.

inverted_spectrum_2()
