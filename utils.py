import executor

Operators = {}
PartialOperators = [
    "str", "num", "write", "push", "merge", "with", "rawmerge"
]
BuilderVersion = 1


class Memory:
    def __init__(self):
        self.mem = {
            "outstr": [],
            "outnum": [],
            "main": []
        }
        self.temp = []
    pass


class Token:
    def __init__(self, type: str, content: str):
        self.type = type
        self.content = content

    def to_json_compatible(self) -> dict:
        return {
            "type": self.type,
            "content": self.content
        }


def token_from_simple(content: str) -> Token:
    if content.endswith("#>_NUM"): return Token("Number", content.replace("#>_NUM", ""))
    if content.endswith("#>_STR"): return Token("String", content.replace("#>_STR", ""))
    return Token("Identifier", content)


def out_error(error: str, line: int):
    print(f"\x1b[1;38;5;196m| Error Occurred\x1b[0m: \x1b[1m{error}; line {line}\x1b[0m")


def expect(token: Token, type: str, line: int) -> bool:
    if token.type == type:
        return True
    else:
        out_error(f"Expected type '{type}', got '{token.type}'", line)
        quit(1)


def mem_exist(memory: str, index: int) -> bool:
    if executor.GlMemory.mem.__contains__(memory):
        return True
    else:
        out_error(f"Memory stack with name '{memory}' was not declared", index)
        quit(1)


def token_from_json(content: dict) -> Token:
    return Token(content["type"], content["content"])


def operator(_func = None):
    def decorator_operator(func):
        global Operators
        match func.__name__:
            case "l_not": Operators["!"] = func
            case "l_eq": Operators["=="] = func
            case "l_noteq": Operators["!="] = func
            case "l_greater": Operators[">"] = func
            case "l_lesser": Operators["<"] = func
            case "l_lesseq": Operators["<"] = func
            case "l_greatereq": Operators[">="] = func
            case _: Operators[func.__name__] = func
    decorator_operator(_func)


def transform_string(string: str) -> str:
    return (string
            .replace("\\r", "\r")
            .replace("\\n", "\n")
            .replace("\\x1b", "\x1b")
            .replace('\\"', '"'))


def token_to_str(token: Token) -> str:
    match token.type:
        case "String": return f"{token.content}#>_STR"
        case "Number": return f"{token.content}#>_NUM"
        case _: return token.content


def fast_tokenseq_to_str(tokens: list[dict]) -> str:
    result = ""
    for token in tokens:
        token = token_from_json(token)
        if token.type == "String":
            result += f'"{token.content}"'
        else:
            result += token.content
        result += " "
    return result


def simple_tokenseq_to_str(tokens: list[str]) -> str:
    result = ""
    for token in tokens:
        token = token_from_simple(token)
        if token.type == "String":
            result += f'"{token.content}"'
        else:
            result += token.content
        result += " "
    return result
