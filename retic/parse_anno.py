# 定义处理类型标注的utility
# 给定一个ast形式的类型标注，返回tysys中对应的类型

# 模块代码结构
# 导入导出
# 内部辅助函数
# 唯一导出函数parse_type_annotation
# 唯一导出工具类ParseTyAnno
import ast

from .tysys import *
from . import visitor
from . import env

__all__ = ['parse_type_annotation', 'ParseTyAnno']


def parse_type_annotation(anno):
    # 解析mypy支持的类型标注，可以只实现一些常用的
    if isinstance(anno, ast.Name):
        if anno.id == "int":
            return TyInt()
        elif anno.id == "str":
            return TyStr()
        elif anno.id == "bool":
            return TyBool()
        else:
            raise ParseTyAnnoErr('暂时不支持除int、str、bool之外的基本类型标注')
    elif isinstance(anno, ast.Subscript):
        if anno.value.id == "Callable":
            arg_type_list = anno.slice.value.elts[0].elts
            return_type = anno.slice.value.elts[1]
            arg_type = []
            for e in arg_type_list:
                arg_type.append(parse_type_annotation(e))
            return TyFun(argType=TyListArg(argTypeList=arg_type), bodyType=parse_type_annotation(return_type))
        elif anno.value.id == "List":
            elem_type = anno.slice.value
            elem_type = parse_type_annotation(elem_type)
            return TyList(eltType=elem_type)
        else:
            raise ParseTyAnnoErr('暂时不支持除Callable、List之外的复合类型标注')
    else:
        raise ParseTyAnnoErr('currently not supported type annotation')


class ParseTyAnno(visitor.Visitor):
    def visit_Module(self, node):
        func_type_recorder = env.FuncTypeRecorder()
        for n in node.body:
            self.visit(n, func_type_recorder)
        return func_type_recorder

    def visit_FunctionDef(self, node, func_type_recorder:env.FuncTypeRecorder):
        arg_list = node.args.args
        arg_type = []
        for arg in arg_list:
            if arg.annotation is None:
                arg_type.append(TyDyn())
            else:
                arg_type.append(parse_type_annotation(arg.annotation))
        return_anno = node.returns
        return_type = TyDyn()
        if return_anno is not None:
            return_type = parse_type_annotation(return_anno)
        print("arg type is: ", end='')
        print(arg_type, end='')
        print(", return type is: " + str(return_type))
        node.retic_type = TyFun(argType=TyListArg(argTypeList=arg_type), bodyType=return_type, funName=node.name)
        func_type_recorder.put(node.name, node.retic_type)


class ParseTyAnnoErr(Exception):
    pass