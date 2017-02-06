# Consciousness

The aim here is to make programs illustrating key features of consciousness.

> My favorite path forward at the moment is a combination of Graziano's attention schema theory (AST), Sloman's suggests on qualia, Armstrong's "headless woman" illusion / Drescher's qualia-as-gensyms, and Kammerer's suggestion about "the hardest part" of the illusion problem. For brief comments on how these fit together, see the paragraph from my report which begins "Furthermore, I can think of ways to supplement…" (including its footnotes). The key sources are Webb & Graziano (2015) [and Graziano (2013) if that paper is too succinct]; Sloman & Chrisley (2003); Drescher (2006), ch. 2 only; Armstrong (1968); Kammerer (2016).
>
> Some other theories (of consciousness or of some component/aspect of consciousness) that could be helpful, either in combination with some stuff from the above paragraph or in combination with other ideas, include sensorimotor theory (O'Regan & Noe 2001; O'Regan 2012), narrative behavior theory (Markkula 2015), and AIR theory (Prinz 2012), among many others.
>
> For inspiration, you might want to study how Stan Franklin & colleagues "implemented" global workspace theory (GWS) in the cognitive architecture called LIDA. For a tutorial on LIDA, see Franklin et al. (2016). On the GWS part specifically, see Franklin et al. (2012). Other examples of computational models of consciousness (or components of consciousness) are described briefly in Reggia (2013): probably only worth reading from section 3.3 up to section 4.

Luke wrote:

> Furthermore, I can think of ways to supplement Graziano’s theory with additional details that explain some additional consciousness explananda beyond what Graziano’s theory (as currently stated) can explain. For example, Graziano doesn’t say much about the ineffability of qualia, but I think a generalization of Gary Drescher’s “qualia as gensyms” account, plus the qualia-related suggestions of Sloman & Chrisley (2003), explain that explanandum pretty well, and could be added to Graziano’s account. Graziano also doesn’t explain why we have the conviction that qualia cannot be “just” brain processes and nothing more, but intuitively it seems to me that an inference algorithm inspired by Armstrong (1968) might explain that conviction pretty well. But why do we find it so hard to even make sense of the hypothesis of illusionism about consciousness, even though we don’t have trouble understanding how other kinds of illusions could be illusions? Perhaps an algorithm inspired by Kammerer (2016) could instantiate this feature of human consciousness.

notes on those things:

### Sloman and Chrisley

The most relevant part of this seems to be the explanation of the privacy and ineffability of qualia on page 35; I think that's what Luke was referring to in his "Furthermore" paragraph.

> Now suppose that an agent A with a meta-management system, as in figure 7, uses a self-organising process to develop concepts for categorising its own internal virtual machine states as sensed by internal monitors. These will be architecture-driven concepts, but need not be architecture-based if the classifica- tion mechanism does not use an implicit or explicit theory of the architecture of the system it is monitoring, but merely develops a way of organising its ‘sensory’ input data. If such a concept C is applied by A to one of its internal states, then the only way C can have meaning for A is in relation to the set of concepts of which it is a member, which in turn derives only from the history of the self-organising process in A. These concepts have what Campbell (1994) refers to as ‘causal indexicality’.
>
> This means that if two agents A and B have each developed concepts in this way, then if A uses its concept Ca, to think the thought ‘I am having experience Ca’, and B uses its concept Cb, to think the thought ‘I am having experience Cb’ the two thoughts are intrinsically private and incommunicable, even if A and B actually have exactly the same architecture and have had identical histories lead- ing to the formation of structurally identical sets of concepts. A can wonder: ‘Does B have an experience described by a concept related to B as my concept Ca is related to me?’ But A cannot wonder ‘Does B have experiences of type Ca’, for it makes no sense for the concept Ca to be applied outside the context for which it was developed, namely one in which A’s internal sensors classify internal states. They cannot classify states of B.
> When different agents use architecture-driven concepts, produced by self organising classifiers, to classify internal states of a virtual machine, and are not even partly explicitly defined in relation to some underlying causes (e.g. external objects or a presumed architecture producing the sensed states), then there is nothing to give those concepts any user-independent content, in the way that our colour words have user-independent content because they refer to properties of physical objects in a common environment. Thus self-referential architecture- driven concepts used by different individuals are strictly non-comparable: not only can you not know whether your concepts are the same as mine, the question is *incoherent*. If we use the word ‘qualia’ to refer to the virtual machine states or entities to which these concepts are applied, then asking whether the qualia in two experiencers are the same would then would be analogous to asking whether two spatial locations in different frames of reference are the same, when the frames are moving relative to each other. But it is hard to convince some people that this makes no sense, because the question is grammatically well-formed. Sometimes real nonsense is not *obvious* nonsense.

### Kammerer

