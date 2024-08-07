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
    val2 = executor.GlMemory.temp.pop(int(args[1].content)-1)
    res = val1 + val2
    executor.GlMemory.temp.append(res)
    return index, 0


@operator
def sub(index: int, args: list[Token]):
    expect(args[0], "Number", index)
    expect(args[1], "Number", index)
    val1 = executor.GlMemory.temp.pop(int(args[0].content))
    val2 = executor.GlMemory.temp.pop(int(args[1].content)-1)
    res = val1 - val2
    executor.GlMemory.temp.append(res)
    return index, 0


@operator
def mul(index: int, args: list[Token]):
    expect(args[0], "Number", index)
    expect(args[1], "Number", index)
    val1 = executor.GlMemory.temp.pop(int(args[0].content))
    val2 = executor.GlMemory.temp.pop(int(args[1].content)-1)
    res = val1 * val2
    executor.GlMemory.temp.append(res)
    return index, 0


@operator
def div(index: int, args: list[Token]):
    expect(args[0], "Number", index)
    expect(args[1], "Number", index)
    val1 = executor.GlMemory.temp.pop(int(args[0].content))
    val2 = executor.GlMemory.temp.pop(int(args[1].content)-1)
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
    val2 = executor.GlMemory.temp.pop(int(args[1].content)-1)
    if val2 == 0:
        out_error("Can't divide by zero", index)
        quit(0)
    res = val1 % val2
    executor.GlMemory.temp.append(res)
    return index, 0


@operator
def inp(index: int, args: list[Token]):
    expect(args[0], "String", index)
    val = input(args[0].content)
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
    mem1 = args[0].content
    mem2 = args[1].content
    if mem1 == "THIS":
        mem1 = executor.CurrentMemory
    if mem2 == "THIS":
        mem2 = executor.CurrentMemory
    if mem_exist(mem1, index) and mem_exist(mem2, index):
        for i in range(0, executor.GlMemory.mem[mem1].__len__()):
            try:
                executor.GlMemory.mem[mem2][i] = executor.GlMemory.mem[mem1][i]
            except:
                executor.GlMemory.mem[mem2].append(executor.GlMemory.mem[mem1][i])
        executor.GlMemory.mem[mem2] = []
    return index, 0


@operator
def forward(index: int, args: list[Token]):
    if args[1].content != "ALL":
        expect(args[0], "Identifier", index)
        if mem_exist(args[0].content, index):
            for b in range(1, args.__len__()):
                i = args[b]
                expect(i, "Number", index)
                executor.GlMemory.mem[args[0].content].append(executor.GlMemory.temp.pop(int(i.content)))
    else:
        expect(args[0], "Identifier", index)
        if mem_exist(args[0].content, index):
            for i in executor.GlMemory.temp:
                executor.GlMemory.mem[args[0].content].append(i)
    return index, 0


@operator
def push(index: int, args: list[Token]):
    if args[0].content != "ALL":
        for i in args:
            expect(i, "Number", index)
            executor.GlMemory.mem[executor.CurrentMemory].append(executor.GlMemory.temp.pop(int(i.content)))
    else:
        for i in executor.GlMemory.temp:
            executor.GlMemory.mem[executor.CurrentMemory].append(i)
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
def writenum(index: int, args: list[Token]):
    for i in args:
        expect(i, "Number", index)
        executor.GlMemory.temp.append(int(i.content))
    return index, 0


@operator
def l_not(index: int, args: list[Token]):
    expect(args[0], "Number", index)
    a = executor.GlMemory.temp.pop(int(args[0].content))
    executor.GlMemory.temp.append(0 if a == 1 else 1)
    return index, 0


@operator
def l_eq(index: int, args: list[Token]):
    expect(args[0], "Number", index)
    expect(args[1], "Number", index)
    a, b = executor.GlMemory.temp.pop(int(args[0].content)), executor.GlMemory.temp.pop(int(args[1].content)-1)
    executor.GlMemory.temp.append(1 if a == b else 0)
    return index, 0


@operator
def l_noteq(index: int, args: list[Token]):
    expect(args[0], "Number", index)
    expect(args[1], "Number", index)
    a, b = executor.GlMemory.temp.pop(int(args[0].content)), executor.GlMemory.temp.pop(int(args[1].content)-1)
    executor.GlMemory.temp.append(1 if a != b else 0)
    return index, 0


@operator
def l_greater(index: int, args: list[Token]):
    expect(args[0], "Number", index)
    expect(args[1], "Number", index)
    a, b = executor.GlMemory.temp.pop(int(args[0].content)), executor.GlMemory.temp.pop(int(args[1].content)-1)
    executor.GlMemory.temp.append(1 if a > b else 0)
    return index, 0


@operator
def l_lesser(index: int, args: list[Token]):
    expect(args[0], "Number", index)
    expect(args[1], "Number", index)
    a, b = executor.GlMemory.temp.pop(int(args[0].content)), executor.GlMemory.temp.pop(int(args[1].content)-1)
    executor.GlMemory.temp.append(1 if a < b else 0)
    return index, 0


@operator
def l_lesseq(index: int, args: list[Token]):
    expect(args[0], "Number", index)
    expect(args[1], "Number", index)
    a, b = executor.GlMemory.temp.pop(int(args[0].content)), executor.GlMemory.temp.pop(int(args[1].content)-1)
    executor.GlMemory.temp.append(1 if a <= b else 0)
    return index, 0


@operator
def l_greatereq(index: int, args: list[Token]):
    expect(args[0], "Number", index)
    expect(args[1], "Number", index)
    a, b = executor.GlMemory.temp.pop(int(args[0].content)), executor.GlMemory.temp.pop(int(args[1].content)-1)
    executor.GlMemory.temp.append(1 if a >= b else 0)
    return index, 0



@operator
def goto(index: int, args: list[Token]):
    expect(args[0], "Number", index)
    return int(args[0].content), 0


@operator
def use(index: int, args: list[Token]):
    if expect(args[0], "Identifier", index):
        if executor.GlMemory.mem.__contains__(args[0].content):
            executor.CurrentMemory = args[0].content
        else:
            out_error(f"Memory stack with name '{args[0].content}' was not declared", index)
    return index, 0
