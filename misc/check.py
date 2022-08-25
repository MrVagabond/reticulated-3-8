
import ast
from retic import tysys
from retic import visitor


class Check(ast.expr):
    # Check(expr value, expect_type)
    def __init__(self, value, expect_type=tysys.Dyn(), lin=0, col=0):
        self.value = value
        self.expect_type = expect_type
        self.lin = lin
        self.col = col


class InsertCheck(visitor.Visitor):
    # 对函数调用的参数和返回值进行check
    # 朴素的做法是，函数的参数check放在函数定义开头处，函数的返回值check放在函数调用处
    # 不过，如果参数check在调用处已经满足，那么不需要在定义处check，如果

    def visit_Module(self, node):
        # Module(stmt* body, type_ignore *type_ignores)
        for nd in node.body:
            self.visit(nd)

    def visit_FunctionDef(self, node):
        pass

    def visit_Call(self, node):
        pass
