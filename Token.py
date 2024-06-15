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

    def to_string(self):
        return str(self.type.name) + " " + self.lexeme + " " + str(self.literal)


token = Token(TokenType.IDENTIFIER, "a_variable", None, 4)
print(token.to_string())
