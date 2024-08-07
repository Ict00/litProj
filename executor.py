import json

from utils import *
from operators import *
GlMemory = Memory()
CurrentMemory = "main"


def pre_execute(to_execute: str) -> dict:
    app = json.loads(to_execute)
    temp_app: dict = app["app"]
    new_app = {}
    for key in temp_app.keys():
        new_app[key] = []
        for token in temp_app[key]:
            new_app[key].append(token_from_simple(token))
    return new_app


def execute(to_execute: str) -> int:
    to_execute = pre_execute(to_execute)
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