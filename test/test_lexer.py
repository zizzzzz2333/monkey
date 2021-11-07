import unittest
from monkey.lexer import Lexer
from monkey.token import Token, TokenType


class TestLexer(unittest.TestCase):
    def assert_token_equal(self, first, second):
        self.assertEqual(first._type, second._type)
        self.assertEqual(first._literal, second._literal)

    def test_next_token(self):
        input_str = '  =+(){},;abc56!-/*5;5 < 10 > 5;if (5 < 10) {return true;} else {return false;}10 == 10;10 != 9;'
        output_list = [Token(TokenType.ASSIGN, '='),
                       Token(TokenType.PLUS, '+'),
                       Token(TokenType.LPAREN, '('),
                       Token(TokenType.RPAREN, ')'),
                       Token(TokenType.LBRACE, '{'),
                       Token(TokenType.RBRACE, '}'),
                       Token(TokenType.COMMA, ','),
                       Token(TokenType.SEMICOLON, ';'),
                       Token(TokenType.IDENT, 'abc'),
                       Token(TokenType.INT, '56'),
                       Token(TokenType.BANG, '!'),
                       Token(TokenType.MINUS, '-'),
                       Token(TokenType.SLASH, '/'),
                       Token(TokenType.ASTERISK, '*'),
                       Token(TokenType.INT, '5'),
                       Token(TokenType.SEMICOLON, ';'),
                       Token(TokenType.INT, '5'),
                       Token(TokenType.LT, '<'),
                       Token(TokenType.INT, '10'),
                       Token(TokenType.GT, '>'),
                       Token(TokenType.INT, '5'),
                       Token(TokenType.SEMICOLON, ';'),
                       Token(TokenType.IF, 'if'),
                       Token(TokenType.LPAREN, '('),
                       Token(TokenType.INT, '5'),
                       Token(TokenType.LT, '<'),
                       Token(TokenType.INT, '10'),
                       Token(TokenType.RPAREN, ')'),
                       Token(TokenType.LBRACE, '{'),
                       Token(TokenType.RETURN, 'return'),
                       Token(TokenType.TRUE, 'true'),
                       Token(TokenType.SEMICOLON, ';'),
                       Token(TokenType.RBRACE, '}'),
                       Token(TokenType.ELSE, 'else'),
                       Token(TokenType.LBRACE, '{'),
                       Token(TokenType.RETURN, 'return'),
                       Token(TokenType.FALSE, 'false'),
                       Token(TokenType.SEMICOLON, ';'),
                       Token(TokenType.RBRACE, '}'),
                       Token(TokenType.INT, '10'),
                       Token(TokenType.EQ, '=='),
                       Token(TokenType.INT, '10'),
                       Token(TokenType.SEMICOLON, ';'),
                       Token(TokenType.INT, '10'),
                       Token(TokenType.NOT_EQ, '!='),
                       Token(TokenType.INT, '9'),
                       Token(TokenType.SEMICOLON, ';'),
                       Token(TokenType.EOF, '')]

        l = Lexer(input_str)
        for o in output_list:
            t = l.next_token()
            self.assert_token_equal(t, o)