> The TIH states that the content of these theories includes, so to speak, the following statements:
>
> 1. Minds can take up information about states of affairs, and then can use > that information to form beliefs about them: states of affairs appear to minds.
> 2. The way minds do that is that they are affected in a certain way, they > have certain experiences.
> 3. The properties of experiences determine what appears to the mind, and a > state of affairs appears to the mind in virtue of these properties of > experiences. For example: an experience of a red circle is an affection of the > mind in virtue of which the presence of a red circle appears to the mind.
> 4. Take all the cases in which a certain state of affairs A appears > veridically to a subject S, and consider what all these cases have in common > regarding the way in which S is affected. What they have in common is a state  E, which is an experience of A.
> 5. Something is a part of E if and only if this thing is part of the way in which > S is affected in all the cases in which A appears veridically to a subject S.
>
> Appearances can be fallacious, and a mind can be deceived by the way states of affairs appear. And here is what happens in cases of fallacious appearances: when a subject S has a fallacious appearance of A, S is affected in exactly the same way as in cases of veridical appearances of A, except that A is not the case. That is to say, when a subject S has a fallacious appearance of A, it is in state E (E being, and being nothing but, what is common to the way S is affected in all the cases in which A appears veridically to her), but A is not the case.

### Armstrong

> What the example shows is that, in certain cases, it is very natural for human beings to pass from something that is true: 'I do not perceive that X is Y', to something that may be false: 'I perceive that X is not Y'

You can phrase this Bayesian-style. If seeing property Z in an X is highly correlated with it having property Y, then if you see an X without property Z, then it's reasonable to go from "I do not percieve that X is Y" to "I percieve X is not Y."

## Classes

Environment, which provides Observations to the Agent, which can then take Actions.

- Should this maybe just be using the OpenAI Gym environment?

What would be really cool things for the agent to be able to do/think?

- "When I start playing video games, I think about them a lot, and it's harder for me to decide to do other things"

## Luke's favored model

Webb and Graziano (2015):

> The hypothesized model of attention, or the attention schema (component A in Figure 1B), would not be a perfectly detailed model of the neuroscientific phenomenon of attention. It would not include anything about lateral inhibition, signal competition, or action potentials. The brain has no functional use for information about those physical details. Instead, the model would be more like a cartoon sketch that depicts the most important, and useful, aspects of attention, without representing any of the mechanistic details that make attention actually happen.
>
> Based on the information contained in this simplified model, brain B would conclude that it possesses a phenomenon with all of the most salient aspects of attention – the ability to take mental possession of an object, focus one’s resources on it, and, ultimately, act on it – but without any of the mechanisms that make this process physically possible. It would conclude that it possesses a magical, non-physical essence, but one which can nevertheless act and exert causal control over behavior, a mysterious conclusion indeed.

One fun note about "It would conclude that it possesses a magical, non-physical essence, but one which can nevertheless act and exert causal control over behavior, a mysterious conclusion indeed."-- Many humans have a similar intuition about their own bodies, cf.

The other things Luke likes:


## Notes

- Attention can affect layers of your sensory perception which are not consciously accessible. Eg, this is why you are better at percieving something when you're looking for it, perhaps?
- When you're thinking through something, seems kind of like MCMC search
- Choices I have to make:
    - How is information passed around?
        - vectors, a la neural nets
        - simple scalar strings
        - some kind of sum type of different kinds of information
        - graph of knowledge
            - This is a good way of expressing complicated ideas.
    - To what extent do I want my implementation to be motivated by a real problem?
        - this is nice to have, but probably not necessary immediately.
- What is awareness for?
    - you can note your own attention and then make predictions about your behavior
    - quotes:
        > if the brain lacks a clear internal model of the arm, such as in the case of anesthesia of the arm, then the control of the arm is still possible but is less effective

        > Another striking example was reported by Tsushima et al. (2006). Subjects performed a centrally presented letter discrimination task while a distracting dot motion stimulus was presented in the periphery. Performance on the letter task was actually better when the subjects were aware of the distracting motion, and performance was most impaired when the distracting motion was subthreshold and subjects were unaware of it.

        > In the theory, awareness is part of the control mechanism for attention. Without awareness, attention is still possible, but the brain in essence lacks knowledge about its state of attention and therefore cannot properly regulate that attention. If attention is directed at stimulus X in the absence of awareness of stimulus X, the brain has no internal knowledge that it is attending to X and therefore the control mechanism cannot easily withdraw that attention from X, or take that attention on X into account when adjusting attention to a different stimulus Y. As a result, the top–down control of attention to X, to Y, or to other stimuli is not as efficient. In that situation, stimulus X has a less well-controlled effect on behavior than it would otherwise.
    - I actually think Webb and Graziano pay insufficient attention to the point that there's a difference between needing to be able to control something and needing to have an accessible model of it. You can control some things without being able to read them.
        - One story: Maybe sometimes we need non-visual modules to control the bottom-up attentional processes in our visual systems.
            - Eg, in the experiment mentioned in Webb and Graziano where the subjects were being distracted by flickerings, when the subjects noticed the flickerings or were told about them, the flickerings were less harmful to the subjects' performance on the visual task
            - The two modules being used there are a learning module (if you noticed it yourself) or a verbal module (if you were informed about the flickerings)
        - Another story: It's much easier to control something if you're aware of it, if you can only change it by pushing on its value.
            - If this is why we need awareness, then without awareness, attention can still be controlled if you need strong absolute shifts, but it will be much clumsier for small shifts.
            - If you can just set the value absolutely instead of relatively, this matters less.
                - In some cases, my intuitions about attention say that it should be able to be set pretty absolutely. Eg I think of "ignore everything in this square" as an absolute instruction.
            - Also, there are some things which you can't set without having a model of them at all. Eg if you don't know which "lever" which you could "pull" corresponds to which part of your attention.
                - If you have ten employees, and you get to tell employees to change their task, then you need to know what your employees are doing in order to reprioritize.
            - Also being aware of its position lets you stabilize more easily
                - In the case of attention: because of bottom-up attention, you won't always be aware of how you should change it. Eg in the case where you are trying to avoid paying attention to the things at the peripheries, dampening it down.
        - A third story: There might be logic that can't be implemented within the attention system itself. Eg "If I'm paying close attention to the center of my visual field and it's a Friday, increase the attention to the color green". The attention system might not know whether it's Friday, so the verbal processing system needs to know when you're paying attention to the center of your visual field.
            - This requires that the logic has conditions about the attention

