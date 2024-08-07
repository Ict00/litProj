from utils import out_error, operator
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
    res = executor.GlMemory.temp.pop(int(args[0].content)) + executor.GlMemory.temp.pop(int(args[1].content))
    executor.GlMemory.temp.append(res)
    return index, 0


@operator
def mergewith(index: int, args: list[Token]):
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
            executor.GlMemory.temp.append(character.encode())
    return index, 0


@operator
def writenum(index: int, args: list[Token]):
    for i in args:
        expect(i, "Number", index)
        executor.GlMemory.temp.append(int(i.content))
    return index, 0


@operator
def use(index: int, args: list[Token]):
    if expect(args[0], "Identifier", index):
        if executor.GlMemory.mem.__contains__(args[0].content):
            executor.CurrentMemory = args[0].content
        else:
            out_error(f"Memory stack with name '{args[0].content}' was not declared", index)
    return index, 0
