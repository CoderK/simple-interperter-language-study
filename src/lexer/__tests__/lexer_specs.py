import unittest

from src.lexer.lexer import lex
from src.lexer.token_table import token_table
from src.enums.token_type import TokenType


class TestLexer(unittest.TestCase):

    def test_문자_입력_값에서_연산자_토큰을_추출할_수_있다(self):
        self.assertEqual(lex('-'), [{'type': token_table['-']}])
        self.assertEqual(lex('+'), [{'type': token_table['+']}])
        self.assertEqual(lex('*'), [{'type': token_table['*']}])
        self.assertEqual(lex('/'), [{'type': token_table['/']}])
        self.assertEqual(lex('%'), [{'type': token_table['%']}])
        self.assertEqual(lex('^'), [{'type': token_table['^']}])
        self.assertEqual(lex('('), [{'type': token_table['(']}])
        self.assertEqual(lex(')'), [{'type': token_table[')']}])
        self.assertEqual(lex(''), [])

    def test_문자열_입력_값에서_숫자_토큰을_추출할_수_있다(self):
        self.assertEqual(lex('90'), [
            {'type': TokenType.NUMBER, 'value': 90}
        ])

    def test_숫자나_연산자가_아닌_모든_토큰은_식별자로_취급해야_한다(self):
        self.assertEqual(lex('abc'), [
            {'type': TokenType.IDENTIFIER, 'value': 'abc'},
        ])

    def test_입력한_문자열을_어휘분석하여_토큰_정보를_배열로_추출할_수_있다(self):
        self.assertEqual(lex('abc-+90/'), [
            {'type': TokenType.IDENTIFIER, 'value': 'abc'},
            {'type': token_table['-']},
            {'type': token_table['+']},
            {'type': TokenType.NUMBER, 'value': 90},
            {'type': token_table['/']},
        ])

    def test_토큰정보를_추출할_때_토큰_사이의_공백은_무시해야_한다(self):
        self.assertEqual(lex('abc-    +  90  /'), [
            {'type': TokenType.IDENTIFIER, 'value': 'abc'},
            {'type': token_table['-']},
            {'type': token_table['+']},
            {'type': TokenType.NUMBER, 'value': 90},
            {'type': token_table['/']}
        ])


if __name__ == '__main__':
    unittest.main()
