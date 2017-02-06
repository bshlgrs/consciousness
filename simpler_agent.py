class SimpleAttentionSchemaAgent:
  def __init__(self):
    self.visual_system = VisualSystem()
    self.model = Model()
    self.planner = Planner()

  def think(self, visual_input):
    """
    This method contains all the details of how information flows between
    different components of the agent. Details of how information is
    processed inside each component of the agent are specified in the
    classes for each component.
    """
    # Process world
    self.visual_system.process_visual_input(visual_input)

    # Update world schema with visual information from the visual system.
    self.model.world_schema.update_with_visual_info(self.visual_system.visual_info())

    # Update attention schema with the information about visual attention
    # that the visual system can provide
    self.model.attention_schema.update_with_visual_attention_info(
      self.visual_system.visual_attention_info())

    # Plan action. The planner uses the information available to it from
    # the visual system directly and from its world schema and attention schema.
    self.plan = self.planner.plan({
      "world_schema": self.model.world_schema.planner_info(),
      "attention_schema": self.model.attention_schema.planner_info()
    })

    # Update our model of what our planner was mostly thinking about
    self.model.attention_schema.update_with_planner_attention_info(
      self.planner.planner_attention_schema_info)

    # The planning system gets to control the attention of the visual
    # system (top-down attention)
    self.visual_system.control_attention(self.plan.new_visual_attention)

    return self.plan.action
