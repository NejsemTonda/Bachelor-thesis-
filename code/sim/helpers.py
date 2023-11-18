
class VecDict(dict):
    def __init__(self, d = {}):
        self.dict = d

    def __getitem__(self, key):
        h = hash((key.x, key.y))
        if h not in self.dict:
            self.dict[h] = []
        return self.dict[h]

    def __setitem__(self, key, value):
        h = hash((key.x, key.y))
        self.dict[h] = value
