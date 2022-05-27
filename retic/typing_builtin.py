from . import tysys

#### 基本类型
Int = tysys.TyInt
Bool = tysys.TyBool
Str = tysys.TyStr
Dyn = tysys.TyDyn
TyNone = tysys.TyNone

#### 函数类型
Function = tysys.TyFun
DynArg = tysys.TyDynArg
PosArg = tysys.TyListArg

#### 容器类型
List = tysys.TyList
Dict = tysys.TyDict
Tuple = tysys.TyTuple
Set = tysys.TySet



s2s = Function(PosArg([]), Str())
s2b = Function(PosArg([]), Bool())

#### 全部按字典序排列，完全遵照python3.8内置类型的规约


def basics(me): # object具有的所有字段，共23个，相比于python3.5多了1个__init_subclass__
    return {
        '__class__': Dyn(),
        '__delattr__': Function(PosArg([Str()]), TyNone()),
        '__dir__': Function(PosArg([]), Dict(Str(), Dyn())),
        '__doc__': Str(),
        '__eq__': Function(PosArg([me]), Bool()),
        '__format__': Function(DynArg(), Str()),
        '__ge__': Function(PosArg([me]), Bool()),
        '__getattribute__': Function(DynArg(), Dyn()),
        '__gt__': Function(PosArg([me]), Bool()),
        '__hash__': Function(PosArg([]), Int()),
        '__init__': Function(DynArg(), TyNone()),
        '__init_subclass__': Dyn(), # __init_subclass__
        '__le__': Function(PosArg([me]), Bool()),
        '__lt__': Function(PosArg([me]), Bool()),
        '__ne__': Function(PosArg([me]), Bool()),
        '__new__': Function(DynArg(), me),
        '__reduce__': Function(DynArg(), Dyn()),
        '__reduce_ex__': Function(DynArg(), Dyn()),
        '__repr__': Function(PosArg([]), Str()),
        '__setattr__': Function(DynArg(), TyNone()),
        '__sizeof__': Function(PosArg([]), Int()),
        '__str__': Function(PosArg([]), Str()),
        '__subclasshook__': Function(DynArg(), Dyn())
    }


intfields = basics(Int()) # int类型在object的基础上多了48个字段，少了47个字段
# __abs__
# __add__
# __and__
# __bool__
# __ceil__
# __divmod__
# __float__
# __floor__
# __floordiv__
# __getnewargs__
# __index__
# __int__
# __invert__
# __lshift__
# __mod__
# __mul__
# __neg__
# __or__
# __pos__
# __pow__
# __radd__
# __rand__
# __rdivmod__
# __rfloordiv__
# __rlshift__
# __rmod__
# __rmul__
# __ror__
# __round__
# __rpow__
# __rrshift__
# __rshift__
# __rsub__
# __rtruediv__
# __rxor__
# __sub__
# __truediv__
# __trunc__
# __xor__
# as_integer_ratio
# bit_length
# conjugate
# denominator
# from_bytes
# imag
# numerator
# real
intfields['to_bytes'] = Function(DynArg(), Dyn())

boolfields = basics(Bool())

nonefields = basics(TyNone()) # None类型在object的基础上多了一个字段
nonefields['__bool__'] = s2b

strfields = basics(Str())
strfields.update({ # str类型在object的基础上多了55个字段，少了3个字段
    'capitalize': s2s,
    'casefold': s2s,
    'center': Function(DynArg(), Str()),  # int x str?
    'count': Function(PosArg([Str()]), Int()),
    'encode': Function(DynArg(), Str()),  # str x str?
    'endswith': Function(DynArg(), Bool()),  # str x int?
    'expandtabs': Function(PosArg([Int()]), Str()),
    'find': Function(DynArg(), Int()),  # ??
    'format': Function(DynArg(), Str()),  # ??
    'format_map': Function(PosArg([Dyn()]), Str()),
    'index': Function(PosArg([Str()]), Int()),
    'isalnum': s2b,
    'isalpha': s2b,
    'isascii': s2b, # isascii
    'isdecimal': s2b,
    'isdigit': s2b,
    'isidentifier': s2b,
    'islower': s2b,
    'isnumeric': s2b,
    'isprintable': s2b,
    'isspace': s2b,
    'istitle': s2b,
    'isupper': s2b,
    # 'join': Function(PosArg([HTuple(Str())]), Str()),
    'ljust': Function(DynArg(), Str()),  # int x str?
    'lower': s2s,
    'lstrip': Function(DynArg(), Str()),  # str?
    'maketrans': Function(DynArg(), Dyn()),  # ??
    # 'partition': Function(PosArg([Str()]), HTuple(Str())),
    'replace': Function(DynArg(), Str()),  # str * str * int?
    'rfind': Function(DynArg(), Int()),  # ??
    'rindex': Function(PosArg([Str()]), Int()),
    'rjust': Function(DynArg(), Str()),  # int x str?
    # 'rpartition': Function(PosArg([Str()]), HTuple(Str())),
    'rsplit': Function(DynArg(), List(Str())),  # str?
    'rstrip': Function(DynArg(), Str()),  # str?
    'split': Function(DynArg(), List(Str())),  # str?
    'splitlines': Function(DynArg(), List(Str())),  # int?
    'startswith': Function(DynArg(), Bool()),  # str x int?
    'strip': Function(DynArg(), Str()),  # str?
    'swapcase': s2s,
    'title': s2s,
    'translate': Dyn(), # translate
    'upper': s2s,
    'zfill': Function(PosArg([Int()]), Str())
})
strfields['__add__'] = Function(PosArg([Str()]), Str())
strfields['__contains__'] = Function(PosArg([Str()]), Bool())
strfields['__getitem__'] = Function(DynArg, Str())
strfields['__getnewargs__'] = Function(PosArg([]), Tuple(Str()))
strfields['__iter__'] = Dyn()
strfields['__len__'] = Function(PosArg([]), Int()) # __len__
strfields['__mod__'] = Function(PosArg([Dyn()]), Str())
strfields['__mul__'] = Function(PosArg([Int()]), Str())
strfields['__rmod__'] = Function(PosArg([Dyn()]), Str())
strfields['__rmul__'] = Function(PosArg([Int()]), Str())


