

__all__ = ['FuncTypeRecorder']

class Env:
    def __init__(self):
        self.env:dict = {}
    def put(self, key, val):
        if self.env.get(key) is None:
            self.env[key] = val
        else:
            raise EnvException('重复加入函数')
    def get(self, key):
        return self.env.get(key)

class FuncTypeRecorder(Env):
    pass


class EnvException(Exception):
    pass
