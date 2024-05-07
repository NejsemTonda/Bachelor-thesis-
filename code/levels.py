from sim.environment import Environment
from sim.components import Car
from Box2D.b2 import vec2
from dataclasses import dataclass

citi_car = 6 #3 in Poly Bridge
station_vagon = 5 * citi_car/3 # 5 in Poly Bridge
surfer_van = 6.5 * citi_car/3# 6.5 in Poly Bridge

e = 0.05
@dataclass
class Level:
    env: Environment
    car: Car
    goal: vec2
    x_bounds: vec2
    y_bounds: vec2
    left_side: int
    right_side: int



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
        
        car = env.add_car(vec2(2.5,5.5+e), density=station_vagon)

        goal = vec2(19,5.75577)

        x_bounds = vec2(0,20)
        y_bounds = vec2(0,15)
        left = 0
        right = 2

        return Level(env, car, goal, x_bounds, y_bounds, left, right)

    def level2():
        env = Environment()
        env.add_ground(
            [(0,5+e), (5,5+e), (5,0)],
            anchors=[vec2(5,5)] 
        )
        env.add_ground(
            [(20,5+e), (15,5+e), (15,0)],
            anchors=[vec2(15,5), vec2(10, 2)] 
        )

        car = env.add_car(vec2(1,5.5+e), density=citi_car)
        env.add_car(vec2(3.5,5.5+e), density=citi_car)

        goal = vec2(19,5.75577)

        x_bounds = vec2(0,20)
        y_bounds = vec2(0,15)

        left = 0
        right = 1

        return Level(env, car, goal, x_bounds, y_bounds, left, right)

    def level3():
        env = Environment()
        env.add_ground(
            [(-5,5+e), (4,5+e), (4,0)],
            anchors=[vec2(4,5), vec2(8, 2.5)] 
        )
        env.add_ground(
            [(20,5+e), (16,5+e), (16,0)],
            anchors=[vec2(16,5), vec2(12, 2.5)] 
        )

        car = env.add_car(vec2(0,5.5+e), density=station_vagon)
        env.add_car(vec2(2.5,5.5+e), density=citi_car)

        goal = vec2(19,5.75577)

        x_bounds = vec2(0,20)
        y_bounds = vec2(0,15)

        left = 0
        right = 2

        return Level(env, car, goal, x_bounds, y_bounds, left, right)



    def level4():
        env = Environment()
        env.add_ground(
            [(-5,3+e), (6,3+e), (6,0)],
            anchors=[vec2(6,3)] 
        )
        env.add_ground(
            [(20,5+e), (14,5+e), (14,0)],
            anchors=[vec2(14,5)] 
        )
        car = env.add_car(vec2(3,3.5+e), density=surfer_van)

        goal = vec2(19,5.75577)

        x_bounds = vec2(0,20)
        y_bounds = vec2(0,15)

        left = 0
        right = 1

        return Level(env, car, goal, x_bounds, y_bounds, left, right)




    def test():
        env = Environment()
        env.add_ground(
            [(0,5+e), (6,5+e), (6,0)],
            anchors=[vec2(6,5), vec2(6, 3),
                vec2(2, 14), vec2(6, 14),
                vec2(2, 13), vec2(14, 13),
                vec2(2, 12), vec2(16, 12),
                vec2(3, 11), vec2(16, 11),
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
        
        #Bridge
        env.add_road(vec2(6,5), vec2(8,5))
        env.add_road(vec2(8,5), vec2(10,5))
        env.add_road(vec2(10,5), vec2(12,5))
        env.add_road(vec2(12,5), vec2(14,5))
        
        env.add_plank(vec2(6,5), vec2(7,6))
        env.add_plank(vec2(7,6), vec2(8,5))
        env.add_plank(vec2(8,5), vec2(9,6))
        env.add_plank(vec2(9,6), vec2(10,5))
        env.add_plank(vec2(10,5), vec2(11,6))
        env.add_plank(vec2(11,6), vec2(12,5))
        env.add_plank(vec2(12,5), vec2(13,6))
        env.add_plank(vec2(13,6), vec2(14,5))
        
        env.add_plank(vec2(7,6), vec2(9,6))
        env.add_plank(vec2(9,6), vec2(11,6))
        env.add_plank(vec2(11,6), vec2(13,6))
        
        
        # first road test
        env.add_road(vec2(3,11),vec2(3,9))
        env.add_road(vec2(3,9), vec2(3,7))
        env.add_road(vec2(3,7), vec2(5,7))
        env.add_road(vec2(5,7), vec2(5,9))
        env.add_road(vec2(5,9), vec2(3,9))
        env.add_road(vec2(3,9), vec2(1,9))
        env.add_road(vec2(1,9), vec2(1,7))
        env.add_road(vec2(1,7), vec2(3,7))
        env.add_road(vec2(3,7), vec2(2,8))
        env.add_road(vec2(2,8), vec2(3,9))
        env.add_road(vec2(3,9), vec2(4,8))
        env.add_road(vec2(4,8), vec2(3,7))
        env.add_road(vec2(5,7), vec2(4,8))
        env.add_road(vec2(4,8), vec2(5,9))
        env.add_road(vec2(2,8), vec2(1,9))
        env.add_road(vec2(2,8), vec2(1,7))
        env.add_road(vec2(3,7), vec2(3,5))
        
        
        
        # second road test
        env.add_road(vec2(16,11), vec2(16,9))
        env.add_road(vec2(16,9), vec2(18,9))
        env.add_road(vec2(18,9), vec2(18,7))
        env.add_road(vec2(18,7), vec2(16,7))
        env.add_road(vec2(16,7), vec2(16,9))
        env.add_road(vec2(16,9), vec2(14,9))
        env.add_road(vec2(14,9), vec2(14,7))
        env.add_road(vec2(14,7), vec2(16,7))
        env.add_road(vec2(16,7), vec2(16,5))
        env.add_road(vec2(16,5), vec2(16,3))
        env.add_road(vec2(14,7), vec2(15,8))
        env.add_road(vec2(15,8), vec2(16,7))
        env.add_road(vec2(15,8), vec2(16,9))
        env.add_road(vec2(15,8), vec2(14,9))
        env.add_road(vec2(16,9), vec2(17,8))
        env.add_road(vec2(17,8), vec2(18,9))
        env.add_road(vec2(17,8), vec2(16,7))
        env.add_road(vec2(18,7), vec2(17,8))

        car = env.add_car(vec2(5,5.5+e), density=3)

        goal = vec2(19,6)

        x_bounds = (0,20)
        y_bounds = (0,15)

        left = 0
        right = 2 

        return Level(env, car, goal, x_bounds, y_bounds, left, right)

