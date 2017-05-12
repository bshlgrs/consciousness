from z3 import *
from z3_helper import Z3Helper

set_param(proof=True)

class PhilosopherBot:
    def __init__(self):
        self.color_memory = [1, 1, 2]
        self.current_color = 2
        self.logic_module = PhilosopherLogicModule(self)

    def show_color(self, color):
        # self.visual_module.show_color(color)
        self.color_memory.append(self.current_color)
        self.current_color = color

    def memory_axioms(self):
        memory = self.logic_module.concepts["memory"]
        myself = self.logic_module.concepts["myself"]
        ColorQuale = self.logic_module.concepts["color_quale"]
        qualia = [Const("q" + str(time), ColorQuale) for (time, x) in enumerate(self.color_memory)]

        return ([memory(myself, time, quale) for (time, quale) in enumerate(qualia)] +
            [qualia[x_time] - qualia[y_time] == x - y
                for (x_time, x) in enumerate(self.color_memory)
                for (y_time, y) in enumerate(self.color_memory)
                if x_time < y_time])

    def current_color_axioms(self):
        current_quale = self.logic_module.concepts['current_quale']
        myself = self.logic_module.concepts["myself"]

    def ask_question(self, question):
        if question[0] == "logic":
            return self.logic_module.check_statement(
                self.logic_module.build_z3_expr(question[1])
            )
        elif question[0] == "logic_brief":
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
        elif question[0] == "logic_exhibit":
            res = self.logic_module.check_statement(
               self.logic_module.build_z3_expr(('for_some', question[1], question[2]))
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
        try:
            return self.try_build_z3_expr(expr, ctx)
        except z3types.Z3Exception as e:
            print expr, "failed to build. Types:"
            for frag in expr:
                try:
                    blah = self.try_build_z3_expr(frag, ctx)
                    print frag, blah, blah.sort()
                except Exception as f:
                    pass
            raise Exception()
        except Exception as e:
            raise e

    def try_build_z3_expr(self, expr, ctx = {}):
        if isinstance(expr, int):
            return expr
        elif isinstance(expr, basestring):
            if expr in ctx:
                return ctx[expr]
            elif expr in self.concepts:
                return self.concepts[expr]
            else:
                raise Exception("Concept %s is not known"%expr)
        elif expr[0] == "for_all" or expr[0] == 'exists':
            _, types_sexpr, claim_sexpr = expr

            types = [Const(name, self.concepts[type_obj]) for (type_obj, name) in types_sexpr]
            claim = self.build_z3_expr(claim_sexpr, dict([str(obj), obj] for obj in types, **ctx))

            klass = { 'for_all': ForAll, 'exists': Exists }[expr[0]]
            return klass(types, claim)
        elif expr[0] == "let":
            _, decls_and_definitions, body = expr
            ## This line is terrible code, but I'm leaving it in because Python
            # programmers are officially okay with it. I'm using zip with a splat
            # for unzipping. Sadface.
            decls, definition_sexprs = zip(*((x[:2], x[2]) for x in decls_and_definitions))

            return self.build_z3_expr(
                ("for_all",
                    decls,
                    ("implies",
                        tuple(["and"] + list(definition_sexprs)),
                        body)
                ),
                ctx
            )

        elif expr[0] == "for_some":
            _, types_sexpr, claim_sexpr = expr
            for (type_obj, _) in types_sexpr:
                if type_obj not in self.concepts:
                    raise Exception("Error building for_some. Type %s was referred to but is not known."%type_obj)

            try:
                types = [Const(name, self.concepts[type_obj]) for (type_obj, name) in types_sexpr]
            except Exception as e:
                raise Exception("error building for_some. Types needs to be an array of 2_tuples, it is %s. Error: %s"%(str(types_sexpr), str(e)))

            claim = self.build_z3_expr(claim_sexpr, dict([str(obj), obj] for obj in types))
            return claim
        elif expr[0] == "==":
            return self.build_z3_expr(expr[1], ctx) == self.build_z3_expr(expr[2], ctx)
        elif expr[0] == "!=":
            return self.build_z3_expr(expr[1], ctx) != self.build_z3_expr(expr[2], ctx)
        else:
            return self.concepts[expr[0]](*[self.build_z3_expr(x, ctx) for x in expr[1:]])

    def build_concepts(self):
        self.concepts["and"] = And
        self.concepts["*"] = lambda x, y: x * y
        self.concepts["+"] = lambda x, y: x + y
        self.concepts["implies"] = Implies

        self.concepts["int"] = IntSort()

    def axioms(self):
        axioms = []

        self.concepts["Human"] = Human = DeclareSort('Human')
        self.concepts['myself'] = Const('myself', Human)
        self.concepts["color"] = Color = BitVecSort(5)
        self.concepts["color_quale"] = ColorQuale = BitVecSort(5)
        self.concepts["state_of_affairs"] = StateOfAffairs = DeclareSort('StateOfAffairs')

        WorldFact = DeclareSort('WorldFact')

        self.concepts["vision"] = vision = \
            Function("vision", Human, Color, ColorQuale)
        self.concepts['memory'] = memory = \
             Function("memory", Human, IntSort(), ColorQuale, BoolSort())
        self.concepts['current_quale'] = current_quale = \
                Function("current_quale", Human, ColorQuale)



        # You only remember one experience at a particular time.
        memory = self.concepts["memory"]
        memory_axiom = Z3Helper.myforall([Human, IntSort(), ColorQuale, ColorQuale],
            lambda observer, time, q1, q2:
                Implies(
                    And(memory(observer, time, q1), memory(observer, time, q2)),
                    q1 == q2
                )
        )
        axioms.append(memory_axiom)

        self.concepts['age'] = Function('age', Human, IntSort())

        #### Begin Kammerer stuff


        MaybeColorQuale = Z3Helper.build_maybe_sort(ColorQuale)

        WorldFact = Datatype('WorldFact')
        WorldFact.declare('ExperienceFact', ('wf_human', Human), ('wf_quale', ColorQuale))
        WorldFact.declare('WorldColorFact', ('wf_color', Color))
        WorldFact = WorldFact.create()
        self.concepts["ExperienceFact"] = ExperienceFact = WorldFact.ExperienceFact
        self.concepts["WorldColorFact"] = WorldColorFact = WorldFact.WorldColorFact
        wf_human = WorldFact.wf_human
        wf_quale = WorldFact.wf_quale
        wf_color = WorldFact.wf_color
        is_ExperienceFact = WorldFact.is_ExperienceFact
        is_WorldColorFact = WorldFact.is_WorldColorFact

        self.concepts['WorldState'] = WorldState = DeclareSort('WorldState')

        consistent_facts = Function('consistent_facts', WorldFact, WorldFact, BoolSort())
        axioms.append(Z3Helper.myforall([WorldFact, WorldFact], lambda wf1, wf2:
          consistent_facts(wf1, wf2) ==
            If(is_ExperienceFact(wf1) != is_ExperienceFact(wf2),
              True,
              If(is_ExperienceFact(wf1),
                Or(wf_quale(wf1) == wf_quale(wf2), wf_human(wf1) != wf_human(wf2)),
                wf1 == wf2
              )
            )
        ))

        state_contains_fact = Function('state_contains_fact', WorldState, WorldFact, BoolSort())

        # defining consistency
        axioms.append(Z3Helper.myforall([WorldState, WorldFact, WorldFact], lambda ws, wf1, wf2:
          Implies(And(state_contains_fact(ws, wf1), state_contains_fact(ws, wf2)),
            consistent_facts(wf1, wf2)
          )
        ))

        # define experience_of
        experience_of = Function('experience_of', Human, WorldFact, MaybeColorQuale)
        axioms.append(Z3Helper.myforall([Human, WorldFact], lambda a, wf:
          experience_of(a, wf) ==
            If(is_WorldColorFact(wf),
              MaybeColorQuale.Just(vision(a, wf_color(wf))),
              If(wf_human(wf) == a, MaybeColorQuale.Just(wf_quale(wf)), MaybeColorQuale.Nothing)
          ))
        )

        fact_consistent_with_world = Function('fact_consistent_with_world', WorldFact, WorldState, BoolSort())
        axioms.append(Z3Helper.myforall([WorldState, WorldFact, WorldFact], lambda ws, wf1, wf2:
          Implies(
            And(fact_consistent_with_world(wf1, ws), state_contains_fact(ws, wf2)),
            consistent_facts(wf1, wf2)
          )
        ))

        self.concepts['has_illusion'] = has_illusion = Function('has_illusion', Human, WorldState, WorldFact, BoolSort())
        axioms.append(
          Z3Helper.myforall([Human, WorldState, WorldFact], lambda a, ws, wf:
            has_illusion(a, ws, wf) == And(
              Not(state_contains_fact(ws, wf)),
              Implies(MaybeColorQuale.is_Just(experience_of(a, wf)),
                And(
                  current_quale(a) == MaybeColorQuale.maybe_value(experience_of(a, wf)),
                  state_contains_fact(ws,
                    ExperienceFact(a, MaybeColorQuale.maybe_value(experience_of(a, wf)))),
                )
              )
            )
          )
        )


        # End Kammerer

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
    #     ("logic_brief",
    #         ("for_some", (("Human", "h1"), ("Human", "h2")),
    #             ("for_all", (("color", "c"),), ("==", ("vision", "h1", "c"), ("vision", "h2", "c")))
    #     ))
    # )

    philosopher_bot = PhilosopherBot()

    print "Q: For all y, does there exist an x such that x = y + 1"
    print philosopher_bot.ask_question(
        ("logic_brief",
            ("for_all",
                [("int", "y")],
                ('exists', [('int', 'x')], ('==', 'x', ('+', 'y', 1)))
            )
        )
    )

    print
    print "Q: For all two humans, do they see colors the same?"
    print philosopher_bot.ask_question(
        ("logic_brief",
            ('for_all',
                (("Human", "h1"), ("Human", "h2")),
                ("and",
                    ("!=", "h1", "h2"),
                    ("for_all", (("color", "c"),), ("==", ("vision", "h1", "c"), ("vision", "h2", "c")))
                )
            )
        )
    )

    print
    print "Q: Are my memories at timestep 1 and 2 of the same color?"
    print philosopher_bot.ask_question(
        ('logic_brief',
            ('let',
                [
                    ('color_quale', 'q1', ("memory", "myself", 2, "q1")),
                    ('color_quale', 'q2', ("memory", "myself", 1, "q2"))
                ],
                ("==", "q1", "q2")
            )
        )
    )

    # # # done inverted spectrum
    # # # Todo: zombies. Knowledge argument.
    # print "Q: What's your age?"
    # print philosopher_bot.ask_question(
    #     ('logic_exhibit',
    #         [('int', 'x')],
    #         (('=='), ('age', 'myself'), 'x')
    #     )
    # )

    # print "*shows color*"
    # philosopher_bot.show_color(2)

    # print "Q: What's your age again?"
    # print philosopher_bot.ask_question(
    #     ('logic_exhibit',
    #         [('int', 'x')],
    #         (('=='), ('age', 'myself'), 'x')
    #     )
    # )

    # print "Q: What's 2 + 28?"
    # print philosopher_bot.ask_question(
    #     ('logic_exhibit',
    #         [('int', 'x')],
    #         (('=='), ('+', 2, 28), 'x')
    #     )
    # )

    print
    print "Q: Is it possible for an agent to have an illusion of red?"
    print philosopher_bot.ask_question(
        ("logic_brief",
            ('for_some',
                [("Human", "buck"), ('WorldState', 's'), ('color', 'c')],
                ("has_illusion",
                    "myself",
                    "s",
                    ("WorldColorFact", 'c')
                )
            )
        )
    )

    print
    print "Q: Is it possible for you to have the illusion that Buck is experiencing a color?"
    print philosopher_bot.ask_question(
        ("logic_brief",
            ('for_some',
                [("Human", "buck"), ('WorldState', 's'), ('color', 'c')],
                ("has_illusion",
                    "myself",
                    "s",
                    ("ExperienceFact", "buck", ("vision", "buck", 'c'))
                )
            )
        )
    )

    print
    print "Q: Is it possible for Buck to have an illusion that he is having the experience of redness?"
    print philosopher_bot.ask_question(
        ("logic_brief",
            ('for_some',
                [("Human", "buck"), ('WorldState', 's'), ('color', 'c')],
                ("has_illusion",
                    "buck",
                    "s",
                    ("ExperienceFact", "buck", ("vision", "buck", 'c'))
                )
            )
        )
    )
