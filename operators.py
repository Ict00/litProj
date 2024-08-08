import builtins
import time

from utils import out_error, operator, Token
from executor import *
import executor


@operator
def declare(index: int, args: list[Token]):
    if expect(args[0], "Identifier", index):
        if not executor.GlMemory.mem.__contains__(args[0].content):
            executor.GlMemory.mem[args[0].content] = []
        else:
            out_error(f"Memory stack with name '{args[0].content}' was already declared", index)
            quit(1)
    return index, 0


@operator
def sleep(index: int, args: list[Token]):
    if expect(args[0], "Number", index):
        time.sleep(int(args[0].content))
    return index, 0


@operator
def tpop(index: int, args: list[Token]):
    if args[0].content == "ALL":
        for i in executor.GlMemory.mem[executor.CurrentMemory].__len__():
            executor.GlMemory.temp.append(executor.GlMemory.mem[executor.CurrentMemory].pop(i))
    else:
        for i in args:
            expect(i, "Number", index)
            executor.GlMemory.temp.append(executor.GlMemory.mem[executor.CurrentMemory].pop(int(i.content)))
    return index, 0


@operator
def pull(index: int, args: list[Token]):
    if args[0].content == "ALL":
        for i in executor.GlMemory.mem[executor.CurrentMemory]:
            executor.GlMemory.temp.append(i)
    else:
        for i in args:
            expect(i, "Number", index)
            executor.GlMemory.temp.append(executor.GlMemory.mem[executor.CurrentMemory][int(i.content)])
    return index, 0


@operator
def add(index: int, args: list[Token]):
    expect(args[0], "Number", index)
    expect(args[1], "Number", index)
    val1 = executor.GlMemory.temp.pop(int(args[0].content))
    val2 = executor.GlMemory.temp.pop(int(args[1].content) - 1)
    res = val1 + val2
    executor.GlMemory.temp.append(res)
    return index, 0


@operator
def sub(index: int, args: list[Token]):
    expect(args[0], "Number", index)
    expect(args[1], "Number", index)
    val1 = executor.GlMemory.temp.pop(int(args[0].content))
    val2 = executor.GlMemory.temp.pop(int(args[1].content) - 1)
    res = val1 - val2
    executor.GlMemory.temp.append(res)
    return index, 0


@operator
def mul(index: int, args: list[Token]):
    expect(args[0], "Number", index)
    expect(args[1], "Number", index)
    val1 = executor.GlMemory.temp.pop(int(args[0].content))
    val2 = executor.GlMemory.temp.pop(int(args[1].content) - 1)
    res = val1 * val2
    executor.GlMemory.temp.append(res)
    return index, 0


@operator
def div(index: int, args: list[Token]):
    expect(args[0], "Number", index)
    expect(args[1], "Number", index)
    val1 = executor.GlMemory.temp.pop(int(args[0].content))
    val2 = executor.GlMemory.temp.pop(int(args[1].content) - 1)
    if val2 == 0:
        out_error("Can't divide by zero", index)
        quit(0)
    res = val1 / val2
    executor.GlMemory.temp.append(res)
    return index, 0


@operator
def mod(index: int, args: list[Token]):
    expect(args[0], "Number", index)
    expect(args[1], "Number", index)
    val1 = executor.GlMemory.temp.pop(int(args[0].content))
    val2 = executor.GlMemory.temp.pop(int(args[1].content) - 1)
    if val2 == 0:
        out_error("Can't divide by zero", index)
        quit(0)
    res = val1 % val2
    executor.GlMemory.temp.append(res)
    return index, 0


@operator
def inp(index: int, args: list[Token]):
    if args.__len__() != 0:
        expect(args[0], "String", index)
        val = input(args[0].content)
    else:
        val = input()
    try:
        executor.GlMemory.temp.append(int(val))
    except:
        for c in val:
            executor.GlMemory.temp.append(int(c.encode()[0]))
    return index, 0


