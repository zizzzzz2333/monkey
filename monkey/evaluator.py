from .ast import (
    IntegerLiteral,
    Program,
    ExpressionStatement,
    Boolean,
    PrefixExpression,
    InfixExpression,
    BlockStatement,
    IfExpression,
    ReturnStatement,
    LetStatement,
    Identifier,
    FunctionLiteral,
    CallExpression,
    StringLiteral,
    ArrayLiteral,
    IndexExpression,
)
from .object import (
    Integer,
    Boolean as BooleanObject,
    Null,
    ObjectType,
    ReturnValue,
    Function,
    String,
    Builtin,
    Array,
)
from .environment import new_enclosed_environment
from .builtins import builtins

NULL = Null()
TRUE = BooleanObject(True)
FALSE = BooleanObject(False)


def eval_program(program, env):
    result = None
    for s in program.statements:
        result = evaluate(s, env)
        if result is None:
            continue
        if result.type_() == ObjectType.RETURN_VALUE_OBJ:
            return result.value
        elif result.type_() == ObjectType.ERROR_OBJ:
            return result
    return result


def eval_expressions(exps, env):
    result = []
    for e in exps:
        evaluated = evaluate(e, env)
        if is_error(evaluated):
            errs = list()
            errs.append(evaluated)
            return errs
        result.append(evaluated)
    return result


def new_error(format_str, *args):
    return format_str.format(*args)


def is_error(obj):
    if obj is not None:
        return obj.type_() == ObjectType.ERROR_OBJ
    return False


def native_bool_to_bool_lean_object(input):
    if input:
        return TRUE
    return FALSE


def native_double_bool_to_bool_lean_object(left, right):
    if left is right:
        return TRUE
    return FALSE


def eval_bang_operator_expression(right):
    if right is TRUE:
        return FALSE
    elif right is FALSE:
        return TRUE
    elif right is NULL:
        return TRUE
    else:
        return FALSE


def eval_minus_prefix_operator_expression(right):
    if right.type_() != ObjectType.INTEGER_OBJ:
        return new_error('unknown operator: -{}', right.type_())

    value = right.value
    return Integer(-value)


def eval_prefix_expression(operator, right):
    if operator == '!':
        return eval_bang_operator_expression(right)
    elif operator == '-':
        return eval_minus_prefix_operator_expression(right)
    else:
        return new_error('unknown operator: {}{}', operator, right.type_())


def eval_integer_infix_expression(operator, left, right):
    left_value = left.value
    right_value = right.value
    left_type = left.type_()
    right_type = right.type_()

    if operator == '+':
        return Integer(left_value + right_value)
    elif operator == '-':
        return Integer(left_value - right_value)
    elif operator == '*':
        return Integer(left_value * right_value)
    elif operator == '/':
        return Integer(left_value / right_value)
    elif operator == '<':
        return native_bool_to_bool_lean_object(left_value < right_value)
    elif operator == '>':
        return native_bool_to_bool_lean_object(left_value > right_value)
    elif operator == '==':
        if left_type == ObjectType.BOOLEAN_OBJ and right_type == ObjectType.BOOLEAN_OBJ:
            return native_double_bool_to_bool_lean_object(left, right)
        return native_bool_to_bool_lean_object(left_value == right_value)
    elif operator == '!=':
        if left_type == ObjectType.BOOLEAN_OBJ and right_type == ObjectType.BOOLEAN_OBJ:
            return native_double_bool_to_bool_lean_object(left, right)
        return native_bool_to_bool_lean_object(left_value != right_value)
    else:
        return new_error('unknown operator: {} {} {}', left.type_(), operator, right.type_())


def eval_string_infix_expression(operator, left, right):
    if operator != '+':
        return new_error('unknown operator: {} {} {}', left.type_(), operator, right.type_())
    left_value = left.value
    right_value = right.value
    return String(left_value + right_value)


def eval_infix_expression(operator, left, right):
    if left.type_() == ObjectType.INTEGER_OBJ and right.type_() == ObjectType.INTEGER_OBJ:
        return eval_integer_infix_expression(operator, left, right)
    if left.type_() != right.type_():
        return new_error('type mismatch: {} {} {}', left.type_(), operator, right.type_())
    if left.type_() == ObjectType.STRING_OBJ and right.type_() == ObjectType.STRING_OBJ:
        return eval_string_infix_expression(operator, left, right)
    else:
        return new_error('unknown operator: {} {} {}', left.type_(), operator, right.type_())


