class ObjectType:
    INTEGER_OBJ = 'INTEGER'
    BOOLEAN_OBJ = 'BOOLEAN'
    NULL_OBJ = 'NULL'
    RETURN_VALUE_OBJ = 'RETURN_VALUE'
    ERROR_OBJ = 'ERROR'
    FUNCTION_OBJ = 'FUNCTION'
    STRING_OBJ = 'STRING'
    BUILTIN_OBJ = 'BUILTIN'
    ARRAY_OBJ = 'ARRAY'


class Integer:
    def __init__(self, value):
        self.value = value

    @staticmethod
    def type_():
        return ObjectType.INTEGER_OBJ

    def inspect(self):
        return str(self.value)


class Boolean:
    def __init__(self, value):
        self.value = value

    @staticmethod
    def type_():
        return ObjectType.BOOLEAN_OBJ

    def inspect(self):
        return str(self.value)


class Null:
    def __init__(self):
        pass

    @staticmethod
    def type_():
        return ObjectType.NULL_OBJ

    @staticmethod
    def inspect(self):
        return 'null'


class ReturnValue:
    def __init__(self, value):
        self.value = value

    @staticmethod
    def type_():
        return ObjectType.RETURN_VALUE_OBJ

    def inspect(self):
        return self.value.inspect()


class Function:
    def __init__(self, params, body, env):
        self.parameters = params
        self.body = body
        self.env = env

    @staticmethod
    def type_():
        return ObjectType.FUNCTION_OBJ

    def inspect(self):
        params = []
        for p in self.parameters:
            params.append(str(p))
        params_str = ', '.join(params)
        s = 'fn({}) {{\n{}\n}}'.format(params_str, str(self.body))

        return s


class String:
    def __init__(self, value):
        self.value = value
        pass

    @staticmethod
    def type_():
        return ObjectType.STRING_OBJ

    def inspect(self):
        return self.value


class Builtin:
    def __init__(self, fn):
        self.fn = fn

    @staticmethod
    def type_():
        return ObjectType.BUILTIN_OBJ

    @staticmethod
    def inspect():
        return 'builtin function'


class Array:
    def __init__(self, elements):
        self.elements = elements

    @staticmethod
    def type_():
        return ObjectType.ARRAY_OBJ

    def inspect(self):
        elements = []

        for e in self.elements:
            elements.append(e.inspect())

        elements_str = ', '.join(elements)

        s = '[{}]'.format(elements_str)
        return s


class Error:
    def __init__(self, message):
        self.message = message

    @staticmethod
    def type_():
        return ObjectType.ERROR_OBJ

    def inspect(self):
        return 'ERROR: {}'.format(self.message)