
#### 为一个Module定型

import re
import ast
from retic import tysys
from retic import visitor



# 使用方法 TypeCollectVisitor(st).visit()
# 这种做法真的好吗？如果有嵌套定义的函数，该怎么处理呢？
class TypeCollectVisitor(visitor.Visitor):
    # 在Module, FunctionDef节点上生成retic_type属性，用于搜集用户标注的类型信息

    def visit_Module(self, node):

        module_fields_type = {}

        for nd in node.body:
            if isinstance(nd, ast.FunctionDef):
                module_fields_type[nd.name] = self.visit_FunctionDef(nd)
            elif isinstance(nd, ast.ClassDef):
                # module_fields_type[nd.name] = self.visit_ClassDef(nd)
                pass

        node.retic_type = tysys.TyModule(module_fields_type)

    def visit_FunctionDef(self, node):
        assert isinstance(node.returns, ast.Constant)
        return_type = tysys.str2type(node.returns.value)
        args_name = []
        args_type = {}

        allArgs = node.args.posonlyargs + node.args.args + [node.args.vararg] + node.args.kwonlyargs + [node.args.kwarg]
        for arg in allArgs:
            if arg is None: # vararg和kwarg可能是None
                continue
            if arg.annotation is not None:
                assert isinstance(arg.annotation, ast.Constant)
                args_name.append(arg.arg)
                args_type[arg.arg] = tysys.str2type(arg.annotation.value)
            else:
                args_name.append(arg.arg)
                args_type[arg.arg] = tysys.TyDyn()

        node.retic_type = tysys.TyFun(  funName=node.name,
                                        argType=tysys.TyListArg([args_type[x] for x in args_name], args_name),
                                        bodyType=return_type )

        return node.retic_type

    def visit_ClassDef(self, node):
        pass


