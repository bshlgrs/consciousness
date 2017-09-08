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
