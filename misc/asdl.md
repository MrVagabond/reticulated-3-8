```asdl
mod = Module(stmt* body, type_ignore *type_ignores)
stmt = FunctionDef(identifier name, arguments args,
                       stmt* body, expr* decorator_list, expr? returns,
                       string? type_comment)
          | Return(expr? value)
          | Delete(expr* targets)
          | Assign(expr* targets, expr value, string? type_comment)
          | AugAssign(expr target, operator op, expr value)
          | For(expr target, expr iter, stmt* body, stmt* orelse, string? type_comment)
          | If(expr test, stmt* body, stmt* orelse)
          | With(withitem* items, stmt* body, string? type_comment)
          | Global(identifier* names)
          | Nonlocal(identifier* names)
          | Expr(expr value)
          | Pass | Break | Continue
expr = BoolOp(boolop op, expr* values)
            | NamedExpr(expr target, expr value)
            | BinOp(expr left, operator op, expr right)
            | UnaryOp(unaryop op, expr operand)
            | Lambda(arguments args, expr body)
            | IfExp(expr test, expr body, expr orelse)
            | Dict(expr* keys, expr* values)
            | Set(expr* elts)
            | ListComp(expr elt, comprehension* generators)
            | SetComp(expr elt, comprehension* generators)
            | DictComp(expr key, expr value, comprehension* generators)
            | GeneratorExp(expr elt, comprehension* generators)
            | Yield(expr? value)
            | YieldFrom(expr value)
            | Compare(expr left, cmpop* ops, expr* comparators)
            | Call(expr func, expr* args, keyword* keywords)
            | Constant(constant value, string? kind)
            | Attribute(expr value, identifier attr, expr_context ctx)
            | Subscript(expr value, slice slice, expr_context ctx)
            | Starred(expr value, expr_context ctx)
            | Name(identifier id, expr_context ctx)
            | List(expr* elts, expr_context ctx)
            | Tuple(expr* elts, expr_context ctx)
```



## informal and formal semantics for each node

`类型`是程序`值`的抽象解释（即运行时值的静态保守估计），所以凡是拥有`值`这一属性的程序元素，都需要为其`定型`。

由于`Python`的所有对象都有`值`，所以需要为所有对象都`定型`，因此有些类型看起来就比较奇怪。

具有结构化特征的值对应着结构化类型



令$\Sigma$表示全局的类型环境



```
mod = Module(stmt* body, type_ignore *type_ignores)
```

模块是一个对象，它的值是什么？在交互模式下值是形如`<module 'ast' from 'D:\\Python\\python3.8\\lib\\ast.py'>`的字符串，这太过于抽象，导致没什么用，我们关心的是模块中有哪些可以被访问的接口，因此模块类型需要设计地更加informative一点。所以模块的值应该是一个结构，里面包含着接口及其类型。一个Python程序可以简洁地看做是若干个模块的组合。



```
FunctionDef(identifier name, arguments args,
                       stmt* body, expr* decorator_list, expr? returns,
                       string? type_comment)
```

函数定义，在当前scope中的函数对象，它的值是什么？在交互模式下值是形如`function func at 0x000002179806D280`的字符串，同理，函数的值也应该是一个结构，包含参数值类型、返回值类型。



```
Return(expr? value)
```

对$\Sigma$不产生影响，但应该检查值类型与标注一致



```
Delete(expr* targets)
```

对$\Sigma$不产生影响



```
Assign(expr* targets, expr value, string? type_comment)
```





```
Assign(expr* targets, expr value, string? type_comment)
```



```
AugAssign(expr target, operator op, expr value)
```



```
For(expr target, expr iter, stmt* body, stmt* orelse, string? type_comment)
```



```
If(expr test, stmt* body, stmt* orelse)
```



```
With(withitem* items, stmt* body, string? type_comment)
```



```
Global(identifier* names)
```



```
Nonlocal(identifier* names)
```



```
Expr(expr value)
```



```
Pass | Break | Continue
```





```asdl
expr = BoolOp(boolop op, expr* values)
            | NamedExpr(expr target, expr value)
            | BinOp(expr left, operator op, expr right)
            | UnaryOp(unaryop op, expr operand)
            | Lambda(arguments args, expr body)
            | IfExp(expr test, expr body, expr orelse)
            | Dict(expr* keys, expr* values)
            | Set(expr* elts)
            | ListComp(expr elt, comprehension* generators)
            | SetComp(expr elt, comprehension* generators)
            | DictComp(expr key, expr value, comprehension* generators)
            | GeneratorExp(expr elt, comprehension* generators)
            | Yield(expr? value)
            | YieldFrom(expr value)
            | Compare(expr left, cmpop* ops, expr* comparators)
            | Call(expr func, expr* args, keyword* keywords)
            | Constant(constant value, string? kind)
            | Attribute(expr value, identifier attr, expr_context ctx)
            | Subscript(expr value, slice slice, expr_context ctx)
            | Starred(expr value, expr_context ctx)
            | Name(identifier id, expr_context ctx)
            | List(expr* elts, expr_context ctx)
            | Tuple(expr* elts, expr_context ctx)
```

