from sim.environment import Environment
from sim.components import Car
from Box2D.b2 import vec2
from dataclasses import dataclass

e = 0.1
@dataclass
class Level:
    env: Environment
    car: Car
    goal: vec2
    x_bounds: vec2
    y_bounds: vec2



class LevelFactory:
    def level1():
        env = Environment()
        env.add_ground(
            [(0,10+e), (12,10+e), (12,0)],
            anchors=[vec2(12,10), vec2(12, 6)] 
        )
        env.add_ground(
            [(40,10+e), (28,10+e), (28,0)],
            anchors=[vec2(28,10), vec2(28, 6)] 
        )
        
        car = env.add_car(vec2(5,11+e), density=3)

        goal = vec2(38,12)

        x_bounds = (0,40)
        y_bounds = (0,30)

        return Level(env, car, goal, x_bounds, y_bounds)

    def level2():
        pass

    def level3():
        pass

    def level4():
        pass

    def level5():
        pass

    def test():
        env = Environment()
        env.add_ground(
            [(0,10+e), (12,10+e), (12,0)],
            anchors=[vec2(12,10), vec2(12, 6)]#, vec2(20, 10)] 
        )
        env.add_ground(
            [(40,10+e), (28,10+e), (28,0)],
            anchors=[vec2(28,10), vec2(28, 6)] 
        )
        
        car = env.add_car(vec2(5,11+e), density=3)

        goal = vec2(38,12)

        x_bounds = (0,40)
        y_bounds = (0,30)

        return Level(env, car, goal, x_bounds, y_bounds)

