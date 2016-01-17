from __future__ import division
import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator
import numpy as np 

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env, learning_rate=0.7, gamma=0.4):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        self.Q = {}
        self.gamma = gamma
        self.alpha = learning_rate
        self.Action = Environment.valid_actions # [None, 'forward', 'left', 'right']
        # self.Action = ['forward', 'left', 'right', None]
        self.state_transitions = {}
        # to check percent failures 
        self.failed_deadline = []
        self.trial_number = 1

    def reset(self, destination = None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required
        # reset state transition 
        self.state_transitions = {}
        self.trial_number += 1

    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # TODO: Update state
        # use inputs and next_waypoint
        current_state = tuple(inputs.values() + [self.next_waypoint])
        # easier to see on screen 
        interpretable_current_state = (inputs, self.next_waypoint)
        self.state = interpretable_current_state

        # TODO: Select action according to your policy
        action = None
        # ----- ***** IMPLEMENT BASIC DRIVING AGENT ***** -----
        # action = np.random.choice(self.A)
        # ----- ***** ----------------------------- ***** -----

        # for new Q(state, action)
        if current_state not in self.Q.keys():
            # initializing to zero doesn't work since valid action is None
            self.Q[current_state] = [3, 3, 3, 3] # the higher the more exploration

        def find_maxQ(self):
            '''max Q value for current state'''
            return self.Q[current_state].index(np.max(self.Q[current_state]))

        Q_max = find_maxQ(self)

        # Execute action and get reward
        action = self.Action[Q_max]
        reward = self.env.act(self, action)

        # TODO: Learn policy based on state, action, reward
        self.state_transitions[t] = (current_state, self.Action.index(action), reward)

        def update_Q(self):
            ''' learning rate - learning step size, that is, how fast learning takes place
                gamma - A higher value of gamma means that the future matters more for the Q-value '''
            # Q(s,a) = (1 - alpha) Q(s,a) + alpha(r + Qmax(s',a'))
            # Compute: Q(state, action) = R(state, action) + Gamma * Max[Q(next state, all actions)]

            # update after initial step
            if t != 0:
                self.Q[self.state_transitions[t - 1][0]][self.state_transitions[t - 1][1]] = \
                (1 - self.alpha) * self.Q[self.state_transitions[t - 1][0]][self.state_transitions[t - 1][1]] + \
                (self.alpha * (self.state_transitions[t - 1][2] + self.gamma * self.Q[current_state][Q_max]))

            # if agent reaches destination, reward = 10 if destination  
            if reward > 2:  
                self.Q[current_state][self.Action.index(action)] = \
                    (1 - self.alpha) * self.Q[current_state][self.A.index(action)] + (self.alpha * reward)
                
            # if deadline is hit 
            else:  
                if deadline == 0:
                    self.Q[current_state][self.Action.index(action)] = \
                        (1 - self.alpha) * self.Q[current_state][self.Action.index(action)] + (self.alpha * reward)
                    self.failed_deadline.append(0)
        print 'Failed Percent:', (len(self.failed_deadline) / self.trial_number)

        update_Q(self)

        print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]


def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # set agent to track

    # Now simulate it
    sim = Simulator(e, update_delay=0.000001)  # reduce update_delay to speed up simulation
    sim.run(n_trials=150)  # press Esc or close pygame window to quit


if __name__ == '__main__':
    run()
