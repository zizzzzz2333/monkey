from enum import Enum, unique


@unique
class TokenType(Enum):
    ASSIGN = 0
    PLUS = 1
    LPAREN = 2
    RPAREN = 3
    LBRACE = 4
    RBRACE = 5
    COMMA = 6
    SEMICOLON = 7
    FUNCTION = 8
    LET = 9
    IDENT = 10
    INT = 11
    ILLEGAL = 12
    EOF = 13
    MINUS = 14
    BANG = 15
    ASTERISK = 16
    SLASH = 17
    LT = 18
    GT = 19
    TRUE = 20
    FALSE = 21
    IF = 22
    ELSE = 23
    RETURN = 24
    EQ = 25
    NOT_EQ = 26
    STRING = 27
    LBRACKET = 28
    RBRACKET = 29

    def __int__(self):
        return self.value

    def __repr__(self):
        template = 'TokenType.{}'
        return template.format(self.name)


class Token:
    def __init__(self, _type, literal):
        self._type = _type
        self._literal = literal

    def __repr__(self):
        template = 'Token({}, "{}")'
        return template.format(self._type, self._literal)
