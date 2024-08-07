import executor
from lexer import *
from builder import *
from executor import *
from operators import *

e = lex2(lex1(prelex("write 33 num;push ALL;merge THIS with outstr")))

#for i in e:
#    print(f"{i.content} {i.type}")
execute(simple_build(e))

#print(executor.GlMemory.mem)