class Environment:
    def __init__(self):
        self.map = dict()
        self.outer = None

    def get(self, name):
        obj = self.map.get(name)
        if obj is None and self.outer is not None:
            obj = self.outer.get(name)

        return obj

    def set(self, name, val):
        self.map[name] = val
        return val


def new_enclosed_environment(outer):
    env = Environment()
    env.outer = outer
    return env