def eval_array_index_expression(array, index):
    idx = index.value
    max = int(len(array.elements) - 1)

    if idx < 0 or idx > max:
        return NULL

    return array.elements[idx]


def eval_index_expression(left, index):
    if left.type_() == ObjectType.ARRAY_OBJ and index.type_() == ObjectType.INTEGER_OBJ:
        return eval_array_index_expression(left, index)
    else:
        return new_error('index operator not supported: {}'.format(left.type_()))


def is_truthy(obj):
    if obj is NULL:
        return False
    elif obj is TRUE:
        return True
    elif obj is FALSE:
        return False
    else:
        return True


def eval_if_expression(ie, env):
    condition = evaluate(ie.condition, env)

    if is_error(condition):
        return condition
    elif is_truthy(condition):
        return evaluate(ie.consequence, env)
    elif ie.alternative is not None:
        return evaluate(ie.alternative, env)
    else:
        return None


def eval_block_statement(block, env):
    result = None

    for s in block.statements:
        result = evaluate(s, env)
        if result is not None:
            rt = result.type_()
            if rt == ObjectType.RETURN_VALUE_OBJ or rt == ObjectType.ERROR_OBJ:
                return result

    return result


def eval_identifier(node, env):
    val = env.get(node.value)
    if val is not None:
        return val

    builtin = builtins.get(node.value)
    if builtin is not None:
        return builtin

    return new_error('identifier not found: {}'.format(node.value))


def apply_function(fn, args):
    if isinstance(fn, Function):
        extended_env = extend_function_env(fn, args)
        evaluated = evaluate(fn.body, extended_env)
        return unwrap_return_value(evaluated)
    elif isinstance(fn, Builtin):
        return fn.fn(args)

    return new_error('not a function: {}', fn.type_())


def extend_function_env(fn, args):
    env = new_enclosed_environment(fn.env)

    for i in range(len(fn.parameters)):
        param = fn.parameters[i]
        env.set(param.value, args[i])

    return env


def unwrap_return_value(obj):
    if isinstance(obj, ReturnValue):
        return obj.value

    return obj


def evaluate(node, env):
    if isinstance(node, Program):
        return eval_program(node, env)
    elif isinstance(node, IntegerLiteral):
        return Integer(node.value)
    elif isinstance(node, ExpressionStatement):
        return evaluate(node.expression, env)
    elif isinstance(node, Boolean):
        return native_bool_to_bool_lean_object(node.value)
    elif isinstance(node, PrefixExpression):
        right = evaluate(node.right, env)
        if is_error(right):
            return right
        return eval_prefix_expression(node.operator, right)
    elif isinstance(node, InfixExpression):
        left = evaluate(node.left, env)
        if is_error(left):
            return left
        right = evaluate(node.right, env)
        if is_error(right):
            return right
        return eval_infix_expression(node.operator, left, right)
    elif isinstance(node, BlockStatement):
        return eval_block_statement(node, env)
    elif isinstance(node, IfExpression):
        return eval_if_expression(node, env)
    elif isinstance(node, ReturnStatement):
        val = evaluate(node.value, env)
        if is_error(val):
            return val
        return ReturnValue(val)
    elif isinstance(node, LetStatement):
        val = evaluate(node.value, env)
        if is_error(val):
            return val
        env.set(node.name.value, val)
    elif isinstance(node, Identifier):
        return eval_identifier(node, env)
    elif isinstance(node, FunctionLiteral):
        params = node.parameters
        body = node.body
        return Function(params, body, env)
    elif isinstance(node, CallExpression):
        func = evaluate(node.function, env)
        if is_error(func):
            return func
        args = eval_expressions(node.arguments, env)
        if len(args) == 1 and is_error(args[0]):
            return args[0]
        return apply_function(func, args)
    elif isinstance(node, StringLiteral):
        return String(node.value)
    elif isinstance(node, ArrayLiteral):
        elements = eval_expressions(node.elements, env)
        if len(elements) == 1 and is_error(elements[0]):
            return elements[0]
        return Array(elements)
    elif isinstance(node, IndexExpression):
        left = evaluate(node.left, env)
        if is_error(left):
            return left
        index = evaluate(node.index, env)
        if is_error(index):
            return index
        return eval_index_expression(left, index)
    return None
