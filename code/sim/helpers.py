from Box2D.b2 import vec2
class VecDict(dict):
    def __getitem__(self, key):
        h = hash((key.x, key.y))
        return super().__getitem__(h) 

    def __setitem__(self, key, value):
        h = hash((key.x, key.y))
        super().__setitem__(h, value)

    def __contains__(self, key):
        h = hash((key.x, key.y))
        return super().__contains__(h)



if __name__ == "__main__":
    d = VecDict()
    d[vec2(1,1)] = 1
    print(d[vec2(1,1)])
    print(vec2(1,1) in d)
