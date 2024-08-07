import executor
from lexer import *
from builder import *
from executor import *
from operators import *

e = lex2(lex1(prelex("declare test;write \"Test 1\" str;push ALL;clone THIS to test;use test;ddel THIS;mforward outstr ALL")))

#for i in e:
#    print(f"{i.content} {i.type}")
execute(simple_build(e))

#print(executor.GlMemory.mem)