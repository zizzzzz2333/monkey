import unittest
from monkey.token import Token, TokenType


class TestToken(unittest.TestCase):
    def test_repr(self):
        token = Token(TokenType.ASSIGN, '=')
        token_repr = 'Token(TokenType.ASSIGN, "=")'
        self.assertEqual(repr(token), token_repr)
