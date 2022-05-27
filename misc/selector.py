import ast
from retic import astim

class Selector:
    def __init__(self, tree:ast.Module):
        self.tree = tree
        astim.add_parent(self.tree) # 默认添加parent属性


    def S(self, pattern, order=0): # 根据pattern选择所有满足的节点
        if pattern is None:
            raise SelectorErr('search pattern must be specified')

        allNodes = []

        if pattern[0] == '.': # 类选择器
            clzName = pattern[1:]
            clz = getattr(ast, clzName)
            allNodes = astim.search(self.tree, filter=lambda nd: isinstance(nd, clz), order=order)
        else:
            raise SelectorErr('not support this pattern')

        return allNodes

    def A(self, pattern, order=0, action=None, **kwargs): # 根据pattern选择所有满足的节点并对每个节点进行action操作，action的参数是节点和kwargs
        allNodes = self.S(pattern, order=order)
        if action is not None:
            for node in allNodes:
                action(node, **kwargs)
        return allNodes

class SelectorErr(Exception):
    pass


