import z3

class EzZ3:
    def __init__(self):
        self.axioms = []
        self.sorts = {}

    def declare_sort_alias(self, name, sort):
        pass





# def program(ez):
#     ColorQualia = ez.declare_sort_alias("ColorQualia", ez.BitVector(4))
#     Color = ez.declare_sort_alias("Color", ez.BitVector(4))

#     Agent = ez.declare_sort("Agent", {
#         memory: ez.ListType(ColorQualia),
#         current_quale: ColorQualia,
#         vision: ex.FunctionType([Color], ColorQualia)
#     })

#     ez.declare_sort("StateOfAffairs", {
#         color: ColorFact,
#         # agentExperiences: ez.MapType(Agent, ColorQualia)
#         agentExperiences: ez.MapType(Agent, ColorQualia)
#     })

#     ez.declare_function("experienceOfSeeingColor",
#         [("a", Agent), ("c", Color)], ColorQualia
#     )

#     WorldFact = ez.declare_closed_sort("WorldFact")
#     ColorFact = WorldFact.subsort("ColorFact", {
#         color: Color
#     })
#     AgentExperienceFact = WorldFact.subsort("AgentExperienceFact", {
#         agent: Agent, colorQualia: ColorQualia
#     })

#     StateOfAffairs.declare_method("agentExperienceFacts", [], AgentExperienceFact,
#         lambda self: self.agentExperiences.asTuples.map(lambda a, cq: AgentExperienceFact(a, cq))
#     )


