from TokenType import TokenType


# Class representing a Token
class Token:
    # Attributes of a Token
    type: TokenType
    lexeme: str
    literal: object
    line: int

    # Constructor for Token
    def __init__(self, type: TokenType, lexeme: str, literal: object, line: int):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    # String representation of Token
    def __str__(self):
        return str(self.type.name) + " " + self.lexeme + " " + str(self.literal)
