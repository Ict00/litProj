import json

import builder
from utils import *
from operators import *
GlMemory = Memory()
CurrentMemory = "main"
Executing = ""


def pre_execute(to_execute: str, root: str) -> dict:
    try:
        app = json.loads(to_execute)
        version = app["built_with"]
        if version > builder.BuilderVersion:
            out_error("File is not supported", None)
            quit(1)
        if app.__contains__(root):
            temp_app: dict = app[root]
            new_app = {}
            for key in temp_app.keys():
                new_app[key] = []
                for token in temp_app[key]:
                    new_app[key].append(token_from_simple(token))
        else:
            out_error("File is not Lit-compatible", None)
            quit(1)
    except:
        out_error("File is not Lit-compatible", None)
        quit(1)
    return new_app


def execute(to_execute: str, root: str) -> int:
    global Executing
    Executing = to_execute
    to_execute = pre_execute(Executing, root)
    i = 0
    while i < to_execute.keys().__len__():
        key = list(to_execute.keys())[i]
        result = Operators[key.split(" ")[1]](i, to_execute[key])
        try:
            i = result[0]
        except:
            out_error(f"Tried to goto out of Execution List: {result[0]}", i)
            quit(1)
        for b in GlMemory.mem["outstr"]:
            print(b.to_bytes().decode(), end='')
        for b in GlMemory.mem["outnum"]:
            print(b, end='')
        GlMemory.mem["outnum"] = []
        GlMemory.mem["outstr"] = []
        i += 1
    return 0