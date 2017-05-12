# A computer program to illustrate an illusionist theory of consciousness

## Introduction

I wrote a program which implements the core features of several illusionist theories of consciousness. In this report, I'll explain how the program works and what it does.

## Background

In the course of writing his “Report on Consciousness and Moral Patienthood”, Luke ran across a variety of theories of consciousness and says that he wishes that these moral theories “went further”

link to #MoreSatisfying in the report

He also lamented that it’s really hard to tell exactly what someone means by their theories of consciousness—we have a tendency to write things like "And yet, I don’t think this version of the Hero object is conscious, and I’d guess that Braithwaite would agree. But if this isn’t what Braithwaite means by “nociception,” “mental representations,” and so on, then what does she mean? What program would satisfy one or more of her indicators of consciousness?"

link to #Hero in the report


### What's our claimed connection between this program and real consciousness?

Mostly just the links *between* components, rather than the components themselves.

This program isn't trying to illustrate a hypothesis like "human intuitions about consciousness are actually implemented with a first-order logic theorem prover".

It's trying to add precision and clarity to a claim like "If an agent knew that its verbal system did not have access to its internal representation of color, but it did have access to some representation of the difference between different colors, then it would get the impression that it's meaningful to ask about whether other agents have inverted spectra, and also the answer is yes."


## Theories of consciousness implemented

- Something like Drescher's gensyms.
  - I'm listing this first because it has a strong case that our expression of it is useful.
- Kammerer's Theoretical Introspection Hypothesis

## What it can do

```
Q: Suppose there are two humans Bob and Jane, do they have the same qualia associated with every color?
Both that statement and its negation are possible.

Q: For all y, does there exist an x such that x = y + 1?
Yes.

Q: For all two humans, do they see colors the same? Should be 'idk'
No.

Q: Are your memories at timestep 1 and 2 of the same color?
No.

Q: Are you seeing the same color now as you saw at timestep 1?
No.

Q: Is it possible for an agent to have an illusion of red?
Yes.

Q: Is it possible for you to have the illusion that Buck is experiencing a color?
Yes.

Q: Is it possible for Buck to have an illusion that he is having the experience of redness?
No, that's impossible.
```


## How it works

The program is written in Python 2. It uses the theorem prover Z3.

It has the following classes:

- Agent
- AgentVerbalSystem
- AgentReasoningSystem

When it sees a color, here's what happens: We call the `show_color` method of Agent. This sets the agent's `current_color` field to the color. It also adds this color to the end of the Agent's list of memories.

When you ask it a question, here's what happens:

- We call the `respond_to_question` method on Agent
- This calls the `respond_to_question` method of the AgentVerbalSystem
- This interprets the question in terms of concepts the agent knows.
- The verbal system then often calls the `check_statement` method of the AgentReasoningSystem, which does logical inference based on inputs to the reasoning system from other modules--in particular, from the Agent's `memory` and `current_color` fields.

### Consciousness explananda

#### Inverted spectrum

This comes from the interaction between the memory and the reasoning system. Instead of the reasoning system being given eg a number to describe the color, the reasoning system is only given relationships between colors.

The agent's AgentReasoningSystem has the idea of vision as a function of type `(Agent, Color) -> ColorQuale`. [link] And it knows that this function is injective -- that is, that agents always see different colors differently. (This rules out, for example, red-green color blindness.)

When asked to make a judgement, the AgentReasoningSystem asks the AgentMemory about its visual memory. The AgentMemory only

## Obstacles

There are a bunch of things that it would be nice if my agent could prove, but which I think are very hard to make with Z3, the theorem prover I’m using, and I don’t know if they’re possible with any currently available theorem prover.

### Communication

For example, “No matter what question I ask you, we’ll never be able to know if we’re having the same experience of red”, which is a reasonably good description of ineffability, is *really hard* to express and prove.

Here’s what’s hard about it:

- Talking about what other agents know. This is hard because classical logic doesn’t let you express things like “this agent doesn’t know X, but he does know that X -> Y”. To express this kind of thing, I’d need to use a modal logic theorem prover. I think that such theorem provers exist, but I don’t know how good they are.
- Talking about the communication of other agents. This one is hard because it requires a formalized definition of “communication” which is powerful enough to express everything we want the agent to understand, but which the theorem prover understands well enough to prove things about. I don’t know if there exist theorem provers which can prove properties of communications between agents. (I think it’s 10% likely that it would be easy to build facts about communication on top of modal logic if I knew modal logic better.)

Instead of expressing it properly, I’ve been expressing things like “Humans don’t necessarily have the same experience when they’re looking at the same color.” This expresses part of the idea, but doesn’t imply ineffibility.

### Intuitions/fuzzy logic/probabilistic reasoning

- Not able to explain how some things are more intuitive than others
- Not able to say that you believe one thing by default, but could be convinced to believe another.

### Unable to implement one-off reasoning

eg Armstrong is hard, I think? Becayse ut

### Repetitiveness of the current strategy

As it is, I'm implementing behaviors twice:

- I have to make the agent behave a particular way
- I have to make the agent believe that agents behave a particular way.

To some extent, humans have these beliefs in-built. But more so, we learn these concepts from our experience

## Where could we go from here?

-
