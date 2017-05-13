from z3 import *

class Z3Helper:
    @staticmethod
    def enumerate_type_completely(type, options):
        thing = z3.Const("thing-of-type-" + str(type), type)
        return And(
            ForAll([thing], Or(*[thing == option for option in options])),
            Distinct(options)
        )

    @staticmethod
    def for_all(types, claim):
        args = claim.__code__.co_varnames
        assert len(types) == len(args)
        arg_vars = [Const(arg, type) for (arg, type) in zip(args, types)]
        return ForAll(arg_vars, claim(*arg_vars))

    @staticmethod
    def there_exists(types, claim):
        args = claim.__code__.co_varnames
        assert len(types) == len(args)
        arg_vars = [Const(arg, type) for (arg, type) in zip(args, types)]
        return Exists(arg_vars, claim(*arg_vars))

    @staticmethod
    def has_set_of(owner_sort, things_sort, function_name):
        return Function(function_name, [things_sort, owner_sort], BoolSort())

    @staticmethod
    def build_maybe_sort(sort):
        Maybe = Datatype('Maybe<%s>' % sort.name())
        Maybe.declare('Just', ('maybe_value', sort))
        Maybe.declare('Nothing')
        return Maybe.create()
