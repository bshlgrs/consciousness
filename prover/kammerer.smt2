; benchmark generated from python API
(set-info :status unknown)
(declare-sort Agent)
(declare-sort WorldFact)
(declare-sort Quale)
(declare-sort Color)
(declare-sort WorldState)
(declare-fun make_ExperienceFact (Agent Quale) WorldFact)
(declare-fun vision (Agent Color) Quale)
(declare-fun make_WorldColorFact (Color) WorldFact)
(declare-fun current_quale (Agent) Quale)
(declare-fun red () Color)
(declare-fun buck () Agent)
(declare-fun illusion_world_state () WorldState)
(declare-fun is_experience_of (Quale Agent WorldFact) Bool)
(declare-fun is_WorldColorFact (WorldFact) Bool)
(declare-fun is_ExperienceFact (WorldFact) Bool)
(declare-fun state_contains_fact (WorldState WorldFact) Bool)
(declare-fun fact_consistent_with_world (WorldFact WorldState) Bool)
(declare-fun has_illusion (Agent WorldState WorldFact) Bool)
(assert
 (forall ((q Quale) (a Agent) (wf WorldFact) )(let (($x38 (forall ((a2 Agent) (q2 Quale) )(=> (= (make_ExperienceFact a2 q2) wf) (= (is_experience_of q a wf) (= a a2))))
 ))
 (let (($x48 (forall ((c Color) )(=> (= (make_WorldColorFact c) wf) (= (is_experience_of q a wf) (= (vision a c) q))))
 ))
 (and $x48 $x38))))
 )
(assert
 (forall ((wf WorldFact) )(and (distinct (is_ExperienceFact wf) (is_WorldColorFact wf)) true))
 )
(assert
 (forall ((wf WorldFact) )(let (($x23 (exists ((a Agent) (q Quale) )(= (make_ExperienceFact a q) wf))
 ))
 (= $x23 (is_ExperienceFact wf))))
 )
(assert
 (forall ((wf WorldFact) )(let (($x8 (exists ((c Color) )(= (make_WorldColorFact c) wf))
 ))
 (= $x8 (is_WorldColorFact wf))))
 )
(assert
 (forall ((ws WorldState) (wf1 WorldFact) (wf2 WorldFact) )(let (($x53 (forall ((c1 Color) (c2 Color) )(let (($x57 (and (= wf1 (make_WorldColorFact c1)) (= wf2 (make_WorldColorFact c2)))))
 (=> $x57 (= c1 c2))))
 ))
 (=> (and (state_contains_fact ws wf1) (state_contains_fact ws wf2)) (and $x53))))
 )
(assert
 (forall ((wf WorldFact) (ws WorldState) )(let (($x11 (exists ((ws2 WorldState) )(let (($x65 (forall ((wf2 WorldFact) )(=> (state_contains_fact ws wf2) (state_contains_fact ws2 wf2)))
 ))
 (and (state_contains_fact ws2 wf) $x65)))
 ))
 (= (fact_consistent_with_world wf ws) $x11)))
 )
(assert
 (forall ((a Agent) (ws WorldState) (wf WorldFact) )(let (($x89 (forall ((q Quale) )(=> (is_experience_of q a wf) (= (current_quale a) q)))
 ))
 (let (($x92 (and (fact_consistent_with_world wf ws) (not (state_contains_fact ws wf)) $x89)))
 (= (has_illusion a ws wf) $x92))))
 )
(assert
 (has_illusion buck illusion_world_state (make_ExperienceFact buck (vision buck red))))
(check-sat)
