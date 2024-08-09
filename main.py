import datetime
import json
import os.path
import sys
import time

import executor
from lexer import *
from builder import *
from executor import *
from operators import *

operation = ""
arg = []

args = sys.argv

for b in range(1, args.__len__()):
    i = args[b]
    match i:
        case "-b":
            operation = "build"
        case "-r":
            operation = "run"
        case "-c":
            operation = "combine"
        case "-d":
            operation = "debug"
        case "-l":
            operation = "link"
        case _: arg.append(i)
if operation != "build" and operation != "run" and operation != "combine" and operation != "debug" and operation != "link":
    print("\x1b[1;38;5;196mError Occured:\x1b[0m\x1b[1m Unknown operation\x1b[0m")
    quit(-1)


for i in arg:
    if not os.path.isfile(i):
        print(args)
        print("\x1b[1;38;5;196mError Occured:\x1b[0m\x1b[1m Invalid arguments\x1b[0m")
        quit(-1)


match operation:
        case "run":
            execute(open(arg[0]).read(), "app")
        case "debug":
            execute(simple_build(lex2(lex1(prelex(open(arg[0]).read())))), "app")
        case "build":
            for i in arg:
                before = datetime.datetime.now()
                filename = f"{i.replace(os.path.splitext(i)[1], "")}.json"
                try:
                    open(filename, "x").close()
                except:
                    pass
                open(filename, "w").write(simple_build(lex2(lex1(prelex(open(i).read())))))
                got = datetime.datetime.now() - before

                print(f"\x1b[1;38;5;148mBUILT SUCCESSFULLY IN {got.microseconds}ms\x1b[0m")
        case "combine":
            for i in arg:
                filename = f"{i.replace(os.path.splitext(i)[1], "")}.json"
                try:
                    open(filename, "x").close()
                except:
                    pass
                built = simple_build(lex2(lex1(prelex(open(i).read()))))
                open(filename, "w").write(built)
                execute(built, "app")
        case "link":
            try:
                root = json.loads(open(arg[0]).read())
                for b in range(1, arg.__len__()):
                    i = arg[b]
                    sector_name = i.replace(os.path.splitext(i)[1], "")
                    sector = dict(json.loads(open(i).read()))
                    root[sector_name] = sector["app"]
                open(arg[0], "w").write(json.dumps(root))
                for b in range(1, arg.__len__()):
                    os.remove(arg[b])
                print(f"\x1b[1;38;5;148mLINKED SUCCESSFULLY\x1b[0m")
            except:
                print(args)
                print("\x1b[1;38;5;196mError Occured:\x1b[0m\x1b[1m Invalid arguments\x1b[0m")
                quit(-1)