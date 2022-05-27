
import ast
import re
from .tysys import *
from . import visitor
from . import typing_builtin


class TypingVisitor(visitor.Visitor):

    def visit_Module(self, node, typing_env=None):
        # Module(stmt* body, type_ignore *type_ignores)
        env = None
        if typing_env is None:
            env = TypingEnv()
        else:
            env = TypingEnv(copyFrom=typing_env)
        for nd in node.body:
            env = self.dispatch(nd, env)
        node.retic_type = env
        return env

    #---- visit_stmt: TypingEnv -> TypingEnv

    def visit_FunctionDef(self, node, typing_env):
        # FunctionDef(identifier name, arguments args,
        #             stmt* body, expr* decorator_list, expr? returns,
        #             string? type_comment)
        env = TypingEnv(copyFrom=typing_env)

        # 将参数及其类型加入环境，将函数本身也加入环境（用于递归调用）
        return_type = str2type(node.returns.value)
        args_name = []
        args_type = {}

        allArgs = node.args.posonlyargs + node.args.args + [node.args.vararg] + node.args.kwonlyargs + [node.args.kwarg]
        for arg in allArgs:
            if arg is None:  # vararg和kwarg可能是None
                continue
            if arg.annotation is not None:
                assert isinstance(arg.annotation, ast.Constant)
                args_name.append(arg.arg)
                args_type[arg.arg] = str2type(arg.annotation.value)
            else:
                args_name.append(arg.arg)
                args_type[arg.arg] = TyDyn()

        node.retic_type = TyFun(funName=node.name,
                                      argType=TyListArg([args_type[x] for x in args_name], args_name),
                                      bodyType=return_type)
        for nm, ty in zip(node.retic_type.getArgType().getArgNameList(), node.retic_type.getArgType().getArgTypeList()):
            env.put(nm, ty)
        env.put(node.name, node.retic_type)
        for nd in node.body:
            env = self.dispatch(nd, env)

        # 最后只在传入env中新增该函数的类型
        ret_env = TypingEnv(copyFrom=typing_env)
        ret_env.put(node.name, node.retic_type)
        return ret_env

    def visit_ClassDef(self, node, typing_env):
        # ClassDef(identifier name,
        #              expr* bases,
        #              keyword* keywords,
        #              stmt* body,
        #              expr* decorator_list)
        env = TypingEnv(copyFrom=typing_env)
        raise TypingErr('Not Implemented')

    def visit_For(self, node, typing_env):
        # For(expr target, expr iter, stmt* body, stmt* orelse, string? type_comment)
        env = TypingEnv(copyFrom=typing_env)
        raise TypingErr('Not Implemented')

    def visit_While(self, node, typing_env):
        # While(expr test, stmt* body, stmt* orelse)
        env = TypingEnv(copyFrom=typing_env)
        raise TypingErr('Not Implemented')

    def visit_If(self, node, typing_env):
        # If(expr test, stmt* body, stmt* orelse)
        env = TypingEnv(copyFrom=typing_env)
        raise TypingErr('Not Implemented')

    def visit_With(self, node, typing_env):
        # With(withitem* items, stmt* body, string? type_comment)
        env = TypingEnv(copyFrom=typing_env)
        raise TypingErr('Not Implemented')


    def visit_Assign(self, node, typing_env):
        # Assign(expr* targets, expr value, string? type_comment)

        env = TypingEnv(copyFrom=typing_env)
        value_type = self.dispatch(node.value, env)  # Ty
        # case 1: Multiple assignment 就是 x = y = 1 这种
        for t in node.targets:
            assert isinstance(t, ast.Name)
            env.put(t.id, value_type)
            t.retic_type = value_type
        # case 2: Unpacking 也就是 x,y = 1,2 这种，暂不处理
        if isinstance(node.targets[0], ast.Tuple) or isinstance(node.targets[0], ast.List):
            raise TypingErr('暂时不支持unpacking形式的assign操作')
        return env


    def visit_Return(self, node, typing_env):
        # Return(expr? value)
        if node.value is None:
            pass
        else:
            self.dispatch(node.value, typing_env)
        return TypingEnv(copyFrom=typing_env)


    #---- visit_expr: TypingEnv -> Ty

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
        container_type = self.dispatch(node.value, typing_env)
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
        instance_type = self.dispatch(node.value, typing_env)
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
        left_type = self.dispatch(node.left, typing_env)  # Ty
        right_type = self.dispatch(node.right, typing_env)  # Ty
        if typeEq(left_type, right_type):
            node.retic_type = left_type
        else:
            # 保守处理，这排除了类似"hello"*3这样的合法表达式
            node.retic_type = TyDyn()
        return node.retic_type

    def visit_UnaryOp(self, node, typing_env):
        # UnaryOp(unaryop op, expr operand)
        operand_type = self.dispatch(node.operand, typing_env)
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
        func_type = self.dispatch(node.func, typing_env)
        for nd in node.args:
            self.dispatch(nd, typing_env)
        for nd in node.keywords:
            self.dispatch(nd, typing_env)

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

    def dispatch(self, node, indent):
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
            self.dispatch(nd, indent+1)


class TypingErr(Exception):
    pass