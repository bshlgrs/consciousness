from Agent import Agent
from SexprParser import parse_sexpr
import readline

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
