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
            [(0,5+e), (6,5+e), (6,0)],
            anchors=[vec2(6,5), vec2(6, 3)] 
        )
        env.add_ground(
            [(20,5+e), (14,5+e), (14,0)],
            anchors=[vec2(14,5), vec2(14, 3)] 
        )
        
        car = env.add_car(vec2(2.5,5.5+e), density=3)

        goal = vec2(19,6)

        x_bounds = (0,20)
        y_bounds = (0,15)

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
            [(0,5+e), (6,5+e), (6,0)],
            anchors=[vec2(6,5), vec2(6, 3),
                vec2(2, 14), vec2(6, 14),
                vec2(2, 13), vec2(14, 13),
                vec2(2, 12), vec2(16, 12),
           ]
        )
        env.add_ground(
            [(20,5+e), (14,5+e), (14,0)],
            anchors=[vec2(14,5), vec2(14, 3)] 
        )
        env.add_road(vec2(2,14), vec2(4,14))
        env.add_road(vec2(4,14), vec2(6,14))

        env.add_plank(vec2(2,13), vec2(4,13))
        env.add_plank(vec2(4,13), vec2(6,13))
        env.add_plank(vec2(6,13), vec2(8,13))
        env.add_plank(vec2(8,13), vec2(10,13))
        env.add_plank(vec2(10,13),vec2(12,13))
        env.add_plank(vec2(12,13),vec2(14,13))
        env.add_plank(vec2(2,12), vec2(4,12))
        env.add_plank(vec2(4,12), vec2(6,12))
        env.add_plank(vec2(6,12), vec2(8,12))
        env.add_plank(vec2(8,12), vec2(10,12))
        env.add_plank(vec2(10,12),vec2(12,12))
        env.add_plank(vec2(12,12),vec2(14,12))
        env.add_plank(vec2(14,12),vec2(16,12))

        car = env.add_car(vec2(5,5.5+e), density=3)

        goal = vec2(19,6)

        x_bounds = (0,20)
        y_bounds = (0,15)

        return Level(env, car, goal, x_bounds, y_bounds)

