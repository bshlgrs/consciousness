import random
from enum import Enum
import pytest

class PhilosopherBot():
    def __init__(self):
        self.imagination = PhilosopherBotImagination()
        self.current_quale = None
        self.color_offset = random.randint(-5, 6)
        self.memory = {} # bidirectional map from colors to names

    def react(self, action):
        if type(action) == AskQuestionAction:
            return self.answer(action.question)
        elif type(action) == ShowColorAction:
            self.current_quale = ColorQuale((action.color.hue + self.color_offset + 6) % 6)
        elif type(action) == TellColorNameAction:
            if self.current_quale:
                if self.current_quale in self.memory:
                    current_name = self.memory[self.current_quale]
                    self.memory[self.current_quale] = action.color_name

                    if action.color_name == current_name:
                        return "Yes, I knew that that was {0}".format(current_name)
                    else:
                        return "Weird, I thought that that was {0}, but okay".format(current_name)
                else:
                    self.memory[self.current_quale] = action.color_name
                    return "Ah, so this is {0}".format(action.color_name)
            else:
                return "I am not seeing anything currently, so it doesn't make sense to tell me what color I'm seeing"

    def answer(self, question):
        if type(question) is ForAllQuestion:
            try:
                possibleWorlds = self.imagination.imagine_worlds(question.types)
                failedWorlds = [possibleWorld
                           for possibleWorld in possibleWorlds
                                if not question.predicate(*possibleWorld)]
                if len(failedWorlds) == 0:
                    return "yes, that seems legit"
                else:
                    return "no, that seems wrong. Here is a counterexample: {0}".format(failedWorlds[0])
            except NotImplementedError as e:
                return e.args[0]
        elif type(question) is QueryQuestion:
            if question.query == "current quale present":
                if self.current_quale:
                    return "Yes I am having a visual experience"
                else:
                    return "No I am not having a visual experience"
            elif question.query == "current quale details":
                if self.current_quale:
                    return "Here is everything I know: {0}".format(self.current_quale.verbally_accessible_details(self.memory))
                else:
                    return "No I am not having a visual experience"
            else:
                return "I don't know what '{0}' means, so cannot answer that question".format(question.query)
        else:
            return "I don't know how to answer that"

    def react_to_multiple(self, multiple_actions):
        for action in multiple_actions:
            self.react(action)


class PhilosopherBotImagination:
    @staticmethod
    def imagine_single(type_):
        def arb(type_2):
            return PhilosopherBotImagination.imagine_single(type_2)

        if type_ == int:
            return random.randint(-100, 100)
        elif type_ == str:
            return random.choice(["green", "blue", "red", "orange", "squeeblish"])
        elif type_ == "baby":
            return Human()
        elif type_ == "history":
            return [arb(Action) for _ in range(random.randint(0, 5))]
        elif type_ == Human:
            actions = arb("history")
            human = Human()
            human.react_to_multiple(actions)

            return human
        elif type_ == Action:
            return random.choice([arb(ShowColorAction), arb(AskQuestionAction), arb(TellColorNameAction)])
        elif type_ == Color:
            return Color(random.randint(0, 5))
        elif type_ == ColorQuale:
            return ColorQuale(random.randint(0, 5))
        elif type_ == ShowColorAction:
            return ShowColorAction(arb(Color))
        elif type_ == AskQuestionAction:
            return AskQuestionAction(arb(Question))
        elif type_ == TellColorNameAction:
            return TellColorNameAction(arb(str))
        elif type_ == Question:
            return arb(QueryQuestion)
        elif type_ == QueryQuestion:
            return QueryQuestion(random.choice(["current quale present"]))
        else:
            raise NotImplementedError("I don't know how to imagine a {0}".format(type_))

    @staticmethod
    def imagine_worlds(types):
        for i in range(100):
            yield [PhilosopherBotImagination.imagine_single(type_) for type_ in types]


class ModelableThing:
    def model(self, action):
        pass

    def current_quale(self):
        raise NotImplementedError()


