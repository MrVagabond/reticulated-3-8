def get_first(l:'List[Int]') -> 'Int':
    return l[0]

def apply(x:'Int', f:'Fun[Pos(Int),Int]') -> 'Int':
    return f(x)