from src.enums.token_type import TokenType


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.symbols = {}
        self.workingIndex = 0

        self._add_infix()
        self._add_prefix()
        self._add_symbols()

    def parse(self):
        parse_tree = []

        while self._current_token().get('type') is not TokenType.END:
            parse_tree.append(self._expression(0))

        return parse_tree

    def _add_infix(self):
        self._infix(TokenType.POWER, 6, 5)
        self._infix(TokenType.DIVISION, 4)
        self._infix(TokenType.MOD, 4)
        self._infix(TokenType.PLUS, 3)
        self._infix(TokenType.MINUS, 3)
        self._infix(TokenType.ASSIGN, 1, 2, self._euqlas_evaluator)

    def _add_prefix(self):
        self._prefix(TokenType.MINUS, 7)

    def _add_symbols(self):
        self._symbol(TokenType.COMMA)
        self._symbol(TokenType.R_PAREN)
        self._symbol(TokenType.END)

        self._symbol(TokenType.NUMBER, lambda number: number)
        self._symbol(TokenType.L_PAREN, self._lparen_evaluator)
        self._symbol(TokenType.IDENTIFIER, self._identifier_evaluator)

    def _lparen_evaluator(self):
        value = self._expression(2)
        token = self._current_token()
        if token.get('type') is not TokenType.R_PAREN:
            raise ValueError('Unexpected token', token.get('type'))

        self._advance()
        return value

    def _identifier_evaluator(self, name):
        token = self._current_token()
        args = []

        if token.get('type') is TokenType.L_PAREN:
            next_token = self.tokens[self.workingIndex + 1]

            if next_token.get('type') is TokenType.R_PAREN:
                self._advance()
            else:
                while next_token.get('type') is TokenType.COMMA:
                    self._advance()
                    next_token = self._current_token()
                    args.append(self._expression(2))

                if next_token is not TokenType.R_PAREN:
                    raise ValueError('Unexpected token', next_token.get('type'))

        self._advance()

        return {
            'type': TokenType.CALL,
            'args': args,
            'name': name
        }

    def _euqlas_evaluator(self, left):
        left_type = left.get('type')

        if left_type is TokenType.CALL:
            for arg in left.get('args'):
                if arg.get('type') is not TokenType.IDENTIFIER:
                    raise ValueError('Invalid argument name', arg.get('type'))

            return {
                'type': TokenType.FUNCTION,
                'name': left.get('name'),
                'args': left.get('args'),
                'value': self._expression(2)
            }
        elif left_type is TokenType.IDENTIFIER:
            return {
                'type': TokenType.ASSIGN,
                'name': left.get('value'),
                'value': self._expression(2)
            }
        else:
            raise ValueError('Invalid lvalue')

    def _symbol(self, key, nud=None, lbp=None, led=None):
        sym = self.symbols.get(key)
        if sym is None:
            sym = {}

        self.symbols[key] = {
            'nud': 'nud' in sym and sym['nud'] or nud,
            'lbp': 'lbp' in sym and sym['lbp'] or lbp,
            'led': 'led' in sym and sym['led'] or led
        }

    def _interpret_token(self, token):
        sym = self.symbols.get(token.get('type'))

        if sym is None:
            sym = {}

        sym['type'] = token.get('type')
        sym['value'] = token.get('value')

        return sym

    def _current_token(self):
        return self._interpret_token(self.tokens[self.workingIndex])

    def _advance(self):
        self.workingIndex += 1
        return self._current_token()

    def _expression(self, rbp):
        token = self._current_token()
        self._advance()

        if 'nud' not in token: raise ValueError('Unexpected token', token)

        left = token.get('nud')(token)

        while self._current_token().get('lbp') is not None and (rbp < self._current_token().get('lbp')):
            token = self._current_token()
            self._advance()

            if 'led' not in token: raise ValueError('Unexpected token', token)

            left = token.get('led')(left)

        return left

    def _infix(self, key, lbp=None, rbp=None, led=None):
        rbp = rbp is not None and rbp or lbp
        led = led is not None and led or (lambda left: {
            'type': key,
            'left': left,
            'right': self._expression(rbp)
        })
        self._symbol(key, None, lbp, led)

    def _prefix(self, key, rbp=None):
        self._symbol(key, lambda: {'type': key, 'right': self._expression(rbp)})
