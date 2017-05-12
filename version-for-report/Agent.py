from z3 import *
from AgentReasoningModule import AgentReasoningModule


class Agent:
    def __init__(self):
        self.color_memory = []
        self.current_color = None
        self.reasoning_system = AgentReasoningModule(self)

    def show_color(self, color):
        self.color_memory.append(color)
        self.current_color = color

    def memory_axioms(self):
        memory = self.reasoning_system.concepts["memory"]
        myself = self.reasoning_system.concepts["myself"]
        ColorQuale = self.reasoning_system.concepts["color_quale"]
        qualia = [Const("q" + str(time), ColorQuale) for (time, x) in enumerate(self.color_memory)]

        return (#[memory(myself, time, quale) for (time, quale) in enumerate(qualia)] +
            [qualia[x_time] - qualia[y_time] == x - y
                for (x_time, x) in enumerate(self.color_memory)
                for (y_time, y) in enumerate(self.color_memory)
                if x_time < y_time])

    def current_color_axioms(self):
        current_quale = self.reasoning_system.concepts['current_quale']
        myself = self.reasoning_system.concepts["myself"]

    def ask_question(self, question):
        if question[0] == "logic":
            return self.reasoning_system.check_statement(
                self.reasoning_system.build_z3_expr(question[1])
            )
        elif question[0] == "logic_brief":
            res = self.reasoning_system.check_statement(
                self.reasoning_system.build_z3_expr(question[1])
            )

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

