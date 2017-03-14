from queue import PriorityQueue


class VisionSystem(object):
    pass


class Model(object):
    def __init__(self):
        self.vision_system = None

    def attach_vision_system(self, vision_system):
        self.vision_system = vision_system

    # `world` is something like [{"type": "ball", "position": "left", "color": "red"}]
    def predict_visual_experience(self, world):



class VerbalSystem(object):
    def __init__(self):
        self.vision_system = None
        self.model = None

    def attach_vision_system(self, vision_system):
        self.vision_system = vision_system

    def attach_model(self, model):
        self.model = model

class Simulation():
    @staticmethod
    def simulate(events, agent):
        queue = PriorityQueue()

        total_time = 0
        for (time, event) in events:
            queue.put((total_time, "visual_experience_changes", event))
            total_time += time

        while not queue.empty():
            (time, type, details) = queue.get()

            print(time, type, details)




class Agent():
    def __init__(self):
        self.current_instructions = {}

        self.vision_system = VisionSystem()
        self.model = Model()
        self.verbal_system = VerbalSystem()

        self.model.attach_vision_system(self.vision_system)

        self.verbal_system.attach_vision_system(self.vision_system)
        self.verbal_system.attach_model(self.model)

    def instruct(self, instruction, value):
        self.current_instructions[instruction] = value


agent = Agent()

# Tell the agent to fixate on the center of its visual field
agent.instruct("fixate", "center")


class PhysicalObject(object):
    pass

class Lightbulb(PhysicalObject):
    def __init__(self, luminence):
        self.luminence = luminence


class Ball(PhysicalObject):
    def __init__(self, color):
        self.color = color



agent.simulate_visual_experiences([200, { 'left': Lightbulb(0.1), 'right': Ball("red") }])

# Tell it that something is going to appear on the right.
# It should aim its covert attention at the right, with intended intensity of attention 80%,
# with a halflife of 2 seconds.
# agent.tell("covert-attend", 'right', 0.8, 2)

print(agent.ask(["ball", "color"])) # => 'red'
print(agent.ask(["things-seen"]).map("type")) # => ['ball']
print(agent.ask(["attention"])) # => { "center": 0.5, "left": 0.3, "right": 0.2 }
print(agent.ask(["most-recent-visual-experience"]))
# => [{ 'type': 'ball-experience', 'color': 'red', position: 'right'}]
print(agent.ask(["model-MAP"])) # => [{right: [{ 'type': 'ball', 'color': 'red'}]}]

# Okay, that all demonstrates that it has an idea of what its own attention is.

# Now it needs to know about what illusions are.

# This is calculated by figuring out whether the world normally causes a different visual experience.
agent.ask_about_hypothetical({
    'world': [{"type": "ball", "position": "left", "color": "red"}],
    'visual-experience': [{"type": "ball", "position": "left", "color": "green"}]
}, "illusory") # true