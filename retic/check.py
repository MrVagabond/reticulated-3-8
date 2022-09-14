
import ast
from . import tysys
from . import visitor
from . import transformer
from . import env

class Tag:
    pass

class PosArg(Tag):
    def __init__(self, n, lin, col):
        self.n = n
        self.lin = lin
        self.col = col

class Ret(Tag):
    def __init__(self, lin, col):
        self.lin = lin
        self.col = col

class Check(ast.expr):
    # Check(expr value, Ty expect_type, Tag tag)
    def __init__(self, value, expect_type: tysys.Ty, tag: Tag):
        self.value = value
        self.expect_type = expect_type
        self.tag = tag
        print('insert check at [{},{}]: value={}, expect_type={}'.format(value.lineno, value.col_offset, value, str(expect_type)))

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

class InsertCheck(transformer.Transformer):
    # 对函数调用的参数和返回值进行check
    # 朴素的做法是，函数的参数check放在函数定义开头处，函数的返回值check放在函数调用处
    # 不过，如果参数check在调用处已经满足，那么不需要在定义处check，如果
    def visit_Module(self, node, ftr:env.FuncTypeRecorder):
        for nd in node.body:
            self.visit(nd, ftr)

    def visit_FunctionDef(self, node, ftr:env.FuncTypeRecorder):

        fun_type = node.retic_type
        arg_type = fun_type.getArgType()
        arg_type_list:list = fun_type.getArgType().getArgTypeList()
        return_type = fun_type.getBodyType()
        arg_name_list = []
        for e in node.args.args:
            arg_name_list.append(e.arg)

        # 如果该函数不对参数和返回值做任何enforcement，那么不插入任何检查，直接返回

        # 该函数的参数如果是简单类型的，那么由调用者进行检查；如果是函数类型的，创建blame栈
        # for i in range(len(arg_type_list)):
        #     ty = arg_type_list[i]
        #     nm = arg_name_list[i]
        #     node.body.insert(0, Check(nm, ty, PosArg(i, node.lineno, node.col_offset)))


        # 如果该函数有返回值的类型标注，那么由该函数进行检查
        for nd in node.body:
            self.visit(nd, ftr, return_type)
        return node



    def visit_Call(self, node, ftr:env.FuncTypeRecorder, return_type:tysys.Ty):
        # Call(expr func, expr* args, keyword* keywords)
        func = node.func
        args:list = node.args




    def visit_Return(self, node, ftr:env.FuncTypeRecorder, return_type:tysys.Ty):
        value = node.value
        if value is None:
            if isinstance(return_type, tysys.TyNone):
                return
            else:
                raise CheckInsertErr('Expected return type <None> but get type <{}>'.format(str(return_type)))
            return node
        else:
            return ast.Return(value=Check(value=node.value, expect_type=return_type, tag=Ret(node.lineno, node.col_offset)))



class Check2AST(transformer.Transformer):

    def visit_Check(self, node):
        return node.to_ast()



class CheckInsertErr(Exception):
    pass