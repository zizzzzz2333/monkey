from .object import (
    Builtin,
    String,
    Integer,
)


def new_error(format_str, *args):
    return format_str.format(*args)


def __len(args):
    if len(args) != 1:
        return new_error('wrong number of arguments. got={}, want=1', len(args))

    arg = args[0]
    if isinstance(arg, String):
        return Integer(int(len(arg.value)))

    return new_error("argument to 'len' not supported, got {}", arg.type_())


builtins = {
    'len': Builtin(__len)
}