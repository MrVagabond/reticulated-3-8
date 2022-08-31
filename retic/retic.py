# main是入口函数

import ast
import sys
import astpretty

import typing
from . import parse_anno
from . import check

__all__ = ['main']

def main():
    filename = sys.argv[1]
    file = open(filename, 'r', encoding='UTF-8')
    st = ast.parse(file.read())
    file.close()
    astpretty.pprint(st, show_offsets=False) # 打印
    parse_anno.ParseTyAnno().visit(st)
    check.InsertCheck().visit(st)
    check.Check2AST().visit(st)
    astpretty.pprint(st, show_offsets=False)  # 打印
    code = compile(st, filename, 'exec')
    print(code)
    exec(code)




