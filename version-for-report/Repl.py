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
        print "doing %s"%question
    elif question[0] == "(":
        print agent.respond_to_question(parse_sexpr(question))