def modfields(me): # module类型只在object的基础上多了1个字段
    ret = basics(me)
    ret['__dict__'] = Dict(Str(), Dyn())
    return ret


def funcfields(me):  # function类型在object的基础上多了12个字段
    ret = basics(me)
    ret['__annotations__'] = Dict(Str(), Dyn())
    ret['__call__'] = me
    ret['__closure__'] = Dyn()
    ret['__code__'] = Dyn()
    ret['__defaults__'] = Dyn()
    ret['__dict__'] = Dict(Str(), Dyn())
    ret['__get__'] = Function(DynArg(), Function(DynArg(), me.to))
    ret['__globals__'] = Dict(Str(), Dyn())
    ret['__kwdefaults__'] = Dyn()
    ret['__module__'] = Str()
    ret['__name__'] = Str()
    ret['__qualname__'] = Str()
    return ret


def dictfields(me): # dict类型在object的基础上多了18个字段，少了2个
    ret = basics(me)
    ret['__contains__'] = Function(PosArg([me.keys]), Bool())
    ret['__delitem__'] = Function(PosArg([me.keys]), TyNone())
    ret['__getitem__'] = Function(DynArg, me.values)
    ret['__iter__'] = Dyn()
    ret['__len__'] = Function(PosArg([]), Int()) # __len__
    ret['__reversed__'] = Function(PosArg([]), me) # __reversed__
    ret['__setitem__'] = Function(PosArg([me.keys, me.values]), TyNone())
    ret['clear'] = Function(PosArg([]), TyNone())
    ret['copy'] = Function(PosArg([]), me)
    ret['fromkeys'] = Function(DynArg(), Dyn())
    ret['get'] = Function(DynArg(), me.values)
    ret['items'] = Function(PosArg([]), List(Tuple(me.keys, me.values)))
    ret['keys'] = Function(PosArg([]), List(me.keys))
    ret['pop'] = Function(DynArg(), me.values)
    ret['popitem'] = Function(PosArg([]), Tuple(me.keys, me.values))
    ret['setdefault'] = Function(DynArg(), Dyn())
    ret['update'] = Function(PosArg([me]), TyNone())
    ret['values'] = Function(PosArg([]), Dyn())
    return ret


def setfields(me): # set类型在object的基础上多了32个字段，少了1个
    ret = basics(me)
    ret['__and__'] = Function(PosArg([me]), me)
    ret['__contains__'] = Function(PosArg([me.elts]), Bool())
    ret['__iand__'] = Function(PosArg([me]), me)
    ret['__ior__'] = Function(PosArg([me]), me)
    ret['__isub__'] = Function(PosArg([me]), me)
    ret['__iter__'] = Dyn()
    ret['__ixor__'] = Function(PosArg([me]), me)
    ret['__len__'] = Function(PosArg([]), Int())
    ret['__or__'] = Function(PosArg([me]), me)
    ret['__rand__'] = Function(PosArg([me]), me)
    ret['__ror__'] = Function(PosArg([me]), me)
    ret['__rsub__'] = Function(PosArg([me]), me)
    ret['__rxor__'] = Function(PosArg([me]), me)
    ret['__sub__'] = Function(PosArg([me]), me)
    ret['__xor__'] = Function(PosArg([me]), me) # __xor__
    ret['add'] = Function(PosArg([me.elts]), TyNone())
    ret['clear'] = Function(PosArg([]), TyNone())
    ret['copy'] = Function(PosArg([]), me)
    ret['difference'] = Function(DynArg(), me)
    ret['difference_update'] = Function(DynArg(), TyNone())
    ret['discard'] = Function(PosArg([me.elts]), TyNone())
    ret['intersection'] = Function(DynArg(), me)
    ret['intersection_update'] = Function(DynArg(), TyNone())
    ret['isdisjoint'] = Function(PosArg([me]), Bool())
    ret['issubset'] = Function(PosArg([me]), Bool())
    ret['issuperset'] = Function(PosArg([me]), Bool())
    ret['pop'] = Function(PosArg([]), me.elts)
    ret['remove'] = Function(PosArg([me.elts]), TyNone())
    ret['symmetric_difference'] = Function(DynArg(), me)
    ret['symmetric_difference_update'] = Function(DynArg(), TyNone())
    ret['union'] = Function(DynArg(), me)
    ret['update'] = Function(DynArg(), TyNone())
    return ret


