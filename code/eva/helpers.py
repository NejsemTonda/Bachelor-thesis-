import numpy 

def pol2cart(l, alpha):
        x = l * np.cos(alpha)
        y = l * np.sin(alpha)
        return(x, y)
