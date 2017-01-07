import re
from src.enums.token_type import TokenType
from src.lexer.token_table import token_table


def is_digit(c):
    return bool(re.match('[0-9]', c))


def is_whitespace(c):
    return bool(re.match('\s', c))


def is_operator(c):
    return bool(re.match('[+\-*\/\^%=(),]', c))


def is_identifier(c):
    return type(c) == str \
           and not is_operator(c) \
           and not is_digit(c) \
           and not is_whitespace(c)


def lex(input_value):
    tokens = []
    idx = 0

    if input_value == '':
        return tokens

    while idx < len(input_value):
        c = input_value[idx]

        if is_whitespace(c):
            idx += 1

        elif is_operator(c):
            tokens.append({
                'type': token_table[c]
            })
            idx += 1

        elif is_digit(c):
            num = c
            idx += 1

            while idx < len(input_value):
                c = input_value[idx]
                if is_digit(c):
                    num += c
                    idx += 1
                else: break

            tokens.append({
                'type': TokenType.NUMBER,
                'value': int(num)
            })

        elif is_identifier(c):
            identifier = c
            idx += 1

            while idx < len(input_value):
                c = input_value[idx]
                if is_identifier(c):
                    identifier += c
                    idx += 1
                else: break

            tokens.append({
                'type': TokenType.IDENTIFIER,
                'value': identifier
            })

    return tokens
