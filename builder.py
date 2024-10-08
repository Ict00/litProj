import json

import utils
from utils import Token, BuilderVersion, PartialOperators, token_to_str, Operators


def simple_build(tokens: list[Token]) -> str:
    result = \
        {
            "built_with": BuilderVersion
        }
    app = {}
    # Temporary
    operator = ""
    line = []
    cur_line = 0

    for i in range(0, tokens.__len__()):
        token = tokens[i]

        if token.type == "Operator":
            if operator != "":
                operator += token.content
            else:
                operator = f"{cur_line} {token.content}"
        elif token.type == "Semicolon":
            if operator != "":
                if Operators.__contains__(operator.split(" ")[1]):
                    app[operator] = line.copy()
                    line = []
                    operator = ""
                    cur_line += 1
                else:
                    utils.out_error(f"Operator '{operator.split(" ")[1]}' not found", cur_line)
                    quit(1)
            else:
                utils.out_error("No any operator", cur_line)
                quit(1)
        else:
            line.append(token_to_str(token))
        pass

    result["app"] = app
    return json.dumps(result)