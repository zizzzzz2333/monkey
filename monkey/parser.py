from .token import Token, TokenType
from .ast import (
    Program,
    LetStatement,
    Identifier,
    ReturnStatement,
    ExpressionStatement,
    IntegerLiteral,
    PrefixExpression,
    InfixExpression,
    IfExpression,
    BlockStatement,
    Boolean,
    FunctionLiteral,
    CallExpression,
    StringLiteral,
    ArrayLiteral,
    IndexExpression,
)

# operator precedences
LOWEST = 0
EQUALS = 1
LESSGREATER = 2
SUM = 3
PRODUCT = 4
PREFIX = 5
CALL = 6
INDEX = 7

# token precedences
precedences = {
    TokenType.EQ: EQUALS,
    TokenType.NOT_EQ: EQUALS,
    TokenType.LT: LESSGREATER,
    TokenType.GT: LESSGREATER,
    TokenType.PLUS: SUM,
    TokenType.MINUS: SUM,
    TokenType.SLASH: PRODUCT,
    TokenType.ASTERISK: PRODUCT,
    TokenType.LPAREN: CALL,
    TokenType.LBRACKET: INDEX,
}


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.cur_token = Token(TokenType.EOF, '')
        self.peek_token = Token(TokenType.EOF, '')
        self.errors = []
        self.prefix_parse_functions = dict()
        self.register_prefix(TokenType.IDENT, self.parse_identifier)
        self.register_prefix(TokenType.INT, self.parse_integer_literal)
        self.register_prefix(TokenType.BANG, self.parse_prefix_expression)
        self.register_prefix(TokenType.MINUS, self.parse_prefix_expression)
        self.register_prefix(TokenType.TRUE, self.parse_boolean)
        self.register_prefix(TokenType.FALSE, self.parse_boolean)
        self.register_prefix(TokenType.LPAREN, self.parse_grouped_expression)
        self.register_prefix(TokenType.IF, self.parse_if_expression)
        self.register_prefix(TokenType.FUNCTION, self.parse_function_literal)
        self.register_prefix(TokenType.STRING, self.parse_string_literal)
        self.register_prefix(TokenType.LBRACKET, self.parse_array_literal)
        self.infix_parse_functions = dict()
        self.register_infix(TokenType.LPAREN, self.parse_call_expression)
        self.register_infix(TokenType.PLUS, self.parse_infix_expression)
        self.register_infix(TokenType.MINUS, self.parse_infix_expression)
        self.register_infix(TokenType.SLASH, self.parse_infix_expression)
        self.register_infix(TokenType.ASTERISK, self.parse_infix_expression)
        self.register_infix(TokenType.EQ, self.parse_infix_expression)
        self.register_infix(TokenType.NOT_EQ, self.parse_infix_expression)
        self.register_infix(TokenType.LT, self.parse_infix_expression)
        self.register_infix(TokenType.GT, self.parse_infix_expression)
        self.register_infix(TokenType.LBRACKET, self.parse_index_expression)


        self.next_token()
        self.next_token()

    def next_token(self):
        self.cur_token = self.peek_token
        self.peek_token = self.lexer.next_token()

    def expect_peek(self, token_type):
        if self.peek_token_is(token_type):
            self.next_token()
            return True
        else:
            self.peek_error(token_type)
            return False

    def peek_token_is(self, token_type):
        return self.peek_token._type == token_type

    def cur_token_is(self, token_type):
        return self.cur_token._type == token_type

    def register_prefix(self, token, function):
        self.prefix_parse_functions[token] = function

    def register_infix(self, token, function):
        self.infix_parse_functions[token] = function

    def parse_program(self):
        program = Program()

        while self.cur_token._type != TokenType.EOF:
            statement = self.parse_statement()
            if statement is not None:
                program.statements.append(statement)

            self.next_token()

        return program

    def parse_identifier(self):
        i = Identifier(self.cur_token, self.cur_token._literal)
        return i

    def parse_statement(self):
        if self.cur_token_is(TokenType.LET):
            return self.parse_let_statement()
        elif self.cur_token_is(TokenType.RETURN):
            return self.parse_return_statement()
        else:
            return self.parse_expression_statement()

    def parse_let_statement(self):
        statement = LetStatement(self.cur_token)

        if not self.expect_peek(TokenType.IDENT):
            return None

        statement.name = Identifier(self.cur_token, self.cur_token._literal)

        if not self.expect_peek(TokenType.ASSIGN):
            return None

        self.next_token()
        statement.value = self.parse_expression(LOWEST)

        if self.peek_token_is(TokenType.SEMICOLON):
            self.next_token()

        return statement

    def parse_return_statement(self):
        statement = ReturnStatement(self.cur_token)

        self.next_token()

        statement.value = self.parse_expression(LOWEST)

        if self.peek_token_is(TokenType.SEMICOLON):
            self.next_token()

        return statement

    def parse_expression(self, precedence):
        prefix = self.prefix_parse_functions.get(self.cur_token._type)
        if not prefix:
            self.no_prefix_parse_function_error(self.cur_token._type)
            return prefix
        left_exp = prefix()

        while not self.peek_token_is(TokenType.SEMICOLON) and precedence < self.peek_precedence():
            infix = self.infix_parse_functions.get(self.peek_token._type)
            if infix is None:
                return left_exp

            self.next_token()
            left_exp = infix(left_exp)

        return left_exp

    def parse_expression_statement(self):
        statement = ExpressionStatement(self.cur_token)

        statement.expression = self.parse_expression(LOWEST)
        if self.peek_token_is(TokenType.SEMICOLON):
            self.next_token()

        return statement

    def parse_integer_literal(self):
        integer = IntegerLiteral(self.cur_token)
        try:
            value = int(integer.token_literal())
        except Exception as e:
            print('{}: Could not parse {} as integer'.format(e, integer.token_literal()))
            return None
        integer.value = value

        return integer

    def peek_error(self, expect_token):
        msg = "expected next token to be {}, got {} instead"
        self.errors.append(msg.format(expect_token, self.peek_token._type))

    def no_prefix_parse_function_error(self, token_type):
        s = 'no prefix parse function for {} found'.format(token_type)
        self.errors.append(s)

    def parse_prefix_expression(self):
        expression = PrefixExpression(self.cur_token, self.cur_token._literal)
        self.next_token()

        expression.right = self.parse_expression(PREFIX)

        return expression

    def peek_precedence(self):
        p = precedences.get(self.peek_token._type)
        return p if p else LOWEST

    def cur_precedence(self):
        p = precedences.get(self.cur_token._type)
        return p if p else LOWEST

    def parse_infix_expression(self, left):
        expression = InfixExpression(self.cur_token, self.cur_token._literal, left)

        precedence = self.cur_precedence()
        self.next_token()
        expression.right = self.parse_expression(precedence)

        return expression

    def parse_boolean(self):
        b = Boolean(self.cur_token, self.cur_token_is(TokenType.TRUE))
        return b

    def parse_grouped_expression(self):
        self.next_token()

        exp = self.parse_expression(LOWEST)

        if not self.expect_peek(TokenType.RPAREN):
            return None

        return exp

    def parse_if_expression(self):
        expression = IfExpression(self.cur_token)
        if not self.expect_peek(TokenType.LPAREN):
            return None

        self.next_token()
        expression.condition = self.parse_expression(LOWEST)
        if not self.expect_peek(TokenType.RPAREN):
            return None

        if not self.expect_peek(TokenType.LBRACE):
            return None

        expression.consequence = self.parse_block_statement()
        if self.peek_token_is(TokenType.ELSE):
            self.next_token()

            if not self.expect_peek(TokenType.LBRACE):
                return None

            expression.alternative = self.parse_block_statement()
        return expression

    def parse_block_statement(self):
        block = BlockStatement(self.cur_token)
        block.statements = []

        self.next_token()

        while not self.cur_token_is(TokenType.RBRACE):
            statement = self.parse_statement()
            if not statement is None:
                block.statements.append(statement)
            self.next_token()

        return block

    def parse_function_literal(self):
        literal = FunctionLiteral(self.cur_token)

        if not self.expect_peek(TokenType.LPAREN):
            return None

        literal.parameters = self.parse_function_parameters()

        if not self.expect_peek(TokenType.LBRACE):
            return None

        literal.body = self.parse_block_statement()

        return literal

    def parse_function_parameters(self):
        identifiers = []

        if self.peek_token_is(TokenType.RPAREN):
            self.next_token()
            return identifiers

        self.next_token()

        identifier = Identifier(self.cur_token, self.cur_token._literal)
        identifiers.append(identifier)

        if not self.expect_peek(TokenType.RPAREN):
            return None

        return identifiers

    def parse_call_expression(self, function):
        exp = CallExpression(self.cur_token, function)
        exp.arguments = self.parse_expression_list(TokenType.RPAREN)
        return exp

    def parse_call_arguments(self):
        args = []

        if self.peek_token_is(TokenType.RPAREN):
            self.next_token()
            return args

        self.next_token()
        args.append(self.parse_expression(LOWEST))

        while self.peek_token_is(TokenType.COMMA):
            self.next_token()
            self.next_token()
            args.append(self.parse_expression(LOWEST))

        if not self.expect_peek(TokenType.RPAREN):
            return None

        return args

    def parse_expression_list(self, end):
        lst = []

        if self.peek_token_is(end):
            self.next_token()
            return lst

        self.next_token()
        lst.append(self.parse_expression(LOWEST))

        while self.peek_token_is(TokenType.COMMA):
            self.next_token()
            self.next_token()
            lst.append(self.parse_expression(LOWEST))

        if not self.expect_peek(end):
            return None

        return lst

    def parse_string_literal(self):
        return StringLiteral(self.cur_token, self.cur_token._literal)

    def parse_array_literal(self):
        array = ArrayLiteral(self.cur_token)
        array.elements = self.parse_expression_list(TokenType.RBRACKET)

        return array

    def parse_index_expression(self, left):
        exp = IndexExpression(self.cur_token, left)

        self.next_token()
        exp.index = self.parse_expression_list(LOWEST)

        if not self.expect_peek(TokenType.RBRACKET):
            return None

        return exp