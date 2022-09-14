from typing import *

def func(lst: List[int]) -> int:
    sums:int = 10
    while sums < 100:
        n = lst[0] # refactor
        sums += n
    return sums