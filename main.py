import executor
from lexer import *
from builder import *
from executor import *
from operators import *

e = lex2(lex1(prelex("write 0 num;forward outnum ALL;tdel ALL;0 1 pair 0 1;push SOFT 0;0 add 1;tpop 0;forward outnum 0;mdel ALL;goto 4")))
#for i in e:
#    print(f"{i.content} {i.type}")
execute(simple_build(e))

#print(executor.GlMemory.mem)

a = """
0 1 pair 0 1
forward outnum ALL
push SOFT 1
0 add 1
tpop 0
goto 3
"""