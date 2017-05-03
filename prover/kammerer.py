from z3 import *
from z3_helper import Z3Helper

s = Solver()

myForAll = Z3Helper.myforall
myExists = Z3Helper.myexists

axioms = []

Quale = DeclareSort('Quale')
Color = DeclareSort('Color')
Agent = DeclareSort('Agent')
current_quale = Function('current_quale', Agent, Quale)

WorldFact = DeclareSort('WorldFact')
WorldState = DeclareSort('WorldState')

vision = Function('vision', Agent, Color, Quale)
state_contains_fact = Function('state_contains_fact', WorldState, WorldFact, BoolSort())

is_ExperienceFact = Function('is_ExperienceFact', WorldFact, BoolSort())
make_ExperienceFact = Function('make_ExperienceFact', Agent, Quale, WorldFact)
is_WorldColorFact = Function('is_WorldColorFact', WorldFact, BoolSort())
make_WorldColorFact = Function('make_WorldColorFact', Color, WorldFact)


is_experience_of = Function('is_experience_of', Quale, Agent, WorldFact, BoolSort())
axioms.append(myForAll([Quale, Agent, WorldFact], lambda q, a, wf:
      And(
          myForAll([Color], lambda c:
                 Implies(make_WorldColorFact(c) == wf,
                         is_experience_of(q, a, wf) == (vision(a, c) == q))
                ),
          myForAll([Agent, Quale], lambda a2, q2: Implies(make_ExperienceFact(a2, q2) == wf,
                         is_experience_of(q, a, wf) == (a == a2 and q == q2)))
      )
))



axioms.append(myForAll([WorldFact], lambda wf: is_ExperienceFact(wf) != is_WorldColorFact(wf)))

axioms.append(myForAll([WorldFact], lambda wf:
                       myExists([Agent, Quale], lambda a, q: make_ExperienceFact(a, q) == wf)
                            ==  is_ExperienceFact(wf)
                      )
             )

axioms.append(myForAll([WorldFact],
                       lambda wf: myExists([Color], lambda c: make_WorldColorFact(c) == wf) == is_WorldColorFact(wf)
             ))




axioms.append(myForAll([WorldState, WorldFact, WorldFact], lambda ws, wf1, wf2:
  Implies(And(state_contains_fact(ws, wf1), state_contains_fact(ws, wf2)),
    And(

#                 # Facts are inconsistent if they are both about the world color, and they are different colors
      myForAll([Color, Color], lambda c1, c2:
                       Implies(And(wf1 == make_WorldColorFact(c1), wf2 == make_WorldColorFact(c2)),
                          c1 == c2
                  )
      )
    )
  )
))






fact_consistent_with_world = Function('fact_consistent_with_world', WorldFact, WorldState, BoolSort())
# axioms.append(myForAll([WorldFact, WorldState], lambda wf, ws:
#                       fact_consistent_with_world(wf, ws) == myForAll([WorldFact], lambda wf2:
#                             Implies(state_contains_fact(ws, wf2), consistent_facts(wf, wf2))
#                     )))

axioms.append(myForAll([WorldFact, WorldState], lambda wf, ws:
  fact_consistent_with_world(wf, ws) == myExists([WorldState], lambda ws2:
    And(state_contains_fact(ws2, wf),
      myForAll([WorldFact],
        lambda wf2: Implies(state_contains_fact(ws, wf2), state_contains_fact(ws2, wf2)))
  ))
  )
)



has_illusion = Function('has_illusion', Agent, WorldState, WorldFact, BoolSort())

axioms.append(
    myForAll([Agent, WorldState, WorldFact], lambda a, ws, wf:
                has_illusion(a, ws, wf) == And(
                    fact_consistent_with_world(wf, ws),
                    Not(state_contains_fact(ws, wf)),
                    myForAll([Quale], lambda q: Implies(is_experience_of(q, a, wf), current_quale(a) == q))
                )
    )
)



buck = Const('buck', Agent)
red = Const('red', Color)
world_is_red_fact = make_WorldColorFact(red)
buck_is_seeing_red_fact = make_ExperienceFact(buck, vision(buck, red))
illusion_world_state = Const('illusion_world_state', WorldState)

axioms.append(has_illusion(buck, illusion_world_state, world_is_red_fact))


s.add(axioms)


print "OH I AM ABOUT TO CHECK"

# print s.to_smt2()

print s.check()
print s.model()
# print s.reason_unknown()
