import executor
from lexer import *
from builder import *
from executor import *
from operators import *

e = lex2(lex1(prelex("write 1 5 num;0 == 1;forward outnum ALL")))

#for i in e:
#    print(f"{i.content} {i.type}")
execute(simple_build(e))

#print(executor.GlMemory.mem)