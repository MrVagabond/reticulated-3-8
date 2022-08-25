# main是入口函数

import ast
import sys
import astpretty


def main():

    # read source file and get ast
    filename = sys.argv[1]
    file = open(filename)
    st = ast.parse(file.read())
    file.close()
    astpretty.pprint(st, show_offsets=False)
    # astim.add_parent(st) # 为每个节点标记父节点retic_parent
    #
    # typing.TypingVisitor(st).proceed()
    # typing.ShowTyping(st).proceed(indent=0)