Maybe I want to represent knowledge as a graph. Nodes are strings and edges are labelled with words.

- Can you know things without knowing why, in this system?
    - Maybe your senses are hooked up to certain parts of your knowledge graph.
    - What's the distinction between things you know intuitively and things that you have to explicitly reason through?
        - Perhaps it's whether all the reasoning steps are in your graph or not. If you're memory limited, after you prove something you might forget the intermediate steps.

Alternatively I could represent knowledge as a numerical thing in some ways.

## The model

A bad but complete idea:

There is an agent in a car. The agent can drive around and look around. The agent can devote different amounts of mental energy to driving, thinking, and planning. The agent sometimes want to focus particular places in their line of sight. As well as a schema of the world around them, they have a schema of their own attention. They know how much attention they're paying to their sight vs hearing vs senses.

-------

Another:

There is an agent who has multiple subagents, each of whom gets to vote for actions. One of the subagents is stronger in the presence of the smell of chocolate. Our overall agent has a model of this ..asdfsddfas

Gah, that doesn't work because it needs to be able to *read* its attention, not just influence it. But why would you need to do that?

-----

You don't need to have an attention schema to plan, as long as you have a self-model. Eg, Deep Blue has a self-model.

-------

components:

- Long-term memory
- Schemas
    - body
    - outside world
    - attention
- Long-term planner
- Vision processing
    - You have access to the later layers of this neural net
        - Maybe you have access to early layers too, but you don't have access to the edge weights
- Motion planner
- Language module

You answer "What are you thinking about" by looking at your attention schema.

Your plans

## Random notes

- I could make a bunch of attentional experiments that you could do on the internet.






## New notes

The key question I still have is how to represent everything--vectors, trees of facts, graphs of facts, scalar strings?

### Represent everything as numbers?

If my attention is a vector in `R^6`, and my attention schema is a vector in `R^3`, does that count?

### Realistic, effectual schemas

Maybe I need to have a real planning module, so that it's clear what it means
for an agent to have a schema--schemas have a current state, which may have uncertainty, determined by observation; they also can predict how they'll change under various circumstances.

This has the advantage that you couldn't argue that my agents aren't 'really' representing things.

The simplest way to start this is probably having schemas that are so simple that the planning module can be extremely trivial or brute-force.

### Questions you can ask an agent:

- What color is the car?
- How salient is the color of the car, compared to its sound?
    - Translate that to "how much attention do you have on the color of the car?"
- What are you currently most aware of?
    - "The redness of the car"
    - What is the redness like?
        - "Closely related concepts include 'blueness' and 'greenness'"
    - What's different about redness and greenness?
        - "They are just different, I guess."

### Approximations made between the attention and attention schema

Maybe the attention schema just knows the single most salient thing, even though attention is actually spread across many things.

### Hard coded planning module?

The planning module can just be a series of if statements if I want.

- This means the agent can't instrospect on its own rules. If I instead reified its decision procedure, it would not have that problem.

## Example agent

Modules:

- Visual processing
    - recieves input. Has bottom-up attentional processes. Also it has some attentional settings which can be controlled from outside itself.
    - Its output is the result of its processing, plus some info about its attention
- Other inputs: pain, hunger
- Model. Has subcomponents
    - World schema. This is updated to the maximum likelihood world given the result of its visual processing.
    - Self schema. This is a simplified version of hunger. This means that it can for example experience hunger when the cause is more like boredom. This leads to irrational behavior like eating to fix the hunger when that won't help.
    - Attentional schema. This is a model of your visual attention and your model's attention and your planning attention.


## Desiderata

- Being totally functional
- Readibility
- it would be nice if the mind in question seemed like a natural design to solve the problem it's trying to solve.

