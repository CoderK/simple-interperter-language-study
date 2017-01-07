from src.enums.token_type import TokenType

token_table = {
    '-': TokenType.MINUS,
    '+': TokenType.PLUS,
    '*': TokenType.MULTIPLY,
    '/': TokenType.DIVISION,
    '%': TokenType.MOD,
    '^': TokenType.POWER,
    '(': TokenType.L_PAREN,
    ')': TokenType.R_PAREN
}