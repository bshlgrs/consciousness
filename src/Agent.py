from z3 import *
from AgentReasoningSystem import AgentReasoningSystem
from AgentVerbalSystem import AgentVerbalSystem
from Z3Helper import Z3Helper


class Agent:
    """
    This class represents the simulated agent.
    """
    def __init__(self):
        # This is an array containing hues which the agent has seen.
        self.color_memory = []

        # This is the current color the agent is seeing.
        self.current_color = None

        self.reasoning_system = AgentReasoningSystem(self)
        self.verbal_system = AgentVerbalSystem(self.reasoning_system)

    # Public method to show a color to the agent.
    def show_color(self, color):
        self.color_memory.append(color)
        self.current_color = color

    # Public method to show a color to the agent.
    def ask_question(self, question):
        return self.verbal_system.respond_to_question(question)

    def _sense_axioms(self):
        memory = self.reasoning_system.concepts["memory"]
        myself = self.reasoning_system.concepts["myself"]
        current_quale = self.reasoning_system.concepts["current_quale"]
        ColorQuale = self.reasoning_system.concepts["color_quale"]
        qualia = [Const("q" + str(time), ColorQuale) for (time, x) in enumerate(self.color_memory)]

        current_color_axioms = [memory(myself, time) - current_quale(myself) == x - self.current_color
                  for (time, x) in enumerate(self.color_memory)]

        memory_axioms = [
            Z3Helper.abs(memory(myself, x_time) - memory(myself, y_time)) == abs(x - y)
                for (x_time, x) in enumerate(self.color_memory)
                for (y_time, y) in enumerate(self.color_memory)
                if x_time < y_time]

        return (current_color_axioms + memory_axioms)
