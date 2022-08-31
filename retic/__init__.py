
# pass 1: 处理类型标注，将所有类型标注转为tysys中的类型表示，存放在ast节点的retic_type属性中

# pass 2: 在ast合适的位置上插入check节点

# pass 3: 将check节点全部转为合法的AST节点