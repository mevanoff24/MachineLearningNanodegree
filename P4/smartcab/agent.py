import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator
import numpy as np

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env, learning_rate=0.6, discount_factor=0.35):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        self.alpha = learning_rate
        self.gamma = discount_factor
        self.state = None
        self.Q_values = self.initialize_Q_values()

    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required


    def initialize_Q_values(self, val=10.0):
        Q_values = {}
        for waypoint in ['left', 'right', 'forward']:
            for light in ['red', 'green']:
                for action in self.env.valid_actions:
                    Q_values[((waypoint, light), action)] = val
        return Q_values


    def find_max_Q(self, state):
        action = None
        max_Q = 0.0
        for act in self.env.valid_actions:
            Q = self.Q_values[(state, act)]
            if Q > max_Q:
                action = a
                max_Q = Q
        return (max_Q, action)


    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # TODO: Update state
        self.state = (self.next_waypoint, inputs['light'])

        # TODO: Select action according to your policy
        #action = random.choice([None, 'left', 'right', 'forward'])
        (Q, action) = self.find_max_Q(self.state)

        # Execute action and get reward
        reward = self.env.act(self, action)

        # TODO: Learn policy based on state, action, reward
        next_waypoint = self.planner.next_waypoint()
        inputs = self.env.sense(self)
        state_prime = (next_waypoint, inputs['light'])
        (Q_prime, action_prime) = self.find_max_Q(state_prime)        
        Q += self.alpha * (reward + self.gamma * Q_prime - Q) 
        self.Q_values[(self.state, action)] = Q

        print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]


def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=False)  # set agent to track

    # Now simulate it
    sim = Simulator(e)
    sim.run(n_trials=5)  # press Esc or close pygame window to quit


if __name__ == '__main__':
    run()
