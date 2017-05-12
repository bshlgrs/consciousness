from z3 import *
from z3_helper import Z3Helper

myForAll = Z3Helper.myforall
myExists = Z3Helper.myexists

axioms = []

ColorQuale = DeclareSort('ColorQuale')
Color = DeclareSort('Color')
Human = DeclareSort('Human')
current_quale = Function('current_quale', Human, ColorQuale)
vision = Function('vision', Human, Color, ColorQuale)

MaybeColorQuale = Z3Helper.build_maybe_sort(ColorQuale)

WorldFact = Datatype('WorldFact')
WorldFact.declare('ExperienceFact', ('wf_human', Human), ('wf_quale', ColorQuale))
WorldFact.declare('WorldColorFact', ('wf_color', Color))
WorldFact = WorldFact.create()
ExperienceFact = WorldFact.ExperienceFact
WorldColorFact = WorldFact.WorldColorFact
wf_human = WorldFact.wf_human
wf_quale = WorldFact.wf_quale
wf_color = WorldFact.wf_color
is_ExperienceFact = WorldFact.is_ExperienceFact
is_WorldColorFact = WorldFact.is_WorldColorFact

WorldState = DeclareSort('WorldState')

consistent_facts = Function('consistent_facts', WorldFact, WorldFact, BoolSort())
axioms.append(myForAll([WorldFact, WorldFact], lambda wf1, wf2:
  consistent_facts(wf1, wf2) ==
    If(is_ExperienceFact(wf1) != is_ExperienceFact(wf2),
      True,
      If(is_ExperienceFact(wf1),
        Or(wf_quale(wf1) == wf_quale(wf2), wf_human(wf1) != wf_human(wf2)),
        wf1 == wf2
      )
    )
))

state_contains_fact = Function('state_contains_fact', WorldState, WorldFact, BoolSort())

# defining consistency
axioms.append(myForAll([WorldState, WorldFact, WorldFact], lambda ws, wf1, wf2:
  Implies(And(state_contains_fact(ws, wf1), state_contains_fact(ws, wf2)),
    consistent_facts(wf1, wf2)
  )
))

# define experience_of
experience_of = Function('experience_of', Human, WorldFact, MaybeColorQuale)
axioms.append(myForAll([Human, WorldFact], lambda a, wf:
  experience_of(a, wf) ==
    If(is_WorldColorFact(wf),
      MaybeColorQuale.Just(vision(a, wf_color(wf))),
      If(wf_human(wf) == a, MaybeColorQuale.Just(wf_quale(wf)), MaybeColorQuale.Nothing)
  ))
)

fact_consistent_with_world = Function('fact_consistent_with_world', WorldFact, WorldState, BoolSort())
axioms.append(myForAll([WorldState, WorldFact, WorldFact], lambda ws, wf1, wf2:
  Implies(
    And(fact_consistent_with_world(wf1, ws), state_contains_fact(ws, wf2)),
    consistent_facts(wf1, wf2)
  )
))

has_illusion = Function('has_illusion', Human, WorldState, WorldFact, BoolSort())
axioms.append(
  myForAll([Human, WorldState, WorldFact], lambda a, ws, wf:
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

buck = Const('buck', Human)
luke = Const('luke', Human)
red = Const('red', Color)
green = Const('green', Color)
axioms.append(red != green)
buck_red_quale = Const('buck_red_quale', ColorQuale)
axioms.append(vision(buck, red) == buck_red_quale)
world_is_red_fact = WorldColorFact(red)
buck_is_seeing_red_fact = ExperienceFact(buck, buck_red_quale)
illusion_world_state = Const('illusion_world_state', WorldState)

def consider(axioms, axiom):
  s = Solver()
  s.push()
  s.add(axioms)
  s.add(axiom)

  # print s.to_smt2()
  try:
    print s.check()
    # print s.model()
    # print s.reason_unknown()
  except Exception as e:
    print e


print "trying buck / world is red"
consider(axioms, has_illusion(buck, illusion_world_state, world_is_red_fact))

print "trying buck / buck is seeing red"
consider(axioms, has_illusion(buck, illusion_world_state, buck_is_seeing_red_fact))

print "trying luke / buck is seeing red"
consider(axioms, has_illusion(luke, illusion_world_state, buck_is_seeing_red_fact))
