# 定义处理类型标注的utility
# 给定一个ast形式的类型标注，返回tysys中对应的类型

from tysys import *

def parse_type_annotation(anno):
    return TyDyn()