from z3 import *


set_param(proof=True)

# There are 16 colors
Color = BitVecSort(2)
ColorQuale = BitVecSort(2)
RED = 0


class Z3Helper:
    @staticmethod
    def enumerate_type_completely(type, options):
        thing = Const("thing-of-type-" + str(type), type)
        return And(
            ForAll([thing], Or(*[thing == option for option in options])),
            Distinct(options)
        )

    @staticmethod
    def myforall(types, claim):
        args = claim.__code__.co_varnames
        assert len(types) == len(args)
        arg_vars = [Const(arg, type) for (arg, type) in zip(args, types)]
        return ForAll(arg_vars, claim(*arg_vars))

    @staticmethod
    def myexists(types, claim):
        args = claim.__code__.co_varnames
        assert len(types) == len(args)
        arg_vars = [Const(arg, type) for (arg, type) in zip(args, types)]
        return Exists(arg_vars, claim(*arg_vars))

class PhilosopherBot:
    def __init__(self):
        self.color_memory = [1, 1, 2]
        self.current_color = 2
        self.logic_module = PhilosopherLogicModule(self)
        # self.visual_module = VisualModule(self)
        # self.attention_schema = AttentionSchema(self)

    def show_color(self, color):
        # self.visual_module.show_color(color)
        self.color_memory.append(self.current_color)
        self.current_color = color

    def memory_axioms(self):
        memory = self.logic_module.concepts["memory"]
        myself = self.logic_module.concepts["myself"]
        qualia = [Const("q" + str(time), ColorQuale) for (time, x) in enumerate(self.color_memory)]

        return ([memory(myself, time, quale) for (time, quale) in enumerate(qualia)] +
            [qualia[x_time] - qualia[y_time] == x - y
                for (x_time, x) in enumerate(self.color_memory)
                for (y_time, y) in enumerate(self.color_memory)
                if x_time < y_time])

    def current_color_axioms(self):
        current_quale = self.logic_module.concepts['current-quale']
        myself = self.logic_module.concepts["myself"]

    def ask_question(self, question):
        if question[0] == "logic":
            return self.logic_module.check_statement(
                self.logic_module.build_z3_expr(question[1])
            )
        elif question[0] == "logic-brief":
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
                    return "That statement is not consistent with my other beliefs."
                else:
                    return "I believe a contradiction, apparently."
        elif question[0] == "logic-exhibit":
            res = self.logic_module.check_statement(
               self.logic_module.build_z3_expr(('for-some', question[1], question[2]))
            )

            if res['satisfiability'] == sat:
                model = res['model']
                names = [x[1] for x in question[1]]
                return { str(x): self.logic_module.verbalize(model[x]) for x in model.decls() if str(x) in names }

        else:
            return "I don't know how to answer that"

    def current_state(self):
        if self.current_quale:
            pass



class PhilosopherLogicModule:
    def __init__(self, bot):
        self.concepts = {}
        self.bot = bot
        self.build_concepts()

        set_param(proof=True)
        self.solver = Solver()
        self.solver.add(self.axioms())

    def build_z3_expr(self, expr, ctx = {}):
        if isinstance(expr, int):
            return expr
        elif isinstance(expr, basestring):
            if expr in ctx:
                return ctx[expr]
            else:
                return self.concepts[expr]
        elif expr[0] == "for-all" or expr[0] == 'exists':
            _, types_sexpr, claim_sexpr = expr

            types = [Const(name, self.concepts[type_obj]) for (type_obj, name) in types_sexpr]
            claim = self.build_z3_expr(claim_sexpr, dict([str(obj), obj] for obj in types, **ctx))

            klass = { 'for-all': ForAll, 'exists': Exists }[expr[0]]
            return klass(types, claim)
        elif expr[0] == "let":
            _, decls_and_definitions, body = expr
            ## This line is terrible code, but I'm leaving it in because Python
            # programmers are officially okay with it. I'm using zip with a splat
            # for unzipping. Sadface.
            decls, definition_sexprs = zip(*((x[:2], x[2]) for x in decls_and_definitions))

            return self.build_z3_expr(
                ("for-all",
                    decls,
                    ("implies",
                        tuple(["and"] + list(definition_sexprs)),
                        body)
                ),
                ctx
            )

        elif expr[0] == "for-some":
            _, types_sexpr, claim_sexpr = expr
            try:
                types = [Const(name, self.concepts[type_obj]) for (type_obj, name) in types_sexpr]
            except Exception as e:
                raise Exception("error building for-some. Types needs to be an array of 2-tuples, it is %s"%(str(types_sexpr)))

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
        self.concepts["human"] = Human = DeclareSort('Human')
        self.concepts["color"] = Color
        self.concepts["color-quale"] = ColorQuale
        self.concepts["state-of-affairs"] = StateOfAffairs = DeclareSort('StateOfAffairs')

        self.concepts["vision"] = \
            Function("vision", Human, Color, ColorQuale)
        self.concepts['memory'] = Function("memory", Human, IntSort(), ColorQuale, BoolSort())
        self.concepts['current-quale'] = Function("current-quale", Human, ColorQuale, BoolSort())
