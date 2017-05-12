from z3 import *
from AgentReasoningSystem import AgentReasoningSystem
from AgentVerbalSystem import AgentVerbalSystem


class Agent:
    def __init__(self):
        self.color_memory = []
        self.current_color = None
        self.reasoning_system = AgentReasoningSystem(self)
        self.verbal_system = AgentVerbalSystem(self.reasoning_system)

        self.reasoning_system.add_lemmas()

    def show_color(self, color):
        self.color_memory.append(color)
        self.current_color = color

    def sense_axioms(self):
        memory = self.reasoning_system.concepts["memory"]
        myself = self.reasoning_system.concepts["myself"]
        current_quale = self.reasoning_system.concepts["current_quale"]
        ColorQuale = self.reasoning_system.concepts["color_quale"]
        qualia = [Const("q" + str(time), ColorQuale) for (time, x) in enumerate(self.color_memory)]

        current_color_axioms = [memory(myself, time) - current_quale(myself) == x - self.current_color
                  for (time, x) in enumerate(self.color_memory)]

        memory_axioms = [memory(myself, x_time) - memory(myself, y_time) == x - y
                for (x_time, x) in enumerate(self.color_memory)
                for (y_time, y) in enumerate(self.color_memory)
                if x_time < y_time]

        return (current_color_axioms + memory_axioms)


    def respond_to_question(self, question):
        return self.verbal_system.respond_to_question(question)
