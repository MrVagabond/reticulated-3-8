
#### 完全独立的一个模块，用来定义类型系统的数据和接口
import sys


class Ty:
    pass

class TyPrim(Ty):
    pass
class TyInt(TyPrim):
    def __str__(self):
        return 'TyInt'
class TyBool(TyPrim):
    def __str__(self):
        return 'TyBool'
class TyStr(TyPrim):
    def __str__(self):
        return 'TyStr'

class TyDyn(Ty):
    def __str__(self):
        return 'TyDyn'

class TyBot(Ty): # 理论上需要这样的类型，不包含任何元素的类型，用于类型的交，但是不会提供给用户
    def __str__(self):
        return 'TyBot'

class TyNone(Ty):
    pass

class TyModule(Ty): # 不会提供给用户
    def __init__(self, allFieldType):
        # allFieldType是{str:Ty}的python字典
        self.allFieldType = allFieldType
    def __str__(self):
        # print(type(self.allFieldType))
        ret = 'TyModule(\n'
        for key, val in self.allFieldType.items():
            assert isinstance(val, TyFun)
            ret += key + ' = ' + str(val) + '\n'
        ret += ')'
        return ret
    def getAllFieldType(self):
        return self.allFieldType

class TyArg(Ty): # 参数需要单独开一个类型，因为一个函数的参数个数是任意的
    pass

# 参数个数固定的参数类型
class TyListArg(TyArg):
    def __init__(self, argTypeList, argNameList=None):
        self.argTypeList = argTypeList # python列表[Ty]
        if argNameList is None:
            self.argNameList = []
        else:
            self.argNameList = argNameList
    def __str__(self):
        ret = 'TyListArg('
        for t in self.argTypeList:
            ret += str(t) + ','
        if ret[-1] == ',': # 去掉多余的逗号
            ret = ret[:-1]
        ret += ')'
        return ret
    def setTypeOfIndex(self, index, argType):
        if index < 0 or index >= len(self.argTypeList):
            raise TySysErr('index overflow')
        self.argTypeList[index] = argType
    def getTypeOfIndex(self, index):
        if index < 0 or index >= len(self.argTypeList):
            raise TySysErr('index overflow')
        return self.argTypeList[index]

    def getArgTypeList(self):
        return self.argTypeList

    def getArgNameList(self):
        return self.argNameList

# class TyDictArg(TyArg): # 我们只管函数定义时每个参数的名字和类型，函数调用时的参数匹配问题不考虑
#     def __init__(self, *allArgName): # 可以直接TyDictArg()表示函数参数为空
#         self.allArgName = allArgName # a str tuple
#         self.typeOfArg = {} # a dict
#         for name in allArgName:
#             self.typeOfArg[name] = TyDyn()
#     def setTypeOfArg(self, argName, argType):
#         if argName not in self.allArgName:
#             raise TySysErr('bad argument name')
#         self.typeOfArg[argName] = argType
#     def getTypeOfArg(self, argName):
#         if argName not in self.allArgName:
#             raise TySysErr('bad argument name') # 还是严格一点吧
#         return self.typeOfArg[argName]


# 参数个数无法确定的参数类型
class TyDynArg(TyArg): # 函数的参数个数、每个参数的名字及其类型全部未知，相当于全部是TyDyn
    pass

class TyFun(Ty):
    def __init__(self, argType=None, bodyType=None, funName=None):
        # funName可以是None
        self.funName = funName
        if argType is None:
            self.argType = TyDynArg()
        else:
            self.argType = argType
        if bodyType is None:
            self.bodyType = TyDyn()
        else:
            self.bodyType = bodyType
    def __str__(self):
        return 'TyFun(' + str(self.argType) + '->' + str(self.bodyType) + ')'
    def setArgType(self, argType):
        self.argType = argType
    def setBodyType(self, bodyType):
        self.bodyType = bodyType
    def getArgType(self):
        return self.argType
    def getBodyType(self):
        return self.bodyType
    def getFunName(self):
        return self.funName

# class TyClass(Ty):
#     def __init__(self):
#         self.allFieldType = {}
#
# class TyInstance(Ty):
#     def __init__(self, classType=TyDyn()):
#         self.classType = classType

class TyContainer(Ty): # 同质容器类型;如果是异质容器类型，那么只能使用TyDyn
    pass

class TyList(TyContainer):
    def __init__(self, eltType=TyDyn()):
        self.eltType = eltType
    def __str__(self):
        return 'TyList[' + str(self.eltType) + ']'

class TyDict(TyContainer):
    def __init__(self, keyType=TyDyn(), valType=TyDyn()):
        self.keyType = keyType
        self.valType = valType
    def __str__(self):
        return 'TyDict[' + str(self.keyType) + ',' + str(self.valType) + ']'

class TyTuple(TyContainer):
    def __init__(self, eltType=TyDyn()):
        self.eltType = eltType
    def __str__(self):
        return 'TyTuple[' + str(self.eltType) + ']'

class TySet(TyContainer):
    def __init__(self, eltType=TyDyn()):
        self.eltType = eltType
    def __str__(self):
        return 'TySet[' + str(self.eltType) + ']'


# type system utility functions

