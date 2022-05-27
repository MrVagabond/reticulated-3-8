
#### 关于ast的进一步封装，属于utils模块

import ast

###
#  _fields: tuple, name of fields in production
#  假设_fields = (f1, f2, f3)
#  那么node.f1, node.f2, node.f3即为对应的值，其类型是production中定义的类型
#  如果值是optional的，那么该值可以是None
#  如果值是zero-or-more的，那么该值是一个list
#  否则，每个值都是唯一的
#
###


def all_fields(node):
    return ast.iter_fields(node)

def children(node):
    return ast.iter_child_nodes(node)

# None if root, else an AST node
def add_parent(root_node):
    que = [root_node]
    root_node.retic_parent = None

    while len(que) > 0:
        node = que.pop(0)
        for n in children(node):
            que.append(n)
            n.retic_parent = node


def parent(node):
    return getattr(node, 'retic_parent') # raise an exception if not existed


#### 前序遍历得到list
def preorder(node):
    ret = []
    st = set() # set
    def visit(nd):
        if nd in st:
            return
        ret.append(nd)
        st.add(nd)
        for n in children(nd):
            visit(n)
    visit(node)
    return ret

#### 后序遍历得到list
def postorder(node):
    ret = []
    st = set()  # set

    def visit(nd):
        if nd in st:
            return
        for n in children(nd):
            visit(n)
        ret.append(nd)
        st.add(nd)

    visit(node)
    return ret


#### 搜索满足filter条件的所有节点
def search(tree, filter=lambda x: True, order='preorder'):
    ret = []
    searcher = None
    if order == 'preorder':
        searcher = preorder
    elif order == 'postorder':
        searcher = postorder
    else:
        raise AstimErr('order must be preorder or postorder')

    for node in searcher(tree):
        if filter(node):
            ret.append(node)
    return ret


class AstimErr(Exception):
    pass
