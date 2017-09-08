from Agent import Agent
from SexprParser import parse_sexpr
import readline

"""
You can run this program if you want to interact with the agent over text.

It's actually really painful to interact with the agent this way, so I recommend
against using this. You'll have a better time if you interact with it through code,
like in `ExampleRun.py`.

"""


question = None
agent = Agent()

print "** Interacting with consciousness simulating agent **"
print "** Type :q to quit **"

while question is not ":q":
    question = raw_input("> ")
    if question[0] == ":":
        params = question.split(' ')
        command = params[0]
        if command == ":show":
            color = params[1]
            print "show color " + color
            color_num = int(color) # TODO: validate
            agent.show_color(color_num)
        elif command == ':q':
            exit(0)
        else:
            print "The only allowed action is :show and :q"
    elif question[0] == "(":
        print agent.ask_question(parse_sexpr(question))