class Color(Enum):
    MAGENTA = 0
    RED = 1
    YELLOW = 2
    GREEN = 3
    CYAN = 4
    BLUE = 5

    def __init__(self, hue: int):
        self.hue = hue


class ColorQuale:
    def __init__(self, hue_feeling: int):
        self.hue_feeling = hue_feeling

    def verbally_accessible_details(self, memory):
        if self in memory:
            return "I think the name for this color is {0}".format(memory[self])
        else:
            return "This is a color I have not seen before"



class Human(ModelableThing, PhilosopherBot):
    def __init__(self):
        self._current_quale = None
        super(Human, self).__init__()


class Action:
    pass

class AskQuestionAction(Action):
    def __init__(self, question):
        super(AskQuestionAction, self).__init__()

        self.question = question

class ShowColorAction(Action):
    def __init__(self, color):
        self.color = color

class TellColorNameAction(Action):
    def __init__(self, color_name):
        self.color_name = color_name

class Question:
    def __init__(self):
        pass

class ForAllQuestion:
    def __init__(self, types, predicate):
        self.types = types
        self.predicate = predicate


class QueryQuestion(Question):
    def __init__(self, query):
        self.query = query
        super(QueryQuestion, self).__init__()

class PhysicalObject(ModelableThing):
    def current_quale(self):
        return None



if __name__ == '__main__':
    def question(q):
        print("\nQ: ", q)

    bot = PhilosopherBot()

    question("Hey bot, are you having any visual experiences right now?")
    print(bot.react(AskQuestionAction(QueryQuestion("current quale present"))))

    question("*shows green*")
    bot.react(ShowColorAction(Color.GREEN))

    question("How about now?")
    print(bot.react(AskQuestionAction(QueryQuestion("current quale present"))))

    question("Okay, can you tell me every verbally accessible fact about your current quale?")
    print(bot.react(AskQuestionAction(QueryQuestion("current quale details"))))

    question("This color is actually called green.")
    print(bot.react(TellColorNameAction("green")))

    question("Okay, can you tell me every verbally accessible fact about your current quale now?")
    print(bot.react(AskQuestionAction(QueryQuestion("current quale details"))))


    #### questions about other humans
    question("Now we're going to talk about other humans.")
    question("Do other humans always have no qualia?")
    print(bot.react(AskQuestionAction(ForAllQuestion([Human], lambda human: human.current_quale is None))))

    question("Do they always have a visual experience?")
    print(bot.react(AskQuestionAction(ForAllQuestion([Human], lambda human: human.current_quale is not None))))

    question("Do physical objects have qualia?")
    print(bot.react(AskQuestionAction(ForAllQuestion([PhysicalObject], lambda human: human.current_quale is not None))))


    #### Inverted spectra
    question("Suppose there are two humans with the same history of experiences. Must their qualia be the same?")
    def two_humans_with_same_history_have_same_qualia(baby, baby2, history):
        baby.react_to_multiple(history)
        baby2.react_to_multiple(history)

        return baby.current_quale == baby2.current_quale

    print(bot.react(AskQuestionAction(ForAllQuestion(["baby", "baby", "history"], two_humans_with_same_history_have_same_qualia))))

    question("But they will still answer every question the same, right?")

    def two_humans_with_same_history_have_same_answers(baby, baby2, history, question):
        baby.react_to_multiple(history)
        baby2.react_to_multiple(history)

        return baby.answer(question) == baby2.answer(question)
    print(bot.react(
        AskQuestionAction(ForAllQuestion(["baby", "baby", "history", QueryQuestion],
                                         two_humans_with_same_history_have_same_answers))))




    #### Knowledge argument (this one is weak)
    question("Suppose someone has seen green before, and I've explained that the color is green. "
             "Do they know what green is like?")
    # yes

    question("Suppose someone has not seen green before. Do they know what it is like?")
    # no

    ## Alternative reading of this question: Is there a set of actions which lead you to see red,
    # except actually seeing red?

    #### Zombies
    question("Okay, so a zombie is physically the same as you, but is just a physical object. Does it have qualia?")
    # no

    question("But would it claim to have qualia?")
    # yes




