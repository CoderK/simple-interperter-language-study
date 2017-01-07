from enum import Enum


class TokenType(Enum):
    IDENTIFIER = 0,
    NUMBER = 1,
    MINUS = 2,
    PLUS = 3,
    MULTIPLY = 4
    DIVISION = 5,
    MOD = 6,
    POWER = 7,
    L_PAREN = 8,
    R_PAREN = 9
