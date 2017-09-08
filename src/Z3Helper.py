from z3 import *

class Z3Helper:
    """
    This class is a set of helper methods for Z3.
    """
    @staticmethod
    def enumerate_type_completely(type, options):
        """
        This asserts that all of the items in the type `type` are contained in the
        array `options`, and all of those are distinct.

        Eg enumerate_type_completely(primary_colors, [red, green, blue])
        asserts that there are only three primary colors, and that they are red,
        green and blue.
        """
        thing = z3.Const("thing-of-type-" + str(type), type)
        return And(
            ForAll([thing], Or(*[thing == option for option in options])),
            Distinct(options)
        )

    @staticmethod
    def for_all(types, claim):
        """
        Thin wrapper around the Z3 ForAll.
        """
        args = claim.__code__.co_varnames
        assert len(types) == len(args)
        arg_vars = [Const(arg, type) for (arg, type) in zip(args, types)]
        return ForAll(arg_vars, claim(*arg_vars))

    @staticmethod
    def there_exists(types, claim):
        """
        Thin wrapper around the Z3 Exists.
        """
        args = claim.__code__.co_varnames
        assert len(types) == len(args)
        arg_vars = [Const(arg, type) for (arg, type) in zip(args, types)]
        return Exists(arg_vars, claim(*arg_vars))

    @staticmethod
    def build_maybe_sort(sort):
        """
        Builds and returns the sort which corresponds to the Haskell Maybe type
        of the sort. So the sort (Maybe Color) means "either a color, or the special
        NoColor value".
        """
        Maybe = Datatype('Maybe<%s>' % sort.name())
        Maybe.declare('Just', ('maybe_value', sort))
        Maybe.declare('Nothing')
        return Maybe.create()

    @staticmethod
    def abs(x):
        """
        Returns the absolute value of a number.
        """
        return If(x > 0, x, -x)
