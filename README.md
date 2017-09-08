# A software agent illustrating some features of an illusionist account of consciousness

This repo contains the code that I (Buck Shlegeris) wrote for the Open Philanthropy Project as part of their investigations into moral patienthood.

TODO: You can read the report HERE.

If you run `src/ExampleRun.py`, you'll get this output:

    Q: What's 2 + 2?
    4

    Q: Suppose there are two agents Bob and Jane, do they have the same qualia associated with every color?
    Both that statement and its negation are possible.

    Q: For all y, does there exist an x such that x = y + 1?
    Yes.

    Q: For all two agents, do they see colors the same?
    Both that statement and its negation are possible.

    Q: Are your memories at timestep 0 and 1 of the same color?
    Yes.

    Q: Are you seeing the same color now as you saw at timestep 0?
    No.

    Q: Is it possible for an agent to have an illusion of red?
    Yes.

    Q: Is it possible for you to have the illusion that Buck is experiencing a color?
    Yes.

    Q: Is it possible for Buck to have an illusion that he is having the experience of redness?
    No, that's impossible.

The easiest way to play around with the code is to edit that file.

## How to read this code

The agent itself is defined in in the files `Agent.py`, `AgentVerbalSystem.py`, and `AgentReasoningSystem.py`.

- In `Agent.py`, we define the `Agent` class as well as the methods `show_color` and `respond_to_question`, which are the two methods through which we interact with the agent.
- In `AgentVerbalSystem.py`

### Glossary of first order logic terms

- *Proposition*. A truth claim. It can have variables in it, eg the proposition `x > y`, which might or might not be true depending on what `x` and `y` are.
- *Model*. A model is a set of values for all the variables in a set of propositions. In the previous example, a model might be "x = 5, y = 6".
- *Satisfiable*. A proposition is satisfiable if there is a model such that the proposition is true.
- *Valid*. A proposition is valid if it is true for all variable assignments. For example, the proposition "x + y = y + x" is valid, because it's true for all values of `x` and `y`. Note that a proposition is valid if and only if its negation is not satisfiable--this equivalence is central to how Z3 works.
- *Sort*. Z3 uses an extension of first order logic called many-sorted logic, which has the concept of a sort. A sort is basically what you'd call a type in a programming language. Some examples of sorts are: Boolean, Integer, RealNumber, and in the context of this program there are sorts like Human, Color, and ColorQuale.
