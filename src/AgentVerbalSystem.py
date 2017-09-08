from z3 import sat, unsat




class AgentVerbalSystem:
    """
    This class contains the logic that controls how the agent uses its reasoning system to
    answer questions.
    """
    def __init__(self, reasoning_system):
        self.reasoning_system = reasoning_system


    def respond_to_question(self, question):
        """
        This method contains the logic the agent uses to answer questions it's given.
        """

        # The agent can answer five types of questions. These are pretty redundant--
        # they're just thin wrappers around the same functionality.
        if question[0] == "logic":
            # The agent takes a proposition, evaluates, and prints out all of the
            # output of its reasoning system. This one is mostly used for debugging.
            return self.reasoning_system.check_statement(
                self.reasoning_system.build_z3_expr(question[1])
            )
        elif question[0] == "logic_brief":
            # The agent takes a proposition, and checks its satisfiability:
            res = self.reasoning_system.check_statement(
                self.reasoning_system.build_z3_expr(question[1])
            )

            # It now uses the results about satisfiability and the satisfiability
            # of the negation to answer the question "Is $PROPOSITION true", where
            # $PROPOSITION is the proposition we passed in.

            # There are four different possible answers, depending on the satisfiability
            # of the statement and its negation.

            # You might ask why we bother checking whether the statement's negation
            # is satisfiable. This is because you only know that a statement is
            # guaranteed to be true unless you know that the statement's negation is
            # unsatisfiable. See https://en.wikipedia.org/wiki/Satisfiability#Reduction_of_validity_to_satisfiability

            if res['satisfiability'] == sat:
                if res['negation_satisfiability'] == sat:
                    return "Both that statement and its negation are possible."
                else:
                    return "Yes."
            else:
                if res['negation_satisfiability'] == sat:
                    return "No."
                else:
                    return "I believe a contradiction, apparently."
        elif question[0] == "is_it_possible":
            # This takes a proposition and answers the question "Is this proposition possible?"

            # This is just the same thing as the `logic_brief` query, but it returns English
            # sentences to correspond to the question "Is this proposition possible" instead
            # of "Is this proposition true". This makes the usage of this code slightly
            # more intuitive.
            res = self.reasoning_system.check_statement(
                self.reasoning_system.build_z3_expr(question[1])
            )

            if res['satisfiability'] == sat:
                if res['negation_satisfiability'] == sat:
                    return "Yes."
                else:
                    return "Yes. In fact, it's guaranteed by my other beliefs."
            else:
                if res['negation_satisfiability'] == sat:
                    return "No, that's impossible."
                else:
                    return "I believe a contradiction, apparently."

        elif question[0] == "logic_exhibit":
            # This allows us to ask the agent to output the model which causes it to
            # believe something is possible.

            # So we can ask "give me a number which is divisible by two", and it
            # will search for an example of such a number, and return that number.

            # Z3 proves the satisfiability of a proposition by creating explicit finite
            # models in which the proposition is true. So producing models under which a
            # particular proposition is true is very closely related to its normal
            # functionality.
            res = self.reasoning_system.check_statement(
               self.reasoning_system.build_z3_expr(('for_some', question[1], question[2]))
            )

            if res['satisfiability'] == sat:
                model = res['model']
                names = [x[1] for x in question[1]]
                return { str(x): self.reasoning_system.verbalize(model[x]) for x in model.decls() if str(x) in names }

        elif question[0] == "evaluate":
            # This allows us to ask the agent to evaluate some logical expression. For example,
            # we could ask the agent to evaluate 2 + 2, or its own age.
            return self.reasoning_system.evaluate(
                self.reasoning_system.build_z3_expr(question[1]),
                self.reasoning_system.build_z3_expr(question[2]))
        else:
            return "I don't know how to answer that"

