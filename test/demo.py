from typing import *
from add import zero, add

def transform(lst:List[int], f:Callable[[int],int]) -> List[int]:
    res: List[int] = []
    for e in lst:
        res.append(f(e))    # 当不知道f的target时，就无法进入，只能当做黑盒
                            # 但其实运行时是知道target的，f.__name__即可，只是静态时不知道罢了
    return res

def foo(x):
    x = add(zero(), x)
    return x + "hello"

def foo2(x:int):
    return x * "hello"

# 在transform函数内部进行运行时检查，[1,2,3]符合List[int]类型，f暂时不符合该类型，但是相容的，所以放到其调用处进行检查
# 在foo函数内部进行运行时检查，传入的int类型无法和str类型相容，所以blame的位置在transform传入e参数处？
print(transform([1,2,3], foo))
# 在transform函数内部进行运行时检查，[1,2,3]符合List[int]类型，f暂时不符合该类型，但是相容的，所以放到其调用处进行检查
# 在foo2函数内部进行运行时检查，传入的int类型和str类型相容，执行foo2函数
# 发现其返回值不符合int类型，所以blame的位置在transform调用f返回处？
print(transform([1,2,3], foo2))