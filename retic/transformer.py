import ast

class Transformer:
    """
    使用方式：subclass该类，然后对需要修改的节点设计visit_XXX函数即可，注意返回值是新的节点，对其他节点的默认访问方式是继续递归且不修改该节点
    """
    def __init__(self):
        self.currentNode = None

    def visit(self, node, *args, **kwargs):
        clzName = node.__class__.__name__
        meth = getattr(self, 'visit_' + clzName, None)
        if meth is None:
            # raise TransformerErr('this version does not support Python language feature: ' + clzName)
            return self.generic_visit(node) # 对于没有定义的visit函数，默认是继续递归访问，但不修改该节点

        self.currentNode = node
        return meth(node, *args, **kwargs)

    # 对于不需要修改的node，直接return self.generic_visit(node)即可
    def generic_visit(self, node):
        for field, old_value in ast.iter_fields(node):
            if isinstance(old_value, list):
                new_values = []
                for value in old_value:
                    if isinstance(value, ast.AST):
                        value = self.visit(value)
                        if value is None:
                            continue
                        elif not isinstance(value, ast.AST):
                            new_values.extend(value)
                            continue
                    new_values.append(value)
                old_value[:] = new_values
            elif isinstance(old_value, ast.AST):
                new_node = self.visit(old_value)
                if new_node is None:
                    delattr(node, field)
                else:
                    setattr(node, field, new_node)
        return node


class TransformerErr(Exception):
    pass