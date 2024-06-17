from TokenType import TokenType
from typing import List, Dict, Optional
from Token import Token
from error import error


class Scanner:

    # Defining class attributes
    __source: str
    __tokens: List[Token] = list()
    __keywords: Dict[str, TokenType] = {
        "and": TokenType.AND,
        "class": TokenType.CLASS,
        "else": TokenType.ELSE,
        "false": TokenType.FALSE,
        "for": TokenType.FOR,
        "fun": TokenType.FUN,
        "if": TokenType.IF,
        "nil": TokenType.NIL,
        "or": TokenType.OR,
        "print": TokenType.PRINT,
        "return": TokenType.RETURN,
        "super": TokenType.SUPER,
        "this": TokenType.THIS,
        "true": TokenType.TRUE,
        "var": TokenType.VAR,
        "while": TokenType.WHILE,
    }

    __start: int = 0
    __current: int = 0
    __line: int = 1

    def __init__(self, source: str):
        # Initializing the source code to the variable
        self.__source = source

    # Returns list of tokens for main file access.
    def scan_tokens(self) -> List[Token]:
        # Iterate through characters to create tokens using scan_token, updating __start to __current
        while not self.is_at_end():
            self.__start = self.__current
            self.scan_token()

        # Add EOF token at the end of tokens list and return the list
        new_token = Token(TokenType.EOF, "", None, self.__line)
        self.__tokens.append(new_token)
        return self.__tokens

    # This is a function to know if we are at the end of the file.
    def is_at_end(self) -> bool:
        return self.__current >= len(self.__source)

    # Scans individual tokens and assigns type and literal
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
                elif self.match("*"):
                    while (
                        self.peek() != "*" and self.peek_next != "/"
                    ) and not self.is_at_end():
                        self.advance()
                    if not self.is_at_end():
                        self.advance()
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

            # string literals
            case '"':
                self.string()

            # if the char is not in any of the above, call the error function
            case _:
                if self.is_digit(c):
                    self.number()
                elif self.is_alpha(c):
                    self.identifier()
                else:
                    error(self.__line, "Unexpected character.")

    # advances __current to the next value and returns the current char
    def advance(self) -> str:
        char = self.__source[self.__current]
        self.__current = self.__current + 1
        return char

    # Adds a new token to the tokens list with type, lexeme, literal, and line number
    def add_token(self, type: TokenType, literal: Optional[str | float] = None) -> None:
        text: str = self.__source[self.__start : self.__current]
        new_token = Token(type, text, literal, self.__line)
        self.__tokens.append(new_token)

    # Increment __current if char matches expected, return true; otherwise, return false.
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

    # scans string and add the token along with the literal value to the list
    def string(self) -> None:

        # advances till reach the end of string or file
        while self.peek() != '"' and not self.is_at_end():
            # update line number
            if self.peek() == "\n":
                self.__line = self.__line + 1
            self.advance()

        # throws error if string is not terminated
        if self.is_at_end():
            error(self.__line, "Unterminated string.")
            return

        # advances to the next character
        self.advance()

        # takes the literal string value and add it to the token
        value: str = self.__source[self.__start + 1 : self.__current - 1]
        self.add_token(TokenType.STRING, value)

    # checks if the char is between 0 and 9
    def is_digit(self, c: str) -> bool:
        return c >= "0" and c <= "9"

    def number(self) -> None:
        # advances if the current char is digit
        while self.is_digit(self.peek()):
            self.advance()

        # look for a fractional part
        if self.peek() == "." and self.is_digit(self.peek_next()):
            # Consume the "."
            self.advance()

            # advances if the current char is digit
            while self.is_digit(self.peek()):
                self.advance()
        # adds float type with the literal value
        self.add_token(
            TokenType.NUMBER, float(self.__source[self.__start : self.__current])
        )

    # peeks at the next char
    def peek_next(self) -> str:
        # checks if it is end of the file
        if self.__current + 1 >= len(self.__source):
            return "\0"
        # returns the next char
        return self.__source[self.__current + 1]

    # returns true if the char is a-z,A-Z,_
    def is_alpha(self, c: str) -> bool:
        return (c >= "a" and c <= "z") or (c >= "A" and c <= "Z") or c == "_"

    # scans and add identifier to the list
    def identifier(self):
        # advances if the current char is alpha numeric
        while self.is_alpha_numeric(self.peek()):
            self.advance()

        # get the text and check if it is a keyword or else it will be an identifier
        text: str = self.__source[self.__start : self.__current]
        type: TokenType = self.__keywords.get(text, TokenType.IDENTIFIER)

        # adds token to the list
        self.add_token(type)

    # checks if the char is alpha or numeric
    def is_alpha_numeric(self, c: str) -> bool:
        return self.is_alpha(c) or self.is_digit(c)
