import sys
import os
import io
from Token import Token
from typing import List

had_error = False


def main():
    try:
        arg_len = len(sys.argv)
        if arg_len > 2:
            print("Usage: python lox.py [script]")
            exit()
        elif arg_len == 2:
            run_file(sys.argv[1])
        else:
            run_prompt()
    except IOError as e:
        print(e)


def run_file(path: str):
    try:
        with open(path, "rb") as file:
            byte_content = file.read()

        string_content = byte_content.decode(os.device_encoding(0) or "utf-8")

        run(string_content)
        global had_error

        if had_error:
            exit()
    except IOError as e:
        print(e)


def run_prompt():
    try:
        while True:
            line = input("> ")
            if line == None:
                break
            run(line)
            hadError = False
    except (IOError, KeyboardInterrupt) as e:
        print(e)


def run(source: str):
    tokens: List[Token]
    for item in source:
        print(item)


def error(line: int, message: str):
    report(line, "", message)


def report(line: int, where: str, message: str):
    print("[line " + str(line) + "] Error" + where + ": " + message)
    global had_error
    had_error = True


if __name__ == "__main__":
    main()