@operator
def mergewith(index: int, args: list[Token]):
    expect(args[0], "Identifier", index)
    expect(args[1], "Identifier", index)
    mem1 = args[0].content.replace("THIS", executor.CurrentMemory)
    mem2 = args[1].content.replace("THIS", executor.CurrentMemory)
    if mem_exist(mem1, index) and mem_exist(mem2, index):
        for i in range(0, executor.GlMemory.mem[mem1].__len__()):
            try:
                executor.GlMemory.mem[mem2][i] = executor.GlMemory.mem[mem1][i]
            except:
                executor.GlMemory.mem[mem2].append(executor.GlMemory.mem[mem1][i])
    return index, 0


@operator
def rawmergewith(index: int, args: list[Token]):
    expect(args[0], "Identifier", index)
    expect(args[1], "Identifier", index)
    mem1 = args[0].content.replace("THIS", executor.CurrentMemory)
    mem2 = args[1].content.replace("THIS", executor.CurrentMemory)
    if mem_exist(mem1, index) and mem_exist(mem2, index):
        for i in range(0, executor.GlMemory.mem[mem1].__len__()):
            try:
                executor.GlMemory.mem[mem2][i] = executor.GlMemory.mem[mem1][i]
            except:
                executor.GlMemory.mem[mem2].append(executor.GlMemory.mem[mem1][i])
        executor.GlMemory.mem[mem1] = []
    return index, 0


@operator
def mforward(index: int, args: list[Token]):
    if args[1].content != "ALL":
        expect(args[0], "Identifier", index)
        if mem_exist(args[0].content, index):
            for b in range(1, args.__len__()):
                i = args[b]
                expect(i, "Number", index)
                executor.GlMemory.mem[args[0].content].append(
                    executor.GlMemory.mem[executor.CurrentMemory].pop(int(i.content)))
    else:
        expect(args[0], "Identifier", index)
        if mem_exist(args[0].content, index):
            for i in executor.GlMemory.mem[executor.CurrentMemory]:
                executor.GlMemory.mem[args[0].content].append(i)
    return index, 0


@operator
def forward(index: int, args: list[Token]):
    if args[1].content != "ALL":
        expect(args[0], "Identifier", index)
        if mem_exist(args[0].content, index):
            for b in range(1, args.__len__()):
                i = args[b]
                expect(i, "Number", index)
                executor.GlMemory.mem[args[0].content].append(executor.GlMemory.temp[(int(i.content))])
    else:
        expect(args[0], "Identifier", index)
        if mem_exist(args[0].content, index):
            for i in executor.GlMemory.temp:
                executor.GlMemory.mem[args[0].content].append(i)
    return index, 0


@operator
def push(index: int, args: list[Token]):
    if args[0].content == "SOFT":
        for b in range(1, args.__len__()):
            i = args[b]
            expect(i, "Number", index)
            executor.GlMemory.mem[executor.CurrentMemory].append(executor.GlMemory.temp[int(i.content)])
        pass
    elif args[0].content != "ALL":
        for i in args:
            expect(i, "Number", index)
            executor.GlMemory.mem[executor.CurrentMemory].append(executor.GlMemory.temp.pop(int(i.content)))
    else:
        for i in executor.GlMemory.temp:
            executor.GlMemory.mem[executor.CurrentMemory].append(i)
    return index, 0


@operator
def cloneto(index: int, args: list[Token]):
    expect(args[0], "Identifier", index)
    expect(args[1], "Identifier", index)
    mem1 = args[0].content.replace("THIS", executor.CurrentMemory)
    mem2 = args[1].content.replace("THIS", executor.CurrentMemory)
    if mem_exist(mem1, index) and mem_exist(mem2, index):
        executor.GlMemory.mem[mem2] = executor.GlMemory.mem[mem1].copy()
    return index, 0


