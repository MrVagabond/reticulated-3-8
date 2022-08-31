from typing import *

def add(a:int, b:int=1) -> int:
    c = a + b + 1
    return c


x = add(a=1, b=2)
y = add(1, b=2)
z = add(1, 2)
m = add(1)