import numpy as np
from Box2D.b2 import vec2

def pol2cart(l, alpha):
        x = l * np.cos(alpha)
        y = l * np.sin(alpha)
        return(x, y)

def get_possible_points(points, max_len=2.05):
        possible = []
        max_x = int(max([p[0] for p in points])+max_len)*4 
        min_x = int(min([p[0] for p in points])-max_len)*4 
        max_y = int(max([p[1] for p in points])+max_len)*4 
        min_y = int(min([p[1] for p in points])-max_len)*4 
        for x in range(min_x, max_x+1):
            for y in range(min_y, max_y+1):
                for p in points:
                    l = (vec2(x/4,y/4)-vec2(p)).length 
                    if l > max_len or l < 0.1:
                        break
                else:
                    possible.append((x/4,y/4))    
        return possible