@operator
def tdel(index: int, args: list[Token]):
    if args[0].content != "ALL":
        for i in args:
            expect(i, "Number", index)
            try:
                executor.GlMemory.temp[i.content] = 0
            except:
                out_error("Tried to clear out of memory", index)
                quit(1)
    else:
        executor.GlMemory.temp = []
    return index, 0


@operator
def mdel(index: int, args: list[Token]):
    if args[0].content != "ALL":
        for i in args:
            expect(i, "Number", index)
            try:
                executor.GlMemory.mem[executor.CurrentMemory][i.content] = 0
            except:
                out_error("Tried to clear out of memory", index)
                quit(1)
    else:
        executor.GlMemory.mem[executor.CurrentMemory] = []
    return index, 0


@operator
def ddel(index: int, args: list[Token]):
    expect(args[0], "Identifier", index)
    mem = args[0].content.replace("THIS", executor.CurrentMemory)
    if mem_exist(mem, index) and mem != executor.CurrentMemory:
        executor.GlMemory.mem.__delitem__(mem)
    else:
        out_error(f"Tried deleting memory stack '{mem}', which is being executed", index)
        quit(1)
    return index, 0


@operator
def writestr(index: int, args: list[Token]):
    if expect(args[0], "String", index):
        for character in args[0].content:
            executor.GlMemory.temp.append(int(character.encode()[0]))
    return index, 0


@operator
def mark(index: int, args: list[Token]):
    return index, 0


@operator
def pair(index: int, args: list[Token]):
    for i in args:
        expect(i, "Number", index)
    if args.__len__() % 2 != 0:
        out_error("Odd number of arguments", index)
        quit(1)
    else:
        for i in range(0, int(args.__len__()/2)):

            executor.GlMemory.temp.insert(i, int(args[int(args.__len__()/2)+i].content))
    return index, 0


@operator
def writenum(index: int, args: list[Token]):
    for i in args:
        expect(i, "Number", index)
        executor.GlMemory.temp.append(int(i.content))
    return index, 0


@operator
def pycall(index: int, args: list[Token]):
    expect(args[0], "String", index)
    cmd = args[0].content
    try:
        result = eval(cmd)
        if result is not None:
            if isinstance(result, list):
                for i in result:
                    try:
                        executor.GlMemory.temp.append(int(i))
                    except:
                        try:
                            executor.GlMemory.temp.append(int(i.encode()[0]))
                        except:
                            try:
                                if i:
                                    executor.GlMemory.temp.append(1)
                                else:
                                    executor.GlMemory.temp.append(0)
                            except:
                                executor.GlMemory.temp.append(0)
            elif isinstance(result, dict):
                for i in list(result.values()):
                    try:
                        executor.GlMemory.temp.append(int(i))
                    except:
                        try:
                            executor.GlMemory.temp.append(int(i.encode()[0]))
                        except:
                            try:
                                if i:
                                    executor.GlMemory.temp.append(1)
                                else:
                                    executor.GlMemory.temp.append(0)
                            except:
                                executor.GlMemory.temp.append(0)
            elif isinstance(result, int):
                executor.GlMemory.temp.append(result)
            elif isinstance(result, str):
                for i in result:
                    executor.GlMemory.temp.append(int(i.encode()[0]))
            elif isinstance(result, range):
                for i in result:
                    executor.GlMemory.temp.append(i)
            else:
                out_error("pycall: return value is not supported", index)
                quit(1)
    except:
        out_error("pycall: something went wrong", index)
        quit(1)
    return index, 0


@operator
def equit(index: int, args: list[Token]):
    quit(0)


@operator
def lif(index: int, args: list[Token]):
    expect(args[0], "Number", index)
    val = executor.GlMemory.temp.pop(int(args[0].content))
    if val == 0:
        index += 1
    return index, 0


