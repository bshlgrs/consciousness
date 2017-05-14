from Agent import Agent

RED = 10
GREEN = 0

if __name__ == "__main__":
    agent = Agent()

    print "Q: Suppose there are two humans Bob and Jane, do they have the same qualia associated with every color?"
    print agent.respond_to_question(
        ("logic_brief",
            ("for_some", (("Human", "bob"), ("Human", "jane")),
                ("for_all", (("Color", "c"),), ("==", ("vision", "bob", "c"), ("vision", "jane", "c")))
        ))
    )

    print
    print "Q: For all y, does there exist an x such that x = y + 1?"
    print agent.respond_to_question(
        ("logic_brief",
            ("for_all",
                [("int", "y")],
                ('exists', [('int', 'x')], ('==', 'x', ('+', 'y', 1)))
            )
        )
    )



    print
    print "Q: For all two humans, do they see colors the same?"
    print agent.respond_to_question(
        ("logic_brief",
            ('for_all',
                (("Human", "h1"), ("Human", "h2"), ("Color", "c")),
                ("==", ("vision", "h1", "c"), ("vision", "h2", "c"))
            )
        )
    )

    agent.show_color(RED)
    agent.show_color(RED)
    agent.show_color(GREEN)
    agent.show_color(GREEN)


    print
    print "Q: Are your memories at timestep 0 and 1 of the same color?"
    print agent.respond_to_question(
        ('logic_brief',
            ("==", ("memory", "myself", 0), ("memory", "myself", 1))
        )
    )

    print
    print "Q: Are you seeing the same color now as you saw at timestep 0?"
    print agent.respond_to_question(
        ('logic_brief',
            ("==", ("memory", "myself", 1), ("current_quale", "myself"))
        )
    )

    print
    print "Q: Is it possible for an agent to have an illusion of red?"
    print agent.respond_to_question(
        ("is_it_possible",
            ('for_some',
                [("Human", "buck"), ('WorldState', 's'), ("Color", 'c')],
                ("has_illusion",
                    "myself",
                    "s",
                    ("WorldColorFact", 'c')
                )
            )
        )
    )

    print
    print "Q: Is it possible for you to have the illusion that Buck is experiencing a color?"
    print agent.respond_to_question(
        ("is_it_possible",
            ('for_some',
                [("Human", "buck"), ('WorldState', 's'), ("Color", 'c')],
                ("has_illusion",
                    "myself",
                    "s",
                    ("ExperienceFact", "buck", ("vision", "buck", 'c'))
                )
            )
        )
    )

    print
    print "Q: Is it possible for Buck to have an illusion that he is having the experience of redness?"
    print agent.respond_to_question(
        ("is_it_possible",
            ('for_some',
                [("Human", "buck"), ('WorldState', 's'), ("Color", 'c')],
                ("has_illusion",
                    "buck",
                    "s",
                    ("ExperienceFact", "buck", ("vision", "buck", 'c'))
                )
            )
        )
    )
