# main是入口函数

import ast
import sys
import astpretty

from . import typing
from . import parse_anno
from . import check
from . import env

__all__ = ['main']

def main():
    filename = sys.argv[1]
    file = open(filename, 'r', encoding='UTF-8')
    st = ast.parse(file.read())
    file.close()
    astpretty.pprint(st, show_offsets=False) # 打印

    # 提取类型标注，打印ftr
    ftr:env.FuncTypeRecorder = parse_anno.ParseTyAnno().visit(st)

    # typing一些expr，我觉得这是不必要的，因为retic_type依旧是静态推导出来的类型，有了ftr就够了
    # typing.TypingVisitor().visit(st, ftr)

    # 插入check，检查静态的type enforcement和实际运行时的类型
    check.InsertCheck().visit(st, ftr)

    # 将check转为合法的ast
    check.Check2AST().visit(st)

    # astpretty.pprint(st, show_offsets=False)  # 打印

    # 生成可执行的code object
    # code = compile(st, filename, 'exec')
    # print(code)
    # exec(code)




