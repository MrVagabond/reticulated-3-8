
import ast
import re
from .tysys import *
from . import visitor
from . import typing_builtin
from . import env


class TypingVisitor(visitor.Visitor):

    def visit_Module(self, node, ftr:env.FuncTypeRecorder, typing_env=None):
        # 只在函数内进行typing
        for nd in node.body:
            self.visit(nd, ftr)


    def visit_FunctionDef(self, node):
        pass

    def visit_Constant(self, node, typing_env):
        if isinstance(node.value, int):
            node.retic_type = TyInt()
        elif isinstance(node.value, str):
            node.retic_type = TyStr()
        elif isinstance(node.value, bool):
            node.retic_type = TyBool()
        elif isinstance(node.value, type(None)):
            node.retic_type = TyNone()
        else:
            raise TypingErr('not support this kind of constant')
        return node.retic_type

    def visit_Name(self, node, typing_env):
        # Name(identifier id, expr_context ctx)
        name_type = typing_env.get(node.id)
        node.retic_type = name_type
        return node.retic_type

    def visit_Subscript(self, node, typing_env):
        # Subscript(expr value, slice slice, expr_context ctx)
        # slice = Slice(expr? lower, expr? upper, expr? step)
        #           | ExtSlice(slice* dims)
        #           | Index(expr value)
        # 暂时只考虑value是Name，slice是Index的情况，即a[1]
        assert isinstance(node.value, ast.Name)
        assert isinstance(node.slice, ast.Index)
        container_type = self.visit(node.value, typing_env)
        if isinstance(container_type, TyContainer):
            if typeEq(container_type, TyDict()):
                # 只可能是valType
                node.retic_type = container_type.valType
            else:
                node.retic_type = container_type.eltType
        else:
            node.retic_type = TyDyn()
        return node.retic_type

    def visit_Attribute(self, node, typing_env):
        # Attribute(expr value, identifier attr, expr_context ctx)
        # 如果是内置类型，需要访问typing_builtin中的记录
        # 否则就是自定义类型，暂不支持
        assert isinstance(node.value, ast.Name)
        instance_type = self.visit(node.value, typing_env)
        if isinstance(instance_type, TyInt):
            node.retic_type = typing_builtin.intfields[node.attr]
        elif isinstance(instance_type, TyBool):
            node.retic_type = typing_builtin.boolfields[node.attr]
        elif isinstance(instance_type, TyStr):
            node.retic_type = typing_builtin.strfields[node.attr]
        elif isinstance(instance_type, TyNone):
            node.retic_type = typing_builtin.nonefields[node.attr]
        elif isinstance(instance_type, TyModule):
            raise TypingErr('TODO')
        elif isinstance(instance_type, TyFun):
            raise TypingErr('TODO')
        elif isinstance(instance_type, TyList):
            raise TypingErr('TODO')
        elif isinstance(instance_type, TyTuple):
            raise TypingErr('TODO')
        elif isinstance(instance_type, TySet):
            raise TypingErr('TODO')
        elif isinstance(instance_type, TyDict):
            raise TypingErr('TODO')
        else:
            raise TypingErr('暂不支持自定义类型的属性访问操作')

    def visit_List(self, node, typing_env):
        # List(expr* elts, expr_context ctx)
        # 保守处理
        node.retic_type = TyDyn()
        return node.retic_type

    def visit_Tuple(self, node, typing_env):
        # Tuple(expr* elts, expr_context ctx)
        # 保守处理
        node.retic_type = TyDyn()
        return node.retic_type

    def visit_BoolOp(self, node, typing_env):
        # BoolOp(boolop op, expr* values)
        # 无论是什么表达式，返回的结果都是bool类型
        node.retic_type = TyBool()
        return node.retic_type

    def visit_BinOp(self, node, typing_env):
        # BinOp(expr left, operator op, expr right)
        left_type = self.visit(node.left, typing_env)  # Ty
        right_type = self.visit(node.right, typing_env)  # Ty
        if typeEq(left_type, right_type):
            node.retic_type = left_type
        else:
            # 保守处理，这排除了类似"hello"*3这样的合法表达式
            node.retic_type = TyDyn()
        return node.retic_type

    def visit_UnaryOp(self, node, typing_env):
        # UnaryOp(unaryop op, expr operand)
        operand_type = self.visit(node.operand, typing_env)
        if isinstance(node.op, ast.Not):
            node.retic_type = TyBool()
        else:
            # 保守处理
            node.retic_type = TyDyn()
        return node.retic_type

    def visit_IfExp(self, node, typing_env):
        # IfExp(expr test, expr body, expr orelse)
        # 保守处理，本来应该返回body和orelse的并类型
        node.retic_type = TyDyn()
        return node.retic_type

    def visit_Compare(self, node, typing_env):
        # Compare(expr left, cmpop* ops, expr* comparators)
        # 无论怎么比较，返回的结果都是bool类型
        node.retic_type = TyBool()
        return node.retic_type

    def visit_Call(self, node, typing_env):
        # Call(expr func, expr* args, keyword* keywords)
        func_type = self.visit(node.func, typing_env)
        for nd in node.args:
            self.visit(nd, typing_env)
        for nd in node.keywords:
            self.visit(nd, typing_env)

        # * |= *->*
        # A->B |= A->B
        matched_func_type = fun_match(func_type)

        # 检查参数类型是否consistent
        # pass 暂不处理

        # 通过所有检查才能为这个function application定型
        node.retic_type = matched_func_type.getBodyType()
        return node.retic_type

    def visit_Dict(self, node, typing_env):
        # Dict(expr* keys, expr* values)
        # 保守处理
        node.retic_type = TyDyn()
        return node.retic_type

    def visit_Set(self, node, typing_env):
        # Set(expr* elts)
        # 保守处理
        node.retic_type = TyDyn()
        return node.retic_type

# 使用方法 ShowTyping(st).visit(indent=0)
# 打印所有节点的retic_type信息
class ShowTyping(visitor.Visitor):

    def visit(self, node, indent):
        print('------' * indent, end='')
        print(re.findall('<_ast.* object', str(node))[0][6:-7], end='')
        if isinstance(node, ast.expr):
            if getattr(node, 'retic_type', None) is not None:
                print(': ' + str(node.retic_type))
            else:
                print(': ???')
        elif isinstance(node, ast.FunctionDef):
            print(': TyFun')
        elif isinstance(node, ast.Module):
            print(': TyModule')
        else:
            print('')
        for nd in ast.iter_child_nodes(node):
            self.visit(nd, indent + 1)


class TypingErr(Exception):
    pass