def str2type(type_name):
    type_name = type_name.replace(' ', '') # 去掉所有空格

    for name in ['Bool', 'Int', 'Str', 'None', 'Dyn']:
        if type_name == name:
            ty = getattr(sys.modules[__name__], 'Ty' + name)
            return ty()
    for name in ['List', 'Tuple', 'Set']:
        if type_name[0:len(name)] == name:
            ty = getattr(sys.modules[__name__], 'Ty' + name)
            return ty(eltType=str2type(type_name[len(name)+1 : -1]))
    for name in ['Dict']:
        if type_name[0:len(name)] == name:
            ty = getattr(sys.modules[__name__], 'Ty' + name)
            return ty( keyType=str2type(type_name[len(name)+1 : type_name.find(',')]), # 非常朴素，只允许嵌套一层，后面考虑任意的parse
                       valType=str2type(type_name[type_name.find(',')+1 : -1]))

    # Fun[Dyn,Int], Fun[Pos(Int,Bool),Str]
    for name in ['Fun']:
        if type_name[0:len(name)] == name:
            ty = getattr(sys.modules[__name__], 'Ty' + name)
            if type_name[len(name)+1 : type_name.find(',')] == 'Dyn':
                return ty( argType=TyDynArg(), bodyType=str2type(type_name[type_name.find(',')+1 : -1]))
            elif type_name[len(name)+1 : len(name)+4] == 'Pos':
                # 解析所有位置参数的类型和返回值的类型
                argTypes = type_name[8 : type_name.rfind(',') - 1].split(',') # 非常朴素，只允许嵌套一层，后面考虑任意的parse
                return ty( argType=TyListArg([str2type(at) for at in argTypes]), bodyType=str2type(type_name[type_name.rfind(',')+1 : -1]))

    raise TySysErr('bad type string: ' + type_name)

def typeEq(ty1, ty2): # 结构等价
    if isinstance(ty1, TyInt) and isinstance(ty2, TyInt):
        return True
    elif isinstance(ty1, TyBool) and isinstance(ty2, TyBool):
        return True
    elif isinstance(ty1, TyStr) and isinstance(ty2, TyStr):
        return True
    elif isinstance(ty1, TyNone) and isinstance(ty2, TyNone):
        return True
    elif isinstance(ty1, TyDyn) and isinstance(ty2, TyDyn):
        return True
    elif isinstance(ty1, TyFun) and isinstance(ty2, TyFun):
        return typeEq(ty1.getArgType(), ty2.getArgType()) and typeEq(ty1.getBodyType(), ty2.getBodyType())
    elif isinstance(ty1, TyList) and isinstance(ty2, TyList):
        return typeEq(ty1.eltType, ty2.eltType)
    elif isinstance(ty1, TyTuple) and isinstance(ty2, TyTuple):
        return typeEq(ty1.eltType, ty2.eltType)
    elif isinstance(ty1, TySet) and isinstance(ty2, TySet):
        return typeEq(ty1.eltType, ty2.eltType)
    elif isinstance(ty1, TyDict) and isinstance(ty2, TyDict):
        return typeEq(ty1.keyType, ty2.keyType) and typeEq(ty1.valType, ty2.valType)
    else:
        return False

def typeConsistent(ty1, ty2):
    if typeEq(ty1, ty2):
        return True
    else:
        if isinstance(ty1, TyDyn) or isinstance(ty2, TyDyn):
            return True
        elif isinstance(ty1, TyFun) and isinstance(ty2, TyFun):
            # 下面的实现是不对的，但规则是这个规则
            return typeConsistent(ty1.argType, ty2.argType) and typeConsistent(ty1.bodyType, ty2.bodyType)
        else:
            return False

def typeJoin(ty1, ty2): # 子类型
    if typeEq(ty1, ty2):
        return ty1
    else:
        if isinstance(ty1, TyList) and isinstance(ty2, TyList):
            return TyList(typeJoin(ty1.eltType, ty2.eltType))
        elif isinstance(ty1, TyTuple) and isinstance(ty2, TyTuple):
            return TyTuple(typeJoin(ty1.eltType, ty2.eltType))
        elif isinstance(ty1, TySet) and isinstance(ty2, TySet):
            return TySet(typeJoin(ty1.eltType, ty2.eltType))
        elif isinstance(ty1, TyDict) and isinstance(ty2, TyDict):
            return TyDict(keyType=typeJoin(ty1.keyType, ty2.keyType), valType=typeJoin(ty1.valType, ty2.valType))
        elif isinstance(ty1, TyFun) and isinstance(ty2, TyFun):
            # join出来的类型应该在两个类型的使用场景下也能被安全使用，所以它应该接受两个类型的所有参数，返回两个返回值类型的公共部分
            # 也就是说join出来的类型是两个类型的子类型
            raise TySysErr('别搞这些东西，到时候你自己都拎不清')
            # return TyFun(argType=TyDyn, bodyType=typeJoin(ty1.bodyType, ty2.bodyType))
        else:
            return TyDyn()

def typeMeet(ty1, ty2): # 父类型
    if typeEq(ty1, ty2):
        return ty1
    else:
        return TyBot() # 无脑做法

def fun_match(ty):
    if isinstance(ty, TyFun):
        return ty
    elif isinstance(ty, TyDyn):
        return TyFun(argType=TyDynArg(), bodyType=TyDyn())
    else:
        raise TySysErr('bad function matching relation')


class TypingEnv(object):
    def __init__(self, copyFrom=None):
        # copyFrom应该是另一个TypingEnv实例
        if copyFrom is None:
            self.env = {}
        else:
            self.env = copyFrom.getAll().copy()

    def put(self, name, ty):
        self.env[name] = ty

    def get(self, name):
        ret_type = self.env.get(name, None)
        if ret_type is None:
            from . import typing_builtin
            builtin_type = typing_builtin.builtin_functions(name)
            if builtin_type is None:
                return TyDyn() # 不报错，而是沉默、保守处理
            else:
                return builtin_type
        else:
            return ret_type


    def getAll(self):
        return self.env

    def isEmpty(self):
        return len(self.env) == 0




class TySysErr(Exception):
    pass

