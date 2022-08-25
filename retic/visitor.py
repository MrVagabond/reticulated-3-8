

import ast



class Visitor:
    def __init__(self, tree):
        assert tree.__class__ == ast.Module
        self.tree = tree
        self.currentNode = None

    # 所有调用都使用dispatch
    # 由于采用的是访问者模式，所以每个节点都必须手动进行dispatch
    def visit(self, node, *args, **kwargs): # 中转层，也叫dispatch层，允许每个visit函数附带一个元组参数和一个字典参数
        clzName = node.__class__.__name__
        meth = getattr(self, 'visit_' + clzName, None)
        if meth is None:
            raise VisitorErr('this version does not support Python language feature: ' + clzName)

        self.currentNode = node
        return meth(node, *args, **kwargs)

    # proceed只在最上层调用
    def proceed(self, *args, **kwargs):
        return self.visit(self.tree, *args, **kwargs)


    #---- 会产生新的scope的语句

    def visit_Module(self, node, *args, **kwargs):
        raise VisitorErr('visit_Module not handled, must be overridden')

    def visit_FunctionDef(self, node, *args, **kwargs):
        raise VisitorErr('visit_FunctionDef not handled, must be overridden')

    def visit_ClassDef(self, node, *args, **kwargs):
        raise VisitorErr('visit_ClassDef not handled, must be overridden')

    def visit_For(self, node, *args, **kwargs):
        # For(expr target, expr iter, stmt* body, stmt* orelse, string? type_comment)
        raise VisitorErr('visit_For not handled, must be overridden')

    def visit_While(self, node, *args, **kwargs):
        # While(expr test, stmt* body, stmt* orelse)
        raise VisitorErr('visit_While not handled, must be overridden')

    def visit_If(self, node, *args, **kwargs):
        # If(expr test, stmt* body, stmt* orelse)
        raise VisitorErr('visit_If not handled, must be overridden')

    def visit_With(self, node, *args, **kwargs):
        raise VisitorErr('visit_With not handled, must be overridden')


    #---- 会改变env的语句

    def visit_Assign(self, node, *args, **kwargs):
        # Assign(expr* targets, expr value, string? type_comment)
        # 赋值也是非常特殊的语句，需要重点处理
        raise VisitorErr('visit_Assign not handled, must be overridden')

    def visit_AugAssign(self, node, *args, **kwargs):
        # AugAssign(expr target, operator op, expr value)
        # 增量赋值同上
        raise VisitorErr('visit_AugAssign not handled, must be overridden')

    #---- 模块相关的语句

    def visit_Import(self, node, *args, **kwargs):
        raise VisitorErr('visit_Import not handled, must be overridden')

    def visit_ImportFrom(self, node, *args, **kwargs):
        raise VisitorErr('visit_ImportFrom not handled, must be overridden')

    #---- 其他语句

    def visit_Return(self, node, *args, **kwargs):
        # Return(expr? value) 只需要关注返回的表达式
        raise VisitorErr('visit_Return not handled, must be overridden')

    def visit_Delete(self, node, *args, **kwargs):
        raise VisitorErr('visit_Delete not handled, must be overridden')

    def visit_Expr(self, node, *args, **kwargs):
        # Expr(expr value)
        raise VisitorErr('visit_Expr not handled, must be overridden')

    def visit_Pass(self, node, *args, **kwargs):
        raise VisitorErr('visit_Pass not handled, must be overridden')

    def visit_Break(self, node, *args, **kwargs):
        raise VisitorErr('visit_Break not handled, must be overridden')

    def visit_Continue(self, node, *args, **kwargs):
        raise VisitorErr('visit_Continue not handled, must be overridden')

    def visit_Global(self, node, *args, **kwargs):
        raise VisitorErr('visit_Global not handled, must be overridden')

    def visit_Nonlocal(self, node, *args, **kwargs):
        raise VisitorErr('visit_Nonlocal not handled, must be overridden')


    #---- 常量表达式
    def visit_Constant(self, node, *args, **kwargs):
        raise VisitorErr('visit_Constant not handled, must be overridden')

    #---- 带context的表达式

    def visit_Name(self, node, *args, **kwargs):
        # Name(identifier id, expr_context ctx)
        raise VisitorErr('visit_Name not handled, must be overridden')

    def visit_Subscript(self, node, *args, **kwargs):
        raise VisitorErr('visit_Subscript not handled, must be overridden')

    def visit_Attribute(self, node, *args, **kwargs):
        raise VisitorErr('visit_Attribute not handled, must be overridden')

    def visit_Starred(self, node, *args, **kwargs):
        raise VisitorErr('visit_Starred not handled, must be overridden')

    def visit_List(self, node, *args, **kwargs):
        raise VisitorErr('visit_List not handled, must be overridden')

    def visit_Tuple(self, node, *args, **kwargs):
        raise VisitorErr('visit_Tuple not handled, must be overridden')


    #---- 复合操作的表达式
    def visit_BoolOp(self, node, *args, **kwargs):
        raise VisitorErr('visit_BoolOp not handled, must be overridden')

    def visit_BinOp(self, node, *args, **kwargs):
        # BinOp(expr left, operator op, expr right)
        raise VisitorErr('visit_BinOp not handled, must be overridden')

    def visit_UnaryOp(self, node, *args, **kwargs):
        raise VisitorErr('visit_UnaryOp not handled, must be overridden')

    def visit_IfExp(self, node, *args, **kwargs):
        raise VisitorErr('visit_IfExp not handled, must be overridden')

    def visit_Compare(self, node, *args, **kwargs):
        raise VisitorErr('visit_Compare not handled, must be overridden')

    def visit_Call(self, node, *args, **kwargs):
        raise VisitorErr('visit_Call not handled, must be overridden')

    #---- 复合数据结构的表达式

    def visit_Dict(self, node, *args, **kwargs):
        raise VisitorErr('visit_Dict not handled, must be overridden')

    def visit_Set(self, node, *args, **kwargs):
        raise VisitorErr('visit_Set not handled, must be overridden')



class VisitorErr(Exception):
    pass