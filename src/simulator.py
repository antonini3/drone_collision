import sys, pygame, time, random, math
from itertools import permutations
import numpy as np
import threading

from constants import *
from mdp import *

class Simulator():

    def __init__(self):
        self.world = World(num_agents=5)
        self.mdp = MDP()

        pygame.init()
        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
        self.clock = pygame.time.Clock()

    def start_world(self):
        def world_thread():
            while True:
                self.screen.fill(LIGHT_BLUE)
                self.world.timestep()
                self.world.draw(self.screen)
                self.clock.tick(100)
                pygame.display.flip()


        self.thread = threading.Thread(target=world_thread)
        self.thread.start()

    def run_mdp(self):
        while True:
            for drone, target in zip(self.world.drones, self.world.targets):
                action = self.mdp.best_action(drone, target, self.world)
                drone.set_action(action)
            time.sleep(0.01)


    def simulate(self):
        self.start_world()
        self.run_mdp()



class World():

    def __init__(self, num_agents=1, width=WIDTH, height=HEIGHT):
        self.drones = []
        self.targets = []

        for _ in xrange(num_agents):
            self.drones.append(Drone(random.randrange(width), random.randrange(height)))
            self.targets.append(Target())

    def timestep(self):
        done = False
        for drone, target in zip(self.drones, self.targets):
            drone.move()
            if np.linalg.norm([drone.x - target.x, drone.y - target.y]) < 5.0:
                target.reset()
        return done
            

    def draw(self, surface):
        for target in self.targets:
            target.draw(surface)
        for drone in self.drones:
            drone.draw(surface)




class Target():

    def __init__(self, size=20):
        self.reset()
        self.size = size
        self.image = pygame.transform.scale(pygame.image.load('../img/target.png'), (size, size))

    def get_bounds(self):
        return self.x, self.y, self.size, self.size

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

    def get_state(self):
        return self.x, self.y

    def reset(self):
        self.x, self.y = random.randrange(WIDTH), random.randrange(HEIGHT)



class Drone():

    def __init__(self, x, y, size=20):
        self.lock = threading.Lock()
        self.x, self.y, self.size = x, y, size
        self.image = pygame.transform.scale(pygame.image.load('../img/drone1.png'), (size, size))
        self.heading = random.randrange(360)
        self.image = pygame.transform.rotate(self.image, self.heading)
        self.speed = 5.0
        self.actions = ANGULAR_ACTIONS
        self.set_action(random.choice(self.actions))

    def set_action(self, action):
        self.lock.acquire()
        self.action = action
        self.lock.release()

    def get_center(self):
        return self.x, self.y

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

    def get_actions(self):
        return ANGULAR_ACTIONS

    def move(self):
        # deg = np.random.normal(action, 0.005)
        self.lock.acquire()
        deg = self.action
        self.lock.release()
        # print deg, action
        x_, y_, heading_ = self.evaluate_next_state(deg)
        self.x = x_
        self.y = y_
        self.heading = heading_
        # self.image = pygame.transform.rotate(self.image, heading_)


    def get_state(self):
        return self.x, self.y, self.heading, self.speed


    def evaluate_next_state(self, action):
        heading_ = - g * math.tan(action) / self.speed
        temp_heading = self.heading + heading_
        heading = math.radians(temp_heading)
        x_ = self.speed * math.cos(heading)
        y_ = self.speed * math.sin(heading)
        # print 'X and y:',x_, y_
        return self.x + x_, self.y + y_, temp_heading


        

    # # Top, bottom, left, right
    # def get_bounds(self):
    #     return self.y, self.y + self.size, self.x, self.x + self.size



if __name__ == '__main__':
    simulator = Simulator()
    simulator.simulate()
















































# class Simulator():

#     def __init__(self, num_agents=1):
#         pygame.init()
#         self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
#         self.drones = pygame.sprite.Group()
#         self.clock = pygame.time.Clock()
#         self.agents = []

#         for _ in xrange(num_agents):
#             drone = DroneSprite(random.randrange(SCREEN_WIDTH), random.randrange(SCREEN_HEIGHT))
#             target = TargetSprite(random.randrange(SCREEN_WIDTH), random.randrange(SCREEN_HEIGHT))
#             self.agents.append((drone, target))
        

#     def __del__(self):
#         pygame.quit()

#     def simulate(self):
#         while True:
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     sys.exit()

#             self.screen.fill(WHITE)
#             for i, drone in enumerate(self.agents):
                
#                 self.drones.update()
#                 self.drones.draw(self.screen)
#                 self.target.draw(self.screen)
            
#             self.clock.tick(20)
#             pygame.display.flip()
