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

class PhilosopherBot:
    def __init__(self):
        self.memory = {}
        self.current_quale = None
        self.logic_module = PhilosopherLogicModule()

    def ask_question(self, question):
        if question[0] == "logic":
            return self.logic_module.check_statement(
                self.logic_module.build_z3_expr(question[1])
            )
        if question[0] == "logic-brief":
            res = self.logic_module.check_statement(
                self.logic_module.build_z3_expr(question[1])
            )

            if res['satisfiability'] == sat:
                if res['negation_satisfiability'] == sat:
                    return "Both that statement and its negation are possible."
                else:
                    return "That statement is provable."
            else:
                if res['negation_satisfiability'] == sat:
                    return "That statement is definitely false."
                else:
                    return "I believe a contradiction, apparently."

class PhilosopherLogicModule:
    def __init__(self):
        self.concepts = {}
        self.build_concepts()

        set_param(proof=True)
        self.solver = Solver()
        self.solver.add(self.axioms())

    def build_z3_expr(self, expr, ctx = {}):
        if isinstance(expr, basestring):
            if expr in ctx:
                return ctx[expr]
            else:
                return self.concepts[expr]
        elif expr[0] == "forall":
            _, types_sexpr, claim_sexpr = expr

            types = [Const(name, self.concepts[type_obj]) for (type_obj, name) in types_sexpr]
            claim = self.build_z3_expr(claim_sexpr, dict([str(obj), obj] for obj in types, **ctx))

            return ForAll(types, claim)
        elif expr[0] == "forsome":
            _, types_sexpr, claim_sexpr = expr

            types = [Const(name, self.concepts[type_obj]) for (type_obj, name) in types_sexpr]
            claim = self.build_z3_expr(claim_sexpr, dict([str(obj), obj] for obj in types))

            return claim
        elif expr[0] == "==":
            return self.build_z3_expr(expr[1], ctx) == self.build_z3_expr(expr[2], ctx)
        elif expr[0] == "!=":
            return self.build_z3_expr(expr[1], ctx) != self.build_z3_expr(expr[2], ctx)
        else:
            return self.concepts[expr[0]](*[self.build_z3_expr(x, ctx) for x in expr[1:]])

    def build_concepts(self):
        # We have this thing called "vision". For every human, it converts a color to a quale.
        self.concepts["vision"] = \
            Function("vision", Human, Color, Quale)
        self.concepts["human"] = Human
        self.concepts["color"] = Color
        self.concepts["quale"] = Quale
        self.concepts["and"] = And
        self.concepts["int"] = IntSort()

    def axioms(self):
        # For all humans, the experiences of viewing color1 and color2 are the same
        # iff color1 == color2.
        vision = self.concepts["vision"]
        human_vision_axiom = Z3Helper.myforall([Human, Color, Color],
            lambda observer, color1, color2:
                (color1 == color2) == (vision(observer, color1) == vision(observer, color2))
        )

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

        return axioms

    def check_statement(self, statement):
        result = {}

        self.solver.push()
        self.solver.add(Not(statement))
        negation_satisfiability = self.solver.check()
        if negation_satisfiability == sat:
            result["negation_model"] = self.solver.model()

        result["negation_satisfiability"] = negation_satisfiability

        self.solver.pop()
        self.solver.push()

        self.solver.add(statement)

        satisfiability = self.solver.check()
        if satisfiability == sat:
            result["model"] = self.solver.model()

        result["satisfiability"] = satisfiability

        self.solver.pop()

        return result

    # def eval_expr(self, statement):
    #     self.solver.check()
    #     model = self.solver.model()



philosopher_bot = PhilosopherBot()
# print philosopher_bot.ask_question(("forall", ["int", "int"], lambda x, y: x > y))

# print philosopher_bot.ask_question(
#     ("logic", ("forall", (("human", "h1"), ("human", "h2"), ("color", "c")),
#         ("==", ("vision", "h1", "c"), ("vision", "h2", "c"))))
# )


# Is it plausible that two humans have the same qualia
print philosopher_bot.ask_question(
    ("logic-brief",
        ("forsome", (("human", "h1"), ("human", "h2")),
            ("forall", (("color", "c"),), ("==", ("vision", "h1", "c"), ("vision", "h2", "c")))
    ))
)
