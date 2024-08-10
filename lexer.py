from utils import *


def prelex(_code: str) -> list:
    lines = []
    for i in _code.split("\n"):
        if not i.startswith("//"):
            lines.append(i)
    return lines


def lex1(lines: list[str]) -> list[Token]:
    result = []
    for line in range(0, lines.__len__()):
        next_token = ""
        writing_string = False
        for i in range(0, lines[line].__len__()):
            c = lines[line][i]
            match c:
                case '"':
                    if writing_string:
                        if lines[line][i-1] != '\\':
                            result.append(Token("String", next_token))
                            next_token = ""
                            writing_string = not writing_string
                        else:
                            next_token += c
                    else:
                        if next_token != "" and next_token != " " and next_token != "\r":
                            result.append(Token("Identifier", next_token))
                            next_token = ""
                        writing_string = True
                case ' ':
                    if not writing_string:
                        if next_token != "" and next_token != " " and next_token != "\r":
                            result.append(Token("Identifier", next_token))
                            next_token = ""
                    else:
                        next_token += " "
                case ';':
                    if not writing_string:
                        if next_token != "" and next_token != " " and next_token != "\r":
                            result.append(Token("Identifier", next_token))
                            next_token = ""
                        if result[result.__len__()-1].type != "Semicolon":
                            result.append(Token("Semicolon", ";"))
                case _:
                    next_token += c
        if next_token != "" and next_token != " " and next_token != "\r":
            if writing_string:
                result.append(Token("String", next_token))
            else:
                result.append(Token("Identifier", next_token))
        if result[result.__len__()-1].type != "Semicolon":
            result.append(Token("Semicolon", ";"))
    return result


def lex2(tokens: list[Token]) -> list[Token]:
    result = []
    for token in tokens:
        new_token = token
        if token.type != "String":
            if Operators.__contains__(token.content) or PartialOperators.__contains__(token.content):
                new_token.type = "Operator"
            else:
                try:
                    int(token.content)
                    new_token.type = "Number"
                except:
                    pass
        else:
            new_token.content = transform_string(token.content)
        result.append(new_token)
    return result
