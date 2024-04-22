import sys
from sim.environment import Environment
from sim.ui import UI
from Box2D.b2 import vec2
from Box2D import b2Vec2
from levels import LevelFactory
import random 

import numpy as np


while True:
    alpha = random.random()*3 + 0.01
    beta = int(random.random()*2000 + 50)
    gamma = random.random()*9 + 0.3
    delta = (random.random()*5+0.1)
    alpha, beta, gamma, delta = 1.3475121952552491, 765, 3.99204226720507, 0.8214835226562238
    draw = False
    draw = True

    e=0.1
    env = Environment(
       buildable_weight=alpha,
       buildable_limit=beta,
       road_weight_multiplier=gamma,
       road_limit_multiplier=delta,
    )
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
    t1 = env.add_road(vec2(2,14), vec2(4,14))
    env.add_road(vec2(4,14), vec2(6,14))
    
    t2 = env.add_plank(vec2(2,13), vec2(4,13))
    env.add_plank(vec2(4,13), vec2(6,13))
    env.add_plank(vec2(6,13), vec2(8,13))
    env.add_plank(vec2(8,13), vec2(10,13))
    env.add_plank(vec2(10,13),vec2(12,13))
    env.add_plank(vec2(12,13),vec2(14,13))
    
    t3 = env.add_plank(vec2(2,12), vec2(4,12))
    env.add_plank(vec2(4,12), vec2(6,12))
    env.add_plank(vec2(6,12), vec2(8,12))
    env.add_plank(vec2(8,12), vec2(10,12))
    env.add_plank(vec2(10,12),vec2(12,12))
    env.add_plank(vec2(12,12),vec2(14,12))
    env.add_plank(vec2(14,12),vec2(16,12))
    
    #Bridge
    t4_1 = env.add_road(vec2(6,5), vec2(8,5))
    env.add_road(vec2(8,5), vec2(10,5))
    t4_2 = env.add_road(vec2(10,5), vec2(12,5))
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
    t4 = env.add_plank(vec2(9,6), vec2(11,6))
    env.add_plank(vec2(11,6), vec2(13,6))
    
    
    # first road test
    t5 = env.add_road(vec2(3,11),vec2(3,9))
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
    t6 = env.add_road(vec2(16,11), vec2(16,9))
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
    
    if draw: env.init_graphics()
    
    ui = UI(env)
    
    sim = True
    run = True
    wobble = 100
    for _ in range(100 * (4 if draw else 1)):
        if draw: env.draw()
        #ui.update(env.world)
        #ui.draw()

        if t4.body is not None: wobble = min(wobble, t4.body.position[1])
        
        env.step() if sim else None
    
        #for event in ui.events:
        #    if event.type == "quit":
        #        quit()
    
        #    elif event.type == "add-plank":
        #        print(f"env.add_plank{event.data}")
        #        env.add_plank(*event.data)
    
        #    elif event.type == "add-road":
        #        print(f"env.add_road{event.data}")
        #        env.add_road(*event.data)
    
        #    elif event.type == "sim":
        #        run = False
        #        sim = True
    
        #    elif event.type == "remove":
        #        #TODO
        #        pass
    passed = 0
    if (t1.body is None): passed += 1
    if (t2.body is not None): passed += 1
    if (t3.body is None): passed += 1
    if (t4.body is not None and t4_1.body is not None and t4_2.body is not None): passed += 1
    if (t5.body is not None): passed += 1
    if (t6.body is None): passed += 1
    if passed > 4 and (t4.body is not None and t4_1.body is not None and t4_2.body is not None) and (t1.body is None):
        print(f"{passed}/6 {wobble} --> {alpha}, {beta}, {gamma}, {delta}")


