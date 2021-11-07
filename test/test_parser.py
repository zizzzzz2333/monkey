import unittest
from monkey.lexer import Lexer
from monkey.parser import Parser


class TestParser(unittest.TestCase):
    def test_let_statements(self):
        input = 'let x  5;let y = 10;let foobar = 838383;'
        l = Lexer(input)
        p = Parser(l)

        program = p.parse_program()
        self.check_parse_errors(p)
        self.assertEqual(len(program.statements), 3)

        expect_identifier_names = ["x", "y", "foobar"]

        for i in range(len(expect_identifier_names)):
            s = program.statements[i]
            n = expect_identifier_names[i]
            self.assert_let_statement_name_equal(s, n)

    def assert_let_statement_name_equal(self, statement, name):
        self.assertEqual(statement.token_literal(), "let")
        self.assertEqual(statement.name.value, name)
        self.assertEqual(statement.name.token_literal(), name)

    def check_parse_errors(self, program):
        errors = program.errors

        if len(errors) == 0:
            return

        print("parser has {} errors".format(len(errors)))
        for msg in errors:
            print("parse error: {}".format(msg))

        self.fail()
