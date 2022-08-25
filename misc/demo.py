import visitor
import ast
import tysys

class BlameCheck(ast.AST):
    def __init__(self, responsible, tag):
        self.responsible = responsible
        self.tag = tag

class Tag:
    pass

class PosArg(Tag):
    pass

class Ret(Tag):
    pass



def type_check(node):
    if isinstance(node, ast.Constant):
        if isinstance(node.value, int):
            return tysys.TyInt()
        elif isinstance(node.value, str):
            return tysys.TyStr()
        elif isinstance(node.value, bool):
            return tysys.TyBool()
        elif isinstance(node.value, type(None)):
            return tysys.TyNone()
        else:
            raise DemoErr("not support this type of constant")
    elif isinstance(node, ast.Name):




class DemoTransient(visitor.Visitor):
    def visit_Module(self, node, *args, **kwargs):
        # Module(stmt* body, type_ignore *type_ignores)
        for n in self.body:
            self.visit(n, *args, **kwargs)

    def visit_FunctionDef(self, node, *args, **kwargs):
        pass

    def visit_Return(self, node, *args, **kwargs):
        pass

    def visit_Call(self, node, *args, **kwargs):
        pass

    def visit_Assign(self, node, *args, **kwargs):
        pass

    def visit_BinOp(self, node, *args, **kwargs):
        pass

    def visit_Name(self, node, *args, **kwargs):
        pass

    def visit_Constant(self, node, *args, **kwargs):
        pass


class DemoErr(Exception):
    pass