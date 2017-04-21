from z3_consciousness import PhilosopherBot
import unittest



PROVABLE = "That statement is provable."
NOT_CONSISTENT = 'That statement is not consistent with my other beliefs.'
UNDETERMINED = "Both that statement and its negation are possible."

class TestStringMethods(unittest.TestCase):
    def setUp(self):
        self.philosopher_bot = PhilosopherBot()

    def test_math(self):
        """Is there an x for every y such that x == y + 1?
        """
        self.assertEqual(PROVABLE, self.philosopher_bot.ask_question(
            ("logic-brief",
                ("for-all",
                    [("int", "y")],
                    ('exists', [('int', 'x')], ('==', 'x', ('+', 'y', 1)))
                )
            )
        ))

    def test_inverted_spectrum(self):
        """For all two humans, if they are unequal are their color
         experiences of the same color guaranteed to be the same?"""

        res = self.philosopher_bot.ask_question(
            ("logic-brief",
                ('for-all',
                    (("human", "h1"), ("human", "h2")),
                    ("and",
                        ("!=", "h1", "h2"),
                        ("for-all", (("color", "c"),), ("==", ("vision", "h1", "c"), ("vision", "h2", "c")))
                    )
                )
            )
        )

        self.assertEqual(res, NOT_CONSISTENT)

        res = self.philosopher_bot.ask_question(
            ("logic-brief",
                ("for-some", (("human", "h1"), ("human", "h2")),
                    ("for-all", (("color", "c"),), ("==", ("vision", "h1", "c"), ("vision", "h2", "c")))
            ))
        )

        self.assertEqual(res, UNDETERMINED)



if __name__ == '__main__':
    unittest.main()
