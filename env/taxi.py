
import logging
import math
import gym
from gym import spaces
from gym.utils import seeding
import numpy as np
#from RideSimulator.taxi_sim import *

from tf_agents.environments import py_environment
from tf_agents.environments import tf_environment
from tf_agents.environments import tf_py_environment
from tf_agents.environments import utils
from tf_agents.specs import array_spec
from tf_agents.environments import wrappers
from tf_agents.environments import suite_gym
from tf_agents.trajectories import time_step as ts

class TaxiEnv(gym.Env):
    """
    Observation:
        Type: Box(4)
        Num     Observation               Min                     Max
        0       pickup dist               0                       inf
        1       trip distance             0                       inf
        2       time                      0                       24
        3       trips till weekly reward  0                       inf

    Reward:
        reward calculated through the trip  - static time loss

    Actions:
        Type: Discrete(2)
        Num   Action
        0     reject trip
        1     accept trip

    Starting state:
        all values start at 0
    
    Termination:
        12 weeks (12 x 7 x 24 mins)
    """

    def __init__(self, state_dict=None):

        #at least one of the low values HAS to be negative - why?
        low = np.array([-np.finfo(np.float32).max,0.0,0.0,-1.0], dtype=np.float32)
        self.theta_threshold_radians = 12 * 2 * math.pi / 360
        self.x_threshold = 2.4
        high = np.array([np.finfo(np.float32).max, np.finfo(np.float32).max ,24.0, np.finfo(np.float32).max], dtype=np.float32)
   

        self.action_space = spaces.Discrete(2)
        self.observation_space = spaces.Box(low, high, dtype=np.float32)

        self._episode_ended = False
        self.time_limit = 12 * 7 * 24

        self.steps = state_dict
        self.step_count = 0

        self.seed()
        self.viewer = None
        self.state = None


    def seed(self, seed=None):
        #seed not used currently
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):

        #TODO step through a single event in the simulation (run only one step)
        
        err_msg = "%r (%s) invalid" % (action, type(action))
        assert self.action_space.contains(action), err_msg

        pickup_dist, trip_dist, time, weekly_target = self.steps[self.step_count]["pickup_dist"], self.steps[self.step_count]["trip_count"], self.steps[self.step_count]["time"], self.steps[self.step_count]["weekly_target"]

        self.state = pickup_dist, trip_dist, time, weekly_target
        self.step_count += 1

        reward = self.steps["reward"]
        #termination through time limit

        if self.step_count == len(self.steps):
            done = True
        else:
            done = False

        
        """

        if not done:
            reward = 1.0
        elif self.steps_beyond_done is None:
            # Pole just fell!
            self.steps_beyond_done = 0
            reward = 1.0
        el
        #set up simpy env
        TIME_MULTIPLIER = 50
        DRIVER_COUNT = 1
        TRIP_COUNT = 8000
        RUN_TIME = 10000
        INTERVAL = 20
        # GRID_WIDTH = 3809
        # GRID_HEIGHT = 2622
        GRID_WIDTH = 60
        GRID_HEIGHT = 40
        HEX_AREA = 2.6           "True' -- any further steps are undefined behavior."
                )
            self.steps_beyond_done += 1
            reward = 0.0
        """

        return np.array(self.state), reward, done, {}

    def reset(self):
        
        self.state = np.array([0,0,0,20], dtype=np.float32)
        self._episode_ended = False

        """
        self.Env = simpy.Environment()
        self.map_grid = Grid(env=Env, width=self.GRID_WIDTH, height=self.GRID_HEIGHT, interval=self.INTERVAL, num_drivers=self.DRIVER_COUNT,
                        hex_area=self.HEX_AREA)

        self.taxi_spots = map_grid.taxi_spots
        self.driver_list = create_drivers(Env, self.DRIVER_COUNT, map_grid)
        self.driver_pools = map_grid.driver_pools

        #TODO statically generate a list of all the trips (theres nothing dynamic about trip generation)
        #TODO then run just one step in the / driver picking process

        # begin the simpy simulation (i.e. trip generation process)
        #run_simulation(TRIP_COUNT, RUN_TIME, DRIVER_COUNT, TIME_MULTIPLIER, map_grid, taxi_spots, driver_list, driver_pools, Env, rewards, steps, time_step, tf_env, policy)
        """

        return np.array(self.state)

    def render(self):
        print ("render")
        #print reward here

        return None

    def close(self):
        if self.viewer:
            self.viewer.close()
            self.viewer = Nonegym.envs.register(
     id='taxi-v0',
     entry_point='env.taxi:TaxiEnv',
     max_episode_steps=1500,
     kwargs={'states':None},
)