def listfields(me): # list类型在object的基础上多了23个字段
    listfields = basics(me)
    listfields.update({
        # __add__
        # __contains__
        # __delitem__
        # __getitem__
        # __iadd__
        # __imul__
        # __iter__
        # __len__
        # __mul__
        # __reversed__
        # __rmul__
        # __setitem__
        'append': Function(PosArg([me.elts]), TyNone()),
        'clear': Function(PosArg([]), TyNone()),
        'copy': Function(PosArg([]), List(me.elts)),
        'count': Function(PosArg([me.elts]), Int()),
        'extend': Function(PosArg([me]), List(me.elts)),
        'index': Function(PosArg([me.elts]), Int()),
        'insert': Function(PosArg([Int(), me.elts]), TyNone()),
        'pop': Function(DynArg(), me.elts),
        'remove': Function(PosArg([me.elts]), TyNone()),
        'reverse': Function(PosArg([]), TyNone()),
        'sort': Function(DynArg(), TyNone())
    })
    return listfields


def tuplefields(me):
    pass

# 6个未知标识符
# __build_class__
# __doc__
# __loader__
# __name__
# __package__
# __spec__

# 6个内置常量
# __debug__
# copyright
# credits
# exit
# license
# quit

# 69个内置函数
def builtin_functions(name):
    all = {}
    all.update({
        'abs' : Function(PosArg([Int()]),Int()),
        'all' : Function(PosArg([Dyn()]),Bool()),
        'any' : Function(PosArg([Dyn()]),Bool()),
        'ascii' : Function(PosArg([Dyn()]),Str()),
        'bin' : Function(PosArg([Int()]),Str()),
        'bool' : Function(PosArg([Dyn()]),Bool()),
        'breakpoint' : Dyn(),
        'bytearray' : Dyn(),
        'bytes' : Dyn(),
        'callable' : Function(PosArg([Dyn]),Bool),
        'chr' : Function(PosArg([Int]),Str),
        'classmethod' : Dyn(),
        'compile' : Dyn(),
        'complex' : Dyn(),
        'delattr' : Dyn(),
        'dict' : Function(DynArg(),Dict()),
        'dir' : Function(PosArg([Dyn]),List(Str)),
        'divmod' : Dyn(),
        'enumerate' : Dyn(),
        'eval' : Dyn(),
        'exec' : Dyn(),
        'filter' : Dyn(), # 不足以描述
        'float' : Dyn(), # 不足以描述
        'format' : Dyn(),
        'frozenset' : Function(PosArg([Dyn]),Set), # 可行吗？
        'getattr' : Dyn(),
        'globals' : Function(PosArg([]),Dict(Str(),Dyn())),
        'hasattr' : Function(PosArg([Dyn(),Str()]),Bool()),
        'hash' : Function(PosArg([Dyn]),Int()),
        'help' : Dyn(),
        'hex' : Function(PosArg([Int()]),Str()),
        'id' : Dyn(),
        'input' : Dyn(),
        'int' : Function(DynArg(),Int()),
        'isinstance' : Function(PosArg([Dyn(),Dyn()]),Bool()),
        'issubclass' : Function(PosArg([Dyn(),Dyn()]),Bool()),
        'iter' : Dyn(),
        'len' : Function(PosArg([Dyn()]),Int()),
        'list' : Function(PosArg([Dyn()]),List(Dyn())),
        'locals' : Function(PosArg([]),Dict(Str(),Dyn())),
        'map' : Dyn(),
        'max' : Dyn(),
        'memoryview' : Dyn(),
        'min' : Dyn(),
        'next' : Dyn(),
        'object' : Dyn(),
        'oct' : Function(PosArg([Int()]),Str()),
        'open' : Dyn(),
        'ord' : Function(PosArg([Str()]),Int()),
        'pow' : Dyn(), # 不足以描述
        'print' : Dyn(),
        'property' : Dyn(),
        'range' : Dyn(),
        'repr' : Function(PosArg([Dyn()]),Str()),
        'reversed' : Dyn(),
        'round' : Dyn(),
        'set' : Function(PosArg([Dyn()]),Set(Dyn())),
        'setattr' : Dyn(),
        'slice' : Dyn(),
        'sorted' : Dyn(),
        'staticmethod' : Dyn(),
        'str' : Function(DynArg(),Str()),
        'sum' : Dyn(),
        'super' : Dyn(),
        'tuple' : Function(PosArg([Dyn()]),Tuple(Dyn())),
        'type' : Dyn(),
        'vars' : Dyn(),
        'zip' : Dyn(),
        '__import__' : Dyn(),
    })
    return all.get(name, None)
