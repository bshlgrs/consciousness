class Agent:
    def __init__(self):
        self.vision_system = VisionSystem()
        self.model = Model()
        self.planning_system = PlanningSystem()

        self.model.attach_visual_system(self.vision_system)

        self.planning_system.attach_vision_system(self.vision_system)
        self.planning_system.attach_model(self.model)

    def step(self, visual_input):
        self.vision_system.handle_input(visual_input)

        self.model.update()

        self.planning_system.get_action()

class Model:
    def __init___(self):
        self.attention_schema = {}
        self.world_schema = {}
        self.self_schema = {}

    def update(self):
        pass

