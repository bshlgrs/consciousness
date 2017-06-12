## The strength of the consciousness illusion

Our agent’s understanding of conscious experience can be expanded to incorporate  Kammerer’s Theoretical Introspection Hypothesis.

Kammerer observes  that we have unique difficulty in making sense of the hypothesis of illusionism. When faced with traditional illusions like the Müller-Lyer illusion, we have no trouble accepting the claim that under some circumstances what we perceive is illusory. But it’s very hard to make sense of the claim that our experiences are illusory. He writes:

> This contrast shows that the intuitive resistance to illusionism regarding consciousness is pretty unique, and cannot simply be explained by the persistence of a very strong perceptual-like, cognitively impenetrable disposition to believe that we are conscious. The illusion of phenomenality is particularly powerful; it is much more powerful than other ‘classical’ perceptual illusions, and it is powerful in a very distinctive way.

He proposes tackling this problem by coming up with an explicit theory of what things humans consider to be illusory. He proposes his own theory of this type, which he calls the Theoretical Introspection Hypothesis (TIH):

> The TIH states that the content of these theories includes, so to speak, the following statements:
>
> 1. Minds can take up information about states of affairs, and then can use that information to form beliefs about them: states of affairs appear to minds.
> 2. The way minds do that is that they are affected in a certain way, they have certain experiences.
> 3. The properties of experiences determine what appears to the mind, and a state of affairs appears to the mind in virtue of these properties of experiences. For example: an experience of a red circle is an affection of the mind in virtue of which the presence of a red circle appears to the mind.
> 4. Take all the cases in which a certain state of affairs A appears veridically to a subject S, and consider what all these cases have in common regarding the way in which S is affected. What they have in common is a state E, which is an experience of A. Something is a part of E if and only if this thing is part of the way in which S is affected in all the cases in which A appears veridically to a subject.
> 5. Appearances can be fallacious, and a mind can be deceived by the way states of affairs appear. And here is what happens in cases of fallacious appearances: when a subject S has a fallacious appearance of A, S is affected in exactly the same way as in cases of veridical appearances of A, except that A is not the case. That is to say, when a subject S has a fallacious appearance of A, it is in state E (E being, and being nothing but, what is common to the way S is affected in all the cases in which A appears veridically to her), but A is not the case.

We implement the five claims of the TIH  as beliefs in our agent’s reasoning system. This allows the agent to respond to questions like “Is it conceivable that an agent might have an illusion of having a red object in front of them?” with “yes”:

> (for-some (Agent a) (could-have-illusion-of agent (seeing-color red)))

But the agent concludes that it is not conceivable for an agent to have an illusion that it’s having a particular experience. If instead of asking it about an agent having an illusion of having a red object in front of it, we ask about having an illusion of having the experience of red, it says that is impossible. The agent answers this question negatively:

> (for-some (Agent a) (could-have-illusion-of agent (experience-of (seeing-color red))))

In our code, the statements of the TIH hypothesis are implemented as logical claims in the agent’s reasoning module. (They’re in the `kammerer_axioms` method in `ReasoningModule.py` if you want to read them.)

Our agent answers questions about logical possibilities by making calls to the Z3 theorem prover. Z3 is a library which does logical inference--given a set of axioms, it can tell you if another logical expression is entailed by them or not. It uses first order logic. Appendix A contains more information about how these beliefs were translated into first order logic.

## Appendix A: implementation of Theoretical Introspection Hypothesis

The following is how I translated the TIH into first order logic.

- Every state that the world could be in is described by a WorldState. In the environment in which this agent operates, the world has a hue and some number of agents in it who are having color experiences.
- WorldStates consist of many WorldFacts. WorldFacts correspond to Kammerer's concept of a "state of affairs".
- WorldFacts are either facts about what hue the world is (WorldColorFacts) or what hue an Agent is experiencing (ExperienceFacts).
- WorldFacts are "consistent" iff it is conceivable that both are true in the same world state. A more specific definition is: WorldFacts are consistent unless they're both WorldColorFacts and they disagree on what color the world is, or if they're both ExperienceFacts about the same agent and they disagree with color the agent is experiencing.
- Agents might have an experience of a particular WorldFact. This is what Kammerer describes as the state which is "part of the way in which [the subject] S is affected in all the cases in which [the state of affairs] A appears veridically to a subject".
  - Agents don't have an experience associated with every world fact. For example, the agent X has no experience of the fact "agent Y is experiencing red".
  - So in fact, an agent A has an experience of a WorldFact WF if:
    - WF is a WorldColorFact, in which case the experience is the experience of A seeing that color, or
    - WF is the ExperienceFact which describes A having an experience E, in which case the experience of this fact is E.
  - This is described in the code by having a function experience_of from an Agent and WorldFact to either a Quale or nothing.
- In the world state WS, agent A has an illusion of a WorldFact WF if both of the following are true:
  - The fact WF is not actually present in WS. (Gettier-style situations aside, you're not having an illusion of something if it's really there.)
  - If experience_of(A, WF) is a quale Q, then WS contains the ExperienceFact corresponding to A experiencing Q.
    - This means that for Jeff to be having an illusion of the world being red, Jeff must be experiencing red.

The result of this is that the agent thinks that it's conceivable that one might have an illusion of the world being a particular color, and it's conceivable that one might have an illusion of *someone else* seeing a particular color, but it's not logically possible for an agent to have an illusion that it is having an experience. This is a desirable feature of our model because the intuition ‘what you are experiencing is not the sort of thing that can be illusory’ is what this set of axioms tries to capture’.
