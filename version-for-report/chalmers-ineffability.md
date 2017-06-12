In Chalmer’s paper “Consciousness and Cognition”, he argues that ineffability follows inevitably from how information acquired by our senses is represented to the parts of the brain responsible for conscious processing:

> The key point is that once the information flow has reached the central processing portions for the brain, further brain function is not sensitive to the original raw data, but only to the pattern (to the information!) which is embodied in the neural structure.
>
> Consider color perception, for instance. Originally, a spectral envelope of light-wavelengths impinges upon our eyes. Immediately, some distinctions are collapsed, and some pattern is processed. Three different kinds of cones abstract out information about how much light is present in various overlapping wavelength-ranges. This information travels down the optic nerve (as a physical pattern, of course), where it gets further transformed by neural processing into an abstraction about how much intensity is present on what we call the red-green, yellow-blue, and achromatic scales. What happens after this is poorly-understood, but there is no doubt that by the time the central processing region is reached, the pattern is very much transformed, and the information that remains is only an abstraction of certain aspects of the original data.
>
> Anyway, here is why color perception seems strange. In terms of further processing, we are sensitive not to the original data, not even directly to the physical structure of the neural system, but only to the patterns which the system embodies, to the information it contains. It is a matter of access. When our linguistic system (to be homuncular about things) wants to make verbal reports, it cannot get access to the original data; it does not even have direct access to neural structure. It is sensitive only to pattern. Thus, we know that we can make distinctions between certain wavelength distributions, but we do not know how we do it. We've lost access to the original wavelengths - we certainly cannot say "yes, that patch is saturated with 500- 600 nm reflections". And we do not have access to our neural structure, so we cannot say "yes, that's a 50 Hz spiking frequency". It is a distinction that we are able to make, but only on the basis of pattern. We can merely say "Yes, that looks different from that." When asked "How are they different?", all we can say is "Well, that one's red, and that one's green". We have access to nothing more - we can simply make raw distinctions based on pattern - and it seems very strange.
>
> So this is why conscious experience seems strange. We are able to make distinctions, but we have direct access neither to the sources of those distinctions, or to how we make the distinctions. The distinctions are based purely on the information that is processed. Incidentally, it seems that the more abstract the information-processing - that is, the more that distinctions are collapsed, and information recoded - the stranger the conscious experience seems. Shape- perception, for instance, strikes us as relatively non-strange; the visual system is extremely good at preserving shape information through its neural pathways. Color and taste are strange indeed, and the processing of both seems to involve a considerable amount of recoding.

In Chalmers’ account, then, ineffability is about information loss, and about the invisibility-to-us of the compression mechanism; the more information loss and the less transparent the mechanism, the more we will experience the phenomenon as ineffable. We can design an agent whose sensory experience has these attributes (information loss and a lack of transparency).

Our program implements a simulation of an agent which is connected to a text interface and a single-pixel camera which only measures hue. The agent gets information from its camera and can answer questions that it is asked over the text interface.

When it sees a hue, the agent’s visual processing system represents this as a number according to its hue. This number stands in for the pattern of neuron firings which we identify with our experience of the color.

This number is also saved to the agent's memory. This is analogous to the claim that in our brain, memories are represented in terms of neuron firing patterns.

We can ask the agent questions over its text interface. Like humans, it can answer questions about the experience’s relationship to other things; also like humans, it can’t answer questions about the experience itself. For example, our agent can tell you that it’s already seen the color it’s currently seeing.

We ask questions of the agent by typing in a syntax similar to the programming language Lisp:

    (there-exists (int i) (== (visual-memory-at-time i) current-visual-experience))

A relatively literal reading of the phrasing of this question would be “Does there exist an integer `i` such that your visual memory at time `i` is the same as your current visual experience?"
But the agent has no way to talk about the actual content of its color experience at any time. Chalmers wrote that this is because we are able to distinguish patterns, but don’t have access to the mechanism by which we determined that these patterns are different. This, he says, is why we have the impression that our experiences are primitive values that we can’t further introspect on. In this model, the limitation our program experiences -- that nothing can be communicated directly about the content of its experience -- is the same limitation humans experience when they struggle to describe what looking at ‘red’ is like.

In the AgentReasoningModule, we declare a number of axioms that the agent uses to generate answers to questions. Some of these axioms are about how vision works. One axiom is that the agent will, when presented with a color, produce an associated color quale which is unique for each color. However, it is never given access to the actual number representing that quale. It’s just given access to the results of comparing the quale of different situations.

With these axioms the agent can arrive at conclusions like “I am seeing a color right now that I’ve seen before”, and even “Orange is closer to red than blue is”, but it can’t answer any questions about the actual value of the quale. In Chalmer’s account, this belief that it knows how to reason about the value of its experience without being able to introspect on any objective facts about the experience is what leads to human-like intuitions about ineffability.

—

We refine Chalmers’ account slightly; our agent does not believe that the mapping between colors and experiences is necessarily the same for every human—it just believes that all humans experience differences between colors the same way.

This is done by giving the agent the belief that vision involves a function from both an Agent and a color to a color quale. This allows the experience of a particular color to differ between agents. It follows that it’s possible that some other agent has swapped perceptions of red and green compared to it. So this agent has the intuition that inverted spectra are logically possible.