#        self.concepts['show-color'] = Function("show-color", Human, Color, Human)
        self.concepts['has-illusion'] = Function("has-illusion", Human, StateOfAffairs, BoolSort())
        self.concepts['experience-of'] = Function("experience-of", Human, StateOfAffairs, ColorQuale)
        self.concepts['seeing-color'] = Function("seeing-color", Human, Color, StateOfAffairs)
        self.concepts['having-experience'] = Function("having-experience", Human, ColorQuale, StateOfAffairs)
        self.concepts['myself'] = Const('myself', Human)
        self.concepts["and"] = And
        self.concepts["*"] = lambda x, y: x * y
        self.concepts["+"] = lambda x, y: x + y
        self.concepts["implies"] = Implies
        self.concepts['age'] = Function('fghjfj2', Human, IntSort())

        self.concepts["int"] = IntSort()

    def axioms(self):
        Human = self.concepts["human"]
        Color = self.concepts["color"]
        # For all humans, the experiences of viewing color1 and color2 are the same
        # iff color1 == color2.
        # (I need this because I want there to be 0 or 1 memories of a color.)
        vision = self.concepts["vision"]
        human_vision_axiom = Z3Helper.myforall([Human, Color, Color],
            lambda observer, color1, color2:
                (color1 == color2) == (vision(observer, color1) == vision(observer, color2))
        )

        # You only remember one experience at a particular time.
        memory = self.concepts["memory"]
        memory_axiom = Z3Helper.myforall([Human, IntSort(), ColorQuale, ColorQuale],
            lambda observer, time, q1, q2:
                Implies(
                    And(memory(observer, time, q1), memory(observer, time, q2)),
                    q1 == q2
                )
        )

        # memory_creation_axiom = Z3Helper.myforall([Human, Quale, Human],
        #     lambda h1, q, h2:
        #         Implies()
        # )


        # age = self.concepts['nansai']
        # age_axiom = Z3Helper.myforall([Human, IntSort()],
        #     lambda h, age_num:
        #         And(
        #             Z3Helper.myforall([IntSort(), ColorQuale], lambda t, q:
        #                 Implies(memory(h, t, q), t < age_num)
        #             ),
        #             Z3Helper.myexists([ColorQuale], lambda q:
        #                 memory(h, age_num - 1, q)
        #             )
        #         ) == (age(h) == age_num)
        # )



        axioms = [
            human_vision_axiom,
            memory_axiom,
            # Now we assert that it's not true that for all pairs of humans and colors,
            # the humans see them the same way.
            Not(Z3Helper.myforall([Human, Human, Color],
                lambda h1, h2, c: vision(h1, c) == vision(h2, c))),
            # age_axiom
        ]

        return axioms

    def check_statement(self, statement):
        result = {}

        self.solver.push()
        self.solver.add(self.bot.memory_axioms())

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

        # pop off current state
        self.solver.pop()

        return result

    def verbalize(self, thing):
        # print thing
        return str(thing)
        if isinstance(thing, IntNumRef):
            return str(thing)
        fail()

    # def eval_expr(self, statement):
    #     self.solver.check()
    #     model = self.solver.model()

if __name__ == "__main__":
    # # Is it plausible that two humans have the same qualia associated with all colors?
    # # should say "Both that statement and its negation are possible."
    # print philosopher_bot.ask_question(
    #     ("logic-brief",
    #         ("for-some", (("human", "h1"), ("human", "h2")),
    #             ("for-all", (("color", "c"),), ("==", ("vision", "h1", "c"), ("vision", "h2", "c")))
    #     ))
    # )

    philosopher_bot = PhilosopherBot()

    # print "Q: Is it plausible that a*a == a+a"
    # print philosopher_bot.ask_question(
    #     ("logic-brief",
    #         ("for-all",
    #             [("int", "y")],
    #             ('exists', [('int', 'x')], ('==', 'x', ('+', 'y', 1)))
    #         )
    #     )
    # )

    print "Q: For all two humans, do they see colors the same?"
    print philosopher_bot.ask_question(
        ("logic-brief",
            ('for-all',
                (("human", "h1"), ("human", "h2")),
                ("and",
                    ("!=", "h1", "h2"),
                    ("for-all", (("color", "c"),), ("==", ("vision", "h1", "c"), ("vision", "h2", "c")))
                )
            )
        )
    )

    print "Q: Are my memories at timestep 1 and 2 of the same color?"
    print philosopher_bot.ask_question(
        ('logic-brief',
            ('let',
                [
                    ('color-quale', 'q1', ("memory", "myself", 2, "q1")),
                    ('color-quale', 'q2', ("memory", "myself", 1, "q2"))
                ],
                ("==", "q1", "q2")
            )
        )
    )

    # # done inverted spectrum
    # # Todo: zombies. Knowledge argument.
    print "Q: What's your age?"
    print philosopher_bot.ask_question(
        ('logic-exhibit',
            [('int', 'x')],
            (('=='), ('age', 'myself'), 'x')
        )
    )

    print "*shows color*"
    philosopher_bot.show_color(2)

    print "Q: What's your age again?"
    print philosopher_bot.ask_question(
        ('logic-exhibit',
            [('int', 'x')],
            (('=='), ('age', 'myself'), 'x')
        )
    )

    print "Q: What's 2 + 28?"
    print philosopher_bot.ask_question(
        ('logic-exhibit',
            [('int', 'x')],
            (('=='), ('+', 2, 28), 'x')
        )
    )

    print "Q: Is it possible for an agent to have an illusion of red?"
    print philosopher_bot.ask_question(
        ("logic-brief",
            ('for-some',
                [("human", "h1")],
                ("has-illusion", "h1", ("seeing-color", "h1", RED))
            )
        )
    )


    print "Q: Is it possible for an agent to have an illusion that they are having the experience of redness?"
    print philosopher_bot.ask_question(
        ("logic-brief",
            ('for-some',
                [("human", "h1")],
                ("has-illusion", "h1", ("having-experience", "h1", ("vision", "h1", RED)))
            )
        )
    )
