import unittest
from src.parser.parser import Parser
from src.enums.token_type import TokenType


class TestParser(unittest.TestCase):

    def test_걍_테스트(self):
        # given
        tokens = [
            {'type': TokenType.NUMBER, 'value': 12},
            {'type': TokenType.PLUS},
            {'type': TokenType.NUMBER, 'value': 4},
            {'type': TokenType.END}
        ]
        parser = Parser(tokens)

        # when
        parse_tree = parser.parse()
        print(parse_tree)

if __name__ == '__main__':
    unittest.main()
