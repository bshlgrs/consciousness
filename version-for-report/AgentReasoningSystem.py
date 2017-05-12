from z3 import *
from Z3Helper import Z3Helper

class AgentReasoningSystem:
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
        self.concepts["or"] = Or
        self.concepts["*"] = lambda x, y: x * y
        self.concepts["+"] = lambda x, y: x + y
        self.concepts["implies"] = Implies
        self.concepts["int"] = IntSort()

    def axioms(self):
        axioms = []

        self.concepts["Human"] = Human = DeclareSort('Human')
        self.concepts['myself'] = Const('myself', Human)
        self.concepts["Color"] = Color = BitVecSort(5)
        self.concepts["color_quale"] = ColorQuale = BitVecSort(5)
        self.concepts["state_of_affairs"] = StateOfAffairs = DeclareSort('StateOfAffairs')

        WorldFact = DeclareSort('WorldFact')

        self.concepts['memory'] = memory = \
             Function("memory", Human, IntSort(), ColorQuale)
        self.concepts['current_quale'] = current_quale = \
                Function("current_quale", Human, ColorQuale)



        self.concepts["vision"] = vision = \
            Function("vision", Human, Color, ColorQuale)

        axioms.append(Z3Helper.myforall([Human, Human, Color, Color],
            lambda h1, h2, c1, c2:
                vision(h1, c1) - vision(h1, c2) == vision(h2, c1) - vision(h2, c2)))

        axioms.extend(self.theoretical_introspection_hypothesis_axioms())
        return axioms

    def add_lemma(self, lemma):
        res = self.check_statement(lemma)
        print res
        if res['negation_satisfiability'] == unsat:
            if res['satisfiability'] == sat:
                print "I guess that that lemma is true"
                self.solver.add(lemma)
            else:
                print "I believe a contradiction"
        else:
            if res['satisfiability'] == sat:
                print "That lemma is not provable"
            else:
                print "That lemma is provably false"

    def add_lemmas(self):
        # TODO: maybe do this
        pass


    def theoretical_introspection_hypothesis_axioms(self):
        axioms = []
        ColorQuale = self.concepts["color_quale"]
        Human = self.concepts["Human"]
        Color = self.concepts["Color"]

        vision = self.concepts["vision"]
        current_quale = self.concepts["current_quale"]

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

        return axioms

    def check_statement(self, statement):
        result = {}

        self.solver.push()

        self.solver.add(self.bot.sense_axioms())

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
