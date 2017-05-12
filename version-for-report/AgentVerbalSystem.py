from z3 import sat, unsat

class AgentVerbalSystem:
    def __init__(self, reasoning_system):
        self.reasoning_system = reasoning_system

    def respond_to_question(self, question):
        if question[0] == "logic":
            return self.reasoning_system.check_statement(
                self.reasoning_system.build_z3_expr(question[1])
            )
        elif question[0] == "logic_brief":
            res = self.reasoning_system.check_statement(
                self.reasoning_system.build_z3_expr(question[1])
            )

            # print res

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
            res = self.reasoning_system.check_statement(
               self.reasoning_system.build_z3_expr(('for_some', question[1], question[2]))
            )

            if res['satisfiability'] == sat:
                model = res['model']
                names = [x[1] for x in question[1]]
                return { str(x): self.reasoning_system.verbalize(model[x]) for x in model.decls() if str(x) in names }

        else:
            return "I don't know how to answer that"

