import ast
import sys
import astpretty

from . import typing
from . import astim

def main():

    # read source file and get ast
    filename = sys.argv[1]
    file = open(filename)
    st = ast.parse(file.read())
    file.close()
    astpretty.pprint(st, show_offsets=False)
    astim.add_parent(st) # 为每个节点标记父节点retic_parent

    typing.TypingVisitor(st).visit()
    typing.ShowTyping(st).visit(indent=0)



