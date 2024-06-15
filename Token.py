from TokenType import TokenType


class Token:
    type: TokenType
    lexeme: str
    literal: object
    line: int

    def __init__(self, type: TokenType, lexeme: str, literal: object, line: int):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        return str(self.type.name) + " " + self.lexeme + " " + str(self.literal)
