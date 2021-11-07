from abc import ABCMeta, abstractmethod


class Node(metaclass=ABCMeta):
    @abstractmethod
    def token_literal(self):
        pass

    @abstractmethod
    def __str__(self):
        pass


class Program(Node):
    def __init__(self):
        self.statements = []

    def token_literal(self):
        if len(self.statements) > 0:
            return self.statements[0].token_literal()
        else:
            return ''

    def __str__(self):
        r = ''
        for s in self.statements:
            r += str(s)
        return r


class LetStatement(Node):
    def __init__(self, token):
        self.token = token
        self.name = None
        self.value = None

    def token_literal(self):
        return self.token._literal

    def statement_node(self):
        pass

    def __str__(self):
        s = '{} {} = {};'.format(self.token_literal(), self.name, self.value)
        return s


class Identifier(Node):
    def __init__(self, token, value):
        self.token = token
        self.value = value

    def token_literal(self):
        return self.token._literal

    def __str__(self):
        return self.value


class ReturnStatement:
    def __init__(self, token):
        self.token = token
        self.value = None

    def token_literal(self):
        return self.token._literal

    def statement_node(self):
        pass

    def __str__(self):
        s = '{} {};'.format(self.token_literal(), self.value)
        return s


class ExpressionStatement:
    def __init__(self, token):
        self.token = token
        self.expression = None

    def token_literal(self):
        return self.token._literal

    def statement_node(self):
        pass

    def __str__(self):
        return str(self.expression)


class IntegerLiteral:
    def __init__(self, token):
        self.token = token
        self.value = None

    def token_literal(self):
        return self.token._literal

    def statement_node(self):
        pass

    def __str__(self):
        return self.token_literal()


class PrefixExpression:
    def __init__(self, token, operator):
        self.token = token
        self.operator = operator
        self.right = None

    def token_literal(self):
        return self.token._literal

    def statement_node(self):
        pass

    def __str__(self):
        s = '({}{})'.format(self.operator, str(self.right))
        return s


class InfixExpression:
    def __init__(self, token, operator, left):
        self.token = token
        self.left = left
        self.operator = operator
        self.right = None

    def token_literal(self):
        return self.token._literal

    def statement_node(self):
        pass

    def __str__(self):
        s = '({} {} {})'.format(str(self.left), self.operator, str(self.right))
        return s


class IfExpression:
    def __init__(self, token):
        self.token = token
        self.condition = None
        self.consequence = None
        self.alternative = None

    def token_literal(self):
        return self.token._literal

    def __str__(self):
        s = 'if{} {}'.format(str(self.condition), self.consequence)
        if self.alternative is not None:
            s += 'else {}'.format(str(self.alternative))
        return s


class BlockStatement:
    def __init__(self, token):
        self.token = token
        self.statements = []

    def token_literal(self):
        return self.token._literal

    def __str__(self):
        r = ''
        for s in self.statements:
            r += str(s)

        return r


class Boolean:
    def __init__(self, token, value):
        self.token = token
        self.value = value

    def token_literal(self):
        return self.token._literal

    def statement_node(self):
        pass

    def __str__(self):
        return self.token_literal()


class FunctionLiteral:
    def __init__(self, token):
        self.token = token
        self.parameters = []
        self.body = None

    def token_literal(self):
        return self.token._literal

    def __str__(self):
        params = []
        for p in self.parameters:
            params.append(str(p))

        params_str = ', '.join(params)
        s = '({}){}'.format(params_str, str(self.body))

        return s


class CallExpression:
    def __init__(self, token, function):
        self.token = token
        self.function = function
        self.arguments = []

    def token_literal(self):
        return self.token._literal

    def __str__(self):
        arguments = []

        for a in self.arguments:
            arguments.append(str(a))

        arguments_str = ', '.join(arguments)
        s = '{}({})'.format(str(self.function), arguments_str)

        return s


class StringLiteral:
    def __init__(self, token, value):
        self.token = token
        self.value = value

    def token_literal(self):
        return self.token._literal

    def __str__(self):
        return self.token._literal


class ArrayLiteral:
    def __init__(self, token):
        self.token = token
        self.elements = None

    def token_literal(self):
        return self.token._literal

    def __str__(self):
        elements = []
        for el in self.elements:
            elements.append(el)

        elements_str = ', '.join(elements)

        s = '[{}]'.format(elements_str)

        return s


class IndexExpression:
    def __init__(self, token, left):
        self.token = token
        self.left = left
        self.index = None

    def token_literal(self):
        return self.token._literal

    def __str__(self):
        s = '({}[{}])'.format(str(self.left), str(self.index))
        return s