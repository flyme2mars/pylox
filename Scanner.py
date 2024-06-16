from TokenType import TokenType
from typing import List
from Token import Token
from error import error


class Scanner:

    # Defining class attributes
    __source: str
    __tokens: List[Token] = list()

    __start: int = 0
    __current: int = 0
    __line: int = 1

    def __init__(self, source: str):
        # Initializing the source code to the variable
        self.__source = source

    # This function returns the list of all tokens and this can be accessed in the main file.
    def scan_tokens(self) -> List[Token]:
        # If not in the end of source code, go through each of the char and when we complete a token, add to the list using scan_token, then put __start to the __current value
        while not self.is_at_end():
            self.__start = self.__current
            self.scan_token()

        # When it is at the end, we need to put End Of File at the end of tokens list and finally return that list
        new_token = Token(TokenType.EOF, "", None, self.__line)
        self.__tokens.append(new_token)
        return self.__tokens

    # This is a function to know if we are at the end of the file.
    def is_at_end(self) -> bool:
        return self.__current >= len(self.__source)

    # This method is to scan every individual token and give its appropriate type and literal
    def scan_token(self) -> None:
        # We get the current character
        c: str = self.advance()

        # goes through each of the char
        match c:
            # single char token
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

            # for !=, ==, <= and >=
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

            # deals with comments and /(slash or division symbol)
            case "/":
                if self.match("/"):
                    # A comment goes until the end of the line.
                    while self.peek() != "\n" and not self.is_at_end():
                        self.advance()
                else:
                    self.add_token(TokenType.SLASH)

            # ignores white space
            case " ":
                pass
            case "\r":
                pass
            case "\t":
                pass

            # increment line number when new line char occur
            case "\n":
                self.__line = self.__line + 1

            # if the char is not in any of the above, call the error function
            case _:
                error(self.__line, "Unexpected character.")

    # advances __current to the next value and returns the current char
    def advance(self) -> str:
        char = self.__source[self.__current]
        self.__current = self.__current + 1
        return char

    # takes one or two arguments, the argument for literal is optional. then adds a new token to the tokes list with appropriate type, lexeme, literal and line number
    def add_token(self, type: TokenType, literal=None) -> None:
        text: str = self.__source[self.__start : self.__current]
        new_token = Token(type, text, literal, self.__line)
        self.__tokens.append(new_token)

    # returns true and increment __current if the current char is the expected one. returns false if it is at the end of the current char is not equal the the expected
    def match(self, expected: str) -> bool:
        if self.is_at_end():
            return False
        if self.__source[self.__current] != expected:
            return False
        self.__current = self.__current + 1
        return True

    # returns the current char when not at the end.
    def peek(self) -> str:
        if self.is_at_end():
            return "\0"
        return self.__source[self.__current]
