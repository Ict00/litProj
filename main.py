import executor
from lexer import *
from builder import *
from executor import *
from operators import *

e = lex2(lex1(prelex("writenum 2\nwritenum 3\nadd 0 1\nuse outnum\npush ALL")))

execute(simple_build(e))

#print(executor.GlMemory.mem)