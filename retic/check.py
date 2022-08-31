
import ast
from . import tysys
from . import visitor
from . import transformer

class Tag:
    pass

class PosArg(Tag):
    def __init__(self, n, lin, col):
        self.n = n
        self.lin = lin
        self.col = col


class Check(ast.expr):
    # Check(expr value, Ty expect_type, Tag tag)
    def __init__(self, value, expect_type, tag):
        self.value = value
        self.expect_type = expect_type
        self.tag = tag
        print('insert check: value={}, expect_type={}'.format(value, str(expect_type)))

    def to_ast(self):
        return ast.Expr(
            value=ast.Call(
                        func=ast.Name(id='print', ctx=ast.Load(), lineno=0, col_offset=0),
                        args=[ast.Constant(value='runtime check: do check', kind=None, lineno=0, col_offset=0)],
                        keywords=[],
                        lineno=0, col_offset=0),
            lineno=0, col_offset=0
        )


# check的ast表示，至于如何编译是python解释器的事情
def checkArg(argName, argType):
    pass

class InsertCheck(visitor.Visitor):
    # 对函数调用的参数和返回值进行check
    # 朴素的做法是，函数的参数check放在函数定义开头处，函数的返回值check放在函数调用处
    # 不过，如果参数check在调用处已经满足，那么不需要在定义处check，如果

    def visit_FunctionDef(self, node):
        fun_type = node.retic_type

        arg_type_list = fun_type.getArgType().getArgTypeList()
        return_type = fun_type.getBodyType()

        arg_name_list = []
        for e in node.args.args:
            arg_name_list.append(e.arg)

        for i in range(len(arg_type_list)):
            ty = arg_type_list[i]
            nm = arg_name_list[i]
            node.body.insert(0, Check(nm, ty, PosArg(i, node.lineno, node.col_offset)))



    def visit_Call(self, node):
        pass


class Check2AST(transformer.Transformer):

    def visit_Check(self, node):
        return node.to_ast()



class CheckInsertErr(Exception):
    pass