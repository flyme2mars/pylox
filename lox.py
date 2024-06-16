# imports
import sys
import os
import io
from Token import Token
from typing import List
from Scanner import Scanner
import error

# global variable
had_error = False


# main function
def main():
    try:
        arg_len = len(sys.argv)
        # exit if more than an argument is passed
        if arg_len > 2:
            print("Usage: python lox.py [script]")
            exit()
        # run a file if the file name is passed
        elif arg_len == 2:
            run_file(sys.argv[1])
        # run the REPL if there is no file name
        else:
            run_prompt()
    # give error if IOError occur, like incorrect file name
    except IOError as e:
        print(e)


# Function to run a file
def run_file(path: str):
    try:
        with open(path, "rb") as file:
            byte_content = file.read()

        # Decode byte content to string
        string_content = byte_content.decode(os.device_encoding(0) or "utf-8")

        # Run the content
        run(string_content)
        global had_error

        # Exit if there was an error
        if had_error:
            exit()
    except IOError as e:
        print(e)


# Function to run the REPL prompt
def run_prompt():
    try:
        while True:
            line = input("> ")
            if line == None:
                break
            run(line)
            global had_error
            had_error = False
    except (IOError, KeyboardInterrupt) as e:
        print(e)


# Function to run the source code
def run(source: str):
    # Initialize the scanner with the provided source
    scanner: Scanner = Scanner(source)
    # Get the list of tokens by scanning the source
    tokens: List[Token] = scanner.scan_tokens()

    # Print each token
    for token in tokens:
        print(token)


# def error(line: int, message: str):
#     report(line, "", message)


# def report(line: int, where: str, message: str):
#     print("[line " + str(line) + "] Error" + where + ": " + message)
#     global had_error
#     had_error = True

# Run the main function if the script is executed directly
if __name__ == "__main__":
    main()
