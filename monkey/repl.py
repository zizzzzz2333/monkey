from .lexer import Lexer
from .parser import Parser
from .token import TokenType
from .evaluator import evaluate
from .environment import Environment


# def start():
#     prompt = '>> '
#     while True:
#         str_input = input(prompt)
#         l = Lexer(str_input)
#         token = l.next_token()
#         while token._type != TokenType.EOF:
#             print(token)
#             token = l.next_token()

def print_parse_errors(errors):
    print('parser errors:\n')
    for e in errors:
        print('\t{}\n'.format(e))


def start():
    prompt = '>> '
    env = Environment()
    while True:
        str_input = input(prompt)
        l = Lexer(str_input)
        p = Parser(l)

        program = p.parse_program()
        if not len(p.errors) == 0:
            print_parse_errors(p.errors)
            continue

        evaluated = evaluate(program, env)
        if evaluated is not None:
            print(evaluated.inspect())

        # print('{}\n'.format(str(program)))