# 使用方法 TypingVisitor(st).visit()
# 必须在TypeCollectVisitor处理之后使用，为每个可以具备类型的节点标注其最精确的类型
# 这一遍过后，每个expr类型的节点（除了一些无用的情况）都必须具有retic_type属性
class TypingVisitor(visitor.Visitor):

    # Module和FunctionDef都是scope，遵循树形原则
    def visit_Module(self, node):
        env = node.retic_type.getAllFieldType() # python字典{str:Ty} 初始环境是所有函数的类型
        for nd in node.body:
            env = self.visit(nd, env=env) # 每个节点都初始化一个typing环境
        return env # 返回整个模块所有接口的类型

    def visit_FunctionDef(self, node, env):
        # FunctionDef(identifier name, arguments args,
        #                        stmt* body, expr* decorator_list, expr? returns,
        #                        string? type_comment)

        local_env = env.copy()
        # 将参数加入env
        local_env.update({ nm : ty for nm, ty in zip(node.retic_type.getArgType().getArgNameList(), node.retic_type.getArgType().getArgTypeList())})
        for nd in node.body:
            local_env = self.visit(nd, env=local_env) # 每次都会返回新的env
        return env # 函数定义不会创造新的环境（因为一开始就把所有函数类型加到环境中了）


    #### other stmt，这些stmt都是env->env的函数

    # env -> env
    def visit_Assign(self, node, env):
        # Assign(expr* targets, expr value, string? type_comment)
        # python的赋值操作允许多目标赋值，但我们这里先不管这个

        local_env = env.copy()
        value_type = self.visit(node.value, env=env) # Ty
        # case 1: Multiple assignment 就是 x = y = 1 这种
        for t in node.targets:
            assert isinstance(t, ast.Name)
            local_env.update({t.id : value_type})
            t.retic_type = value_type # 为的是将所有expr都typing

        # case 2: Unpacking 也就是 x,y = 1,2 这种，暂不处理
        if isinstance(node.targets[0], ast.Tuple) or isinstance(node.targets[0], ast.List):
            raise TypingErr('暂时不支持unpacking形式的assign操作')

        return local_env

    def visit_Return(self, node, env):
        # Return(expr? value)
        # 需要在此处检查return的返回值类型是否和标注一致
        return_type = None
        if node.value is None:
            return_type = tysys.TyDyn()
        else:
            return_type = self.visit(node.value, env=env)

        # 向上查找FunctionDef节点，判断其标注类型是否和return_type一致
        fd = node
        while not isinstance(fd, ast.FunctionDef):
            fd = getattr(fd, 'retic_parent')
        expect_type = getattr(fd, 'retic_type').getBodyType()
        if not tysys.typeConsistent(return_type, expect_type):
            raise TypingErr('return type is not consistent with expect body type')
        return env




    #### expr，表达式本身是env->ty的函数，同时每个expr节点都需要增加retic_type属性

    def visit_Constant(self, node, env):
        # Constant(constant value, string? kind)
        if isinstance(node.value, int):
            node.retic_type = tysys.TyInt()
        elif isinstance(node.value, bool):
            node.retic_type = tysys.TyBool()
        elif isinstance(node.value, str):
            node.retic_type = tysys.TyStr()
        elif isinstance(node.value, type(None)):
            node.retic_type = tysys.TyNone()
        else:
            raise TypingErr('not support this kind of constant')
        return node.retic_type

    def visit_Name(self, node, env):
        # Name(identifier id, expr_context ctx)
        name_type = env.get(node.id, None)
        if name_type is None:
            raise TypingErr('cannot find name: ' + node.id)
        node.retic_type = name_type
        return node.retic_type

    def visit_Attribute(self, node, env):
        # Attribute(expr value, identifier attr, expr_context ctx)
        pass

    def visit_Subscript(self, node, env):
        # Subscript(expr value, slice slice, expr_context ctx)
        # slice = Slice(expr? lower, expr? upper, expr? step)
        #           | ExtSlice(slice* dims)
        #           | Index(expr value)
        # 暂时只考虑value是Name，slice是Index的情况，即a[1]
        assert isinstance(node.value, ast.Name)
        assert isinstance(node.slice, ast.Index)
        container_type = self.visit(node.value, env)
        if isinstance(container_type, tysys.TyContainer):
            if tysys.typeEq(container_type, tysys.TyDict()):
                # 只可能是valType
                node.retic_type = container_type.valType
            else:
                node.retic_type = container_type.eltType
        else:
            node.retic_type = tysys.TyDyn()
        return node.retic_type

    def visit_Starred(self, node, env):
        # Starred(expr value, expr_context ctx)
        pass

    def visit_List(self, node, env):
        pass

    def visit_Tuple(self, node, env):
        pass

    def visit_BinOp(self, node, env):
        # BinOp(expr left, operator op, expr right)
        # python的二元操作其实允许"xyz"*3这样的操作，但我们这里先不管这个
        left_type = self.visit(node.left, env=env) # Ty
        right_type = self.visit(node.right, env=env) # Ty
        if tysys.typeConsistent(left_type, right_type):
            node.retic_type = left_type
        else:
            node.retic_type = tysys.TyDyn()
        return node.retic_type

    def visit_BoolOp(self, node, env):
        # BoolOp(boolop op, expr* values)
        for val in node.values:
            self.visit(val, env=env) # 为的是将所有expr都typing
        node.retic_type = tysys.TyBool()
        return node.retic_type

    def visit_Call(self, node, env):
        # Call(expr func, expr* args, keyword* keywords)
        # python函数调用也有多种形式，这里只考虑简单的情况
        assert isinstance(node.func, ast.Name)

        for arg in node.args:
            self.visit(arg, env=env) # 为的是将所有expr都typing
        for kw in node.keywords:
            self.visit(kw, env=env) # 为的是将所有expr都typing

        fun_type = env.get(node.func.id, None)
        # 这里需要检查调用时的参数类型是否匹配
        if fun_type is not None:
            node.func.retic_type = fun_type
            node.retic_type = fun_type.getBodyType() # 不考虑是否匹配，完全信任
        else:
            # node.func.retic_type = tysys.TyDyn()
            # node.retic_type = tysys.TyDyn()
            raise TypingErr('bad fun_type')
        return node.retic_type

    def visit_keyword(self, node, env):
        # keyword = (identifier? arg, expr value)
        # 调用的时候，需要解析出arg对应的参数是哪个，但这里我们先简单地处理，只考虑value的类型
        return self.visit(node.value, env=env)






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


# 使用方法：InferVisitor(st).visit()
# 这一遍过后，每个expr节点都增加infer_type属性，用来表示静态推导出的类型
class InferVisitor(visitor.Visitor):
    # 使用后序遍历，优先为每个子节点typing后再为当前节点typing

    def visit_Module(self, node):
        env = {}
        for nd in node.body:
            env = self.visit(nd, env=env)
        return env  # 返回整个模块所有可以静态推导出的类型

    def visit_FunctionDef(self, node, env):
        pass

    def visit_Constant(self, node, env):
        # Constant(constant value, string? kind)
        if isinstance(node.value, int):
            node.infer_type = tysys.TyInt()
        elif isinstance(node.value, str):
            node.infer_type = tysys.TyStr()
        elif isinstance(node.value, bool):
            node.infer_type = tysys.TyBool()
        elif isinstance(node.value, type(None)):
            node.infer_type = tysys.TyNone()
        else:
            raise TypingErr('not support this kind of constant')
        return node.infer_type






class TypingErr(Exception):
    pass