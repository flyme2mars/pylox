def error(line: int, message: str):
    report(line, "", message)


def report(line: int, where: str, message: str):
    print("[line " + str(line) + "] Error" + where + ": " + message)
    global had_error
    had_error = True
