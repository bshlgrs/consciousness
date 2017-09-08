from z3 import *
from Z3Helper import Z3Helper


class AgentReasoningSystem:
    """
    This class contains the logic used by the agent to come up with its answers
    to questions.

    You might find it easier to understand this code if you first read the glossary
    of first-order logic terms in the README.

    The most interesting code here is probably in the _axioms and
    _theoretical_introspection_hypothesis_axioms methods.

    """
    def __init__(self, agent):
        self.concepts = {}
        self.agent = agent

        # define some concepts that we want to be able to refer to, like
        # addition or multiplication
        self._build_concepts()

        # tell Z3 that I'm going to be wanting to see the proofs it constructs,
        # so it should incur the computational cost of doing proofs in such a
        # way that it can 'show me its work'
        set_param(proof=True)

        # Instantiate a Z3 solver, give it all our built-in axioms.
        # It's called a solver rather than a prover because it works by solving
        # a satisfiability problem. It is the object which does the theorem
        # proving.
        self.solver = Solver()
        self.solver.add(self._axioms())

        # Calling `push` gives us a checkpoint that we can fall back to later,
        # when we want to reset the agent to believing only what it believed
        # initially.
        self.solver.push()

        # When we ask questions of the the "evaluate" type, we want the agent
        # to answer them without particularly doing new reasoning. So here we
        # get the solver to create a model (which is a side effect of the `check`)
        # method, and then we save that model to an instance variable.
        self.solver.check()
        self.model = self.solver.model()

    def check_proposition(self, proposition):
        """
        This method takes a logical proposition, and then determines which of it
        and its negation are true (the answer can be neither or both as well as
        either one)
        """

        # initialize a dictionary to put all of the output in
        result = {}

        # make a checkpoint, so that we can revert to the previous state of the
        # solver later
        self.solver.push()

        # Add all of the current sensory input to the list of axioms that the
        # agent is currently using
        self.solver.add(self.agent._sense_axioms())

        # First, we're going to check whether the proposition could be false.
        # To do this, we assert the negation of the proposition, then we check
        # for a contradiction.

        self.solver.push()
        # To check whether a proposition is consistent with our other axioms, we
        # add it to the axioms of the solver, then we ask the solver to check
        # whether it alls its axioms are still consistent.
        self.solver.add(Not(proposition))
        negation_satisfiability = self.solver.check()

        # If there was no contradiction found, then we save the model.
        if negation_satisfiability == sat:
            result["negation_model"] = self.solver.model()

        # save to output whether the negation was satisfiable.
        result["negation_satisfiability"] = negation_satisfiability

        # Reset to the checkpoint before we added the negation of our proposition.
        self.solver.pop()
        # Create another checkpoint.
        self.solver.push()

        # Add our proposition, not negated this time.
        self.solver.add(proposition)

        satisfiability = self.solver.check()
        if satisfiability == sat:
            result["model"] = self.solver.model()

        result["satisfiability"] = satisfiability

        # Reset to before we added the proposition
        self.solver.pop()
        # Reset to before we added the sense axioms
        self.solver.pop()

        return result

    def _axioms(self):
        """
        This method creates the axioms which are built into the agent.

        All of the agent's judgements are caused by the contents of this method.
        As a result, it's probably the most important function to read for a
        casual reader.

        """
        axioms = []

        # Start out by initializing some useful sorts.

        # Make a sort for agents
        self.concepts["Agent"] = Agent = DeclareSort('Agent')
        # "Myself" refers to a particular agent.
        self.concepts['myself'] = Const('myself', Agent)

        # Define both colors and color qualia to be sorts represented as numbers
        # between 0 and 255.

        # The agent has separate concepts for Color, which is a physical color
        # in the real world, and ColorQuale, which is the experience of a
        # given color.
        self.concepts["Color"] = Color = BitVecSort(8)
        self.concepts["color_quale"] = ColorQuale = BitVecSort(8)

        # The agent thinks that memory is a function from an agent and a timestep
        # to the ColorQuale that that agent was experiencing at that timestep.
        # Note that this definition of memory means that the agent thinks that
        # memories are references to experiences rather than objective facts
        # about the world.
        self.concepts['memory'] = memory = \
             Function("memory", Agent, IntSort(), ColorQuale)

        # "current_quale" is a function from agents to their current color experience.
        self.concepts['current_quale'] = current_quale = \
                Function("current_quale", Agent, ColorQuale)

        # Vision is a function from agent and color to color quale.
        # This definition leads to intuitions that different agents might have
        # different experiences of the same color.
        self.concepts["vision"] = vision = \
            Function("vision", Agent, Color, ColorQuale)

        # Different agents have different experiences of color, but the agent
        # knows that all agents experience the differences between colors the
        # same way. This axiom asserts this.
        axioms.append(Z3Helper.for_all([Agent, Agent, Color, Color],
            lambda h1, h2, c1, c2:
                # For all humans h1 and h2, the difference between h1's experiences
                # of c1 and c2 is the same as the difference between h2's
                # experiences of those two colors.
                Z3Helper.abs(vision(h1, c1) - vision(h1, c2)) ==
                    Z3Helper.abs(vision(h2, c1) - vision(h2, c2))))

        # We also add a bunch more axioms related to Kammerer's theoretical
        # introspection hypothesis. Because those axioms are quite complicated,
        # I've separated them out into another method.
        axioms.extend(self._theoretical_introspection_hypothesis_axioms())
        return axioms


    def _theoretical_introspection_hypothesis_axioms(self):
        axioms = []
        ColorQuale = self.concepts["color_quale"]
        Agent = self.concepts["Agent"]
        Color = self.concepts["Color"]

        vision = self.concepts["vision"]
        current_quale = self.concepts["current_quale"]

        MaybeColorQuale = Z3Helper.build_maybe_sort(ColorQuale)

        WorldFact = Datatype('WorldFact')
        WorldFact.declare('ExperienceFact', ('wf_agent', Agent), ('wf_quale', ColorQuale))
        WorldFact.declare('WorldColorFact', ('wf_color', Color))
        WorldFact = WorldFact.create()
        self.concepts["ExperienceFact"] = ExperienceFact = WorldFact.ExperienceFact
        self.concepts["WorldColorFact"] = WorldColorFact = WorldFact.WorldColorFact
        wf_agent = WorldFact.wf_agent
        wf_quale = WorldFact.wf_quale
        wf_color = WorldFact.wf_color
        is_ExperienceFact = WorldFact.is_ExperienceFact
        is_WorldColorFact = WorldFact.is_WorldColorFact

        self.concepts['WorldState'] = WorldState = DeclareSort('WorldState')

        consistent_facts = Function('consistent_facts', WorldFact, WorldFact, BoolSort())
        axioms.append(Z3Helper.for_all([WorldFact, WorldFact], lambda wf1, wf2:
          consistent_facts(wf1, wf2) ==
            If(is_ExperienceFact(wf1) != is_ExperienceFact(wf2),
              True,
              If(is_ExperienceFact(wf1),
                Or(wf_quale(wf1) == wf_quale(wf2), wf_agent(wf1) != wf_agent(wf2)),
                wf1 == wf2
              )
            )
        ))

        state_contains_fact = Function('state_contains_fact', WorldState, WorldFact, BoolSort())

        # defining consistency
        axioms.append(Z3Helper.for_all([WorldState, WorldFact, WorldFact], lambda ws, wf1, wf2:
          Implies(And(state_contains_fact(ws, wf1), state_contains_fact(ws, wf2)),
            consistent_facts(wf1, wf2)
          )
        ))

        experience_of = Function('experience_of', Agent, WorldFact, MaybeColorQuale)
        axioms.append(Z3Helper.for_all([Agent, WorldFact], lambda a, wf:
          experience_of(a, wf) ==
            If(is_WorldColorFact(wf),
              MaybeColorQuale.Just(vision(a, wf_color(wf))),
              If(wf_agent(wf) == a, MaybeColorQuale.Just(wf_quale(wf)), MaybeColorQuale.Nothing)
          ))
        )

        fact_consistent_with_world = Function('fact_consistent_with_world', WorldFact, WorldState, BoolSort())
        axioms.append(Z3Helper.for_all([WorldState, WorldFact, WorldFact], lambda ws, wf1, wf2:
          Implies(
            And(fact_consistent_with_world(wf1, ws), state_contains_fact(ws, wf2)),
            consistent_facts(wf1, wf2)
          )
        ))

        self.concepts['has_illusion'] = has_illusion = Function('has_illusion', Agent, WorldState, WorldFact, BoolSort())
        axioms.append(
          Z3Helper.for_all([Agent, WorldState, WorldFact], lambda a, ws, wf:
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


    # I don't think the code below this point is very interesting to people who are reading
    # this code casually.


    def evaluate(self, expr, kind):
        """
        This allows us to ask the agent to evaluate some logical expression. For example,
        we could ask the agent to evaluate 2 + 2, or its own age.
        """
        self.solver.push()
        output = Const("output", kind)
        self.solver.add(output == expr)
        self.solver.check()
        res = self.solver.model().evaluate(output)
        self.solver.pop()
        return res


    def build_z3_expr(self, expr, ctx = {}):
        """
        This method takes an proposition expressed as a series of nested tuples,
        like this:

            ("for_some", (("Agent", "bob"), ("Agent", "jane")),
                ("for_all", (("Color", "c"),),
                 ("==", ("vision", "bob", "c"), ("vision", "jane", "c")))
            )

        and translates it into an expression that can be fed into Z3.

        This function mostly is an error-catching wrapper around
        _try_build_z3_expr.
        """
        try:
            return self._try_build_z3_expr(expr, ctx)
        except z3types.Z3Exception as e:
            print expr, "failed to build. Types:"

            for frag in expr:
                try:
                    blah = self._try_build_z3_expr(frag, ctx)
                    print frag, blah, blah.sort()
                except Exception as f:
                    pass
            raise Exception()
        except Exception as e:
            raise e


    def _try_build_z3_expr(self, expr, ctx = {}):
        """
        This method contains the nuts and bolts for translating Python tuples
        into Z3 expressions.
        """
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

    def _build_concepts(self):
        """
        Builds a few basic concepts.
        """
        self.concepts["and"] = And
        self.concepts["or"] = Or
        self.concepts["*"] = lambda x, y: x * y
        self.concepts["+"] = lambda x, y: x + y
        self.concepts["implies"] = Implies
        self.concepts["int"] = IntSort()

