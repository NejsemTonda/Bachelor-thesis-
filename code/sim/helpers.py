from Box2D.b2 import vec2
import math

class VecDict(dict):
    def __getitem__(self, key):
        h = (key.x, key.y)
        return super().__getitem__(h) 

    def __setitem__(self, key, value):
        h = (key.x, key.y)
        super().__setitem__(h, value)

    def __contains__(self, key):
        h = (key.x, key.y)
        return super().__contains__(h)

SCALER = 4
def correctLen(start, end, max_len):
    diff = end-start
    if diff.lengthSquared > max_len**2:
        angle = math.atan2(diff.y, diff.x)
        end = start+vec2(math.cos(angle), math.sin(angle))*max_len
    x = math.floor(SCALER*end.x)/SCALER if diff.x > 0 else math.ceil(SCALER*end.x)/SCALER
    y = math.floor(SCALER*end.y)/SCALER if diff.y > 0 else math.ceil(SCALER*end.y)/SCALER
    return vec2(x,y)





if __name__ == "__main__":
    import random
    import time
    d = VecDict()
    d[vec2(1,1)] = 1
    print(d[vec2(1,1)])
    print(vec2(1,1) in d)
    print(d.keys())
    quit()
    s = time.time()
    for _ in range(100000):
        v1 = vec2(random.randint(0,20),random.randint(0,20))
        v2 = vec2(random.randint(0,20),random.randint(0,20))
        k = correctLen(v1, v2, 10)

    print(time.time() -s)