@operator
def l_not(index: int, args: list[Token]):
    expect(args[0], "Number", index)
    a = executor.GlMemory.temp.pop(int(args[0].content))
    executor.GlMemory.temp.append(0 if a == 1 else 1)
    return index, 0


@operator
def str_eq(index: int, args: list[Token]):
    expect(args[0], "Number", index)
    expect(args[1], "String", index)
    a, b = int(args[0].content), args[1].content
    for i in range(0, b.__len__()):
        try:
            var = executor.GlMemory.mem[executor.CurrentMemory][a]
            if var != int(b.encode()[i]):
                executor.GlMemory.temp.append(0)
                return index, 0
            a += 1
        except:
            executor.GlMemory.temp.append(0)
            return index, 0
    executor.GlMemory.temp.append(1)
    return index, 0


@operator
def str_noteq(index: int, args: list[Token]):
    expect(args[0], "Number", index)
    expect(args[1], "String", index)
    a, b = int(args[0].content), args[1].content
    for i in range(0, b.__len__()):
        try:
            var = executor.GlMemory.mem[executor.CurrentMemory][a]
            if var == int(b.encode()[i]):
                executor.GlMemory.temp.append(0)
                return index, 0
            a += 1
        except:
            executor.GlMemory.temp.append(0)
            return index, 0
    executor.GlMemory.temp.append(1)
    return index, 0


@operator
def l_eq(index: int, args: list[Token]):
    expect(args[0], "Number", index)
    expect(args[1], "Number", index)
    a, b = executor.GlMemory.temp.pop(int(args[0].content)), executor.GlMemory.temp.pop(int(args[1].content) - 1)
    executor.GlMemory.temp.append(1 if a == b else 0)
    return index, 0


@operator
def l_noteq(index: int, args: list[Token]):
    expect(args[0], "Number", index)
    expect(args[1], "Number", index)
    a, b = executor.GlMemory.temp.pop(int(args[0].content)), executor.GlMemory.temp.pop(int(args[1].content) - 1)
    executor.GlMemory.temp.append(1 if a != b else 0)
    return index, 0


@operator
def l_greater(index: int, args: list[Token]):
    expect(args[0], "Number", index)
    expect(args[1], "Number", index)
    a, b = executor.GlMemory.temp.pop(int(args[0].content)), executor.GlMemory.temp.pop(int(args[1].content) - 1)
    executor.GlMemory.temp.append(1 if a > b else 0)
    return index, 0


@operator
def l_lesser(index: int, args: list[Token]):
    expect(args[0], "Number", index)
    expect(args[1], "Number", index)
    a, b = executor.GlMemory.temp.pop(int(args[0].content)), executor.GlMemory.temp.pop(int(args[1].content) - 1)
    executor.GlMemory.temp.append(1 if a < b else 0)
    return index, 0


@operator
def l_lesseq(index: int, args: list[Token]):
    expect(args[0], "Number", index)
    expect(args[1], "Number", index)
    a, b = executor.GlMemory.temp.pop(int(args[0].content)), executor.GlMemory.temp.pop(int(args[1].content) - 1)
    executor.GlMemory.temp.append(1 if a <= b else 0)
    return index, 0


@operator
def l_greatereq(index: int, args: list[Token]):
    expect(args[0], "Number", index)
    expect(args[1], "Number", index)
    a, b = executor.GlMemory.temp.pop(int(args[0].content)), executor.GlMemory.temp.pop(int(args[1].content) - 1)
    executor.GlMemory.temp.append(1 if a >= b else 0)
    return index, 0


@operator
def goto(index: int, args: list[Token]):
    expect(args[0], "Number", index)
    return int(args[0].content)-1, 0


@operator
def use(index: int, args: list[Token]):
    if expect(args[0], "Identifier", index):
        if executor.GlMemory.mem.__contains__(args[0].content):
            executor.CurrentMemory = args[0].content
        else:
            out_error(f"Memory stack with name '{args[0].content}' was not declared", index)
    return index, 0
