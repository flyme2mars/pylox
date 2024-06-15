from TokenType import TokenType
from typing import List
from Token import Token


def error(line: int, message: str):
    report(line, "", message)


def report(line: int, where: str, message: str):
    print("[line " + str(line) + "] Error" + where + ": " + message)
    global had_error
    had_error = True


class Scanner:

    __source: str
    __tokens: List[Token] = list()

    __start: int = 0
    __current: int = 0
    __line: int = 1

    def __init__(self, source: str):
        self.__source = source

    def scan_tokens(self) -> List[Token]:
        while not self.is_at_end():
            self.__start = self.__current
            self.scan_token()

        new_token = Token(TokenType.EOF, "", None, self.__line)
        self.__tokens.append(new_token)
        return self.__tokens

    def is_at_end(self) -> bool:
        return self.__current >= len(self.__source)

    def scan_token(self) -> None:
        c: str = self.advance()
        match c:
            case "(":
                self.add_token(TokenType.LEFT_PAREN)
            case ")":
                self.add_token(TokenType.RIGHT_PAREN)
            case "{":
                self.add_token(TokenType.LEFT_BRACE)
            case "}":
                self.add_token(TokenType.RIGHT_BRACE)
            case ",":
                self.add_token(TokenType.COMMA)
            case ".":
                self.add_token(TokenType.DOT)
            case "-":
                self.add_token(TokenType.MINUS)
            case "+":
                self.add_token(TokenType.PLUS)
            case ";":
                self.add_token(TokenType.SEMICOLON)
            case "*":
                self.add_token(TokenType.STAR)
            case "!":
                self.add_token(
                    TokenType.BANG_EQUAL if self.match("=") else TokenType.BANG
                )
            case "=":
                self.add_token(
                    TokenType.EQUAL_EQUAL if self.match("=") else TokenType.EQUAL
                )
            case "<":
                self.add_token(
                    TokenType.LESS_EQUAL if self.match("=") else TokenType.LESS
                )
            case ">":
                self.add_token(
                    TokenType.GREATER_EQUAL if self.match("=") else TokenType.GREATER
                )
            case "/":
                if self.match("/"):
                    # A comment goes until the end of the line.
                    while self.peek() != "\n" and not self.is_at_end():
                        self.advance()
                else:
                    self.add_token(TokenType.SLASH)
            case " ":
                pass
            case "\r":
                pass
            case "\t":
                pass
            case "\n":
                self.__line = self.__line + 1
            case _:
                error(self.__line, "Unexpected character.")

    def peek(self) -> str:
        if self.is_at_end():
            return "\0"
        return self.__source[self.__current]

    def match(self, expected: str) -> bool:
        if self.is_at_end():
            return False
        if self.__source[self.__current] != expected:
            return False
        self.__current = self.__current + 1
        return True

    def advance(self) -> str:
        char = self.__source[self.__current]
        self.__current = self.__current + 1
        return char

    def add_token(self, type: TokenType, literal=None) -> None:
        text: str = self.__source[self.__start : self.__current]
        new_token = Token(type, text, literal, self.__line)
        self.__tokens.append(new_token)
