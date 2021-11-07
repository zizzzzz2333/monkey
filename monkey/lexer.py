from .token import Token, TokenType


class Lexer:
    def __init__(self, input_str):
        self.ch = ''
        self.position = 0
        self.read_position = 0
        self.input_str = input_str
        self._keyword_map = {
            'fn': TokenType.FUNCTION,
            'let': TokenType.LET,
            'true': TokenType.TRUE,
            'false': TokenType.FALSE,
            'if': TokenType.IF,
            'else': TokenType.ELSE,
            'return': TokenType.RETURN
        }
        self.read_char()

    def next_token(self):
        self.skip_white_space()

        if self.ch == '=':
            if self.peek_char() == '=':
                ch = self.ch
                self.read_char()
                tk = Token(TokenType.EQ, ch + self.ch)
            else:
                tk = Token(TokenType.ASSIGN, self.ch)
        elif self.ch == '+':
            tk = Token(TokenType.PLUS, self.ch)
        elif self.ch == '-':
            tk = Token(TokenType.MINUS, self.ch)
        elif self.ch == '!':
            if self.peek_char() == '=':
                ch = self.ch
                self.read_char()
                tk = Token(TokenType.NOT_EQ, ch + self.ch)
            else:
                tk = Token(TokenType.BANG, self.ch)
        elif self.ch == '/':
            tk = Token(TokenType.SLASH, self.ch)
        elif self.ch == '*':
            tk = Token(TokenType.ASTERISK, self.ch)
        elif self.ch == '<':
            tk = Token(TokenType.LT, self.ch)
        elif self.ch == '>':
            tk = Token(TokenType.GT, self.ch)
        elif self.ch == ',':
            tk = Token(TokenType.COMMA, self.ch)
        elif self.ch == '(':
            tk = Token(TokenType.LPAREN, self.ch)
        elif self.ch == ')':
            tk = Token(TokenType.RPAREN, self.ch)
        elif self.ch == '{':
            tk = Token(TokenType.LBRACE, self.ch)
        elif self.ch == '}':
            tk = Token(TokenType.RBRACE, self.ch)
        elif self.ch == ';':
            tk = Token(TokenType.SEMICOLON, self.ch)
        elif self.is_letter(self.ch):
            token_literal = self.read_identifier()
            token_type = self.look_up_ident_type(token_literal)
            return Token(token_type, token_literal)
        elif self.ch.isdigit():
            token_literal = self.read_number()
            token_type = TokenType.INT
            return Token(token_type, token_literal)
        elif self.ch == '':
            tk = Token(TokenType.EOF, self.ch)
        elif self.ch == '"':
            tk = Token(TokenType.STRING, self.read_string())
        elif self.ch == '[':
            tk = Token(TokenType.LBRACKET, self.ch)
        elif self.ch == ']':
            tk = Token(TokenType.RBRACKET, self.ch)
        else:
            tk = Token(TokenType.ILLEGAL, self.ch)

        self.read_char()
        return tk

    def read_string(self):
        position = self.position + 1
        while True:
            self.read_char()
            if self.ch == '"':
                break
        return self.input_str[position: self.position]

    def read_char(self):
        if self.read_position >= len(self.input_str):
            self.ch = ''
        else:
            self.ch = self.input_str[self.read_position]
        self.position = self.read_position
        self.read_position += 1

    def read_identifier(self):
        position = self.position
        while self.is_letter(self.ch):
            self.read_char()

        return self.input_str[position:self.position]

    def read_number(self):
        position = self.position

        while self.ch.isdigit():
            self.read_char()

        return self.input_str[position:self.position]

    def look_up_ident_type(self, identifier):
        ident_type = self._keyword_map.get(identifier)
        if ident_type is None:
            return TokenType.IDENT
        return ident_type

    @staticmethod
    def is_letter(ch):
        letters = [chr(i) for i in range(97, 123)]
        capital_letters = [chr(i).upper() for i in range(97, 123)]
        letter_list = letters + capital_letters + ['_']
        # print(letter_list)
        return ch in letter_list

    def skip_white_space(self):
        while self.ch == ' ' or self.ch == '\t' or self.ch == '\n' or self.ch == '\r':
            self.read_char()

    def peek_char(self):
        if self.read_position >= len(self.input_str):
            return ''

        return self.input_str[self.read_position]
