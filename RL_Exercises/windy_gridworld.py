#!/usr/env/bin python
"""
A Sarsa solution to the Stocastic Windy Gridworld Problem:

You are attempting to move through a grid world which is n_y x n_x
You want to reach a goal location G specified as g_x, g_y
Each column in X has a wind that moves you, stochastically.
The stocastic delta is equally distributed from {-1, 0, 1} if the wind value is non-zero

From Sutton and Barto, Exercise 6.7
"""

import random

import numpy as np
from scipy import signal
import matplotlib.pyplot as plt


action_to_delta_yx = [
    (1, 0),  # up
    (1, 1),
    (0, 1),  # right
    (-1, 1),
    (-1, 0),  # down
    (-1, -1),
    (0, -1),  # left
    (1, -1),
]


class Agent:
    """
    Agent to play the windy gridworld game.
    Uses Sarsa to update the action-value estimates with an e-greedy policy
    """

    def __init__(self, n_y, n_x, discount=1., epsilon=0.1, alpha=0.1,
                 kings_moves=True):
        """
        :param discount float: future reward discount factor (lambda)
        :param epsilon float: probability of exploring under e-greedy
        :param alpha float: step size on update
        :param kings_moves bool: If True, agent can move in 8 directions
        """
        # Initialize state
        self.n_actions = 8 if kings_moves else 4
        self.n_x = n_x
        self.n_y = n_y
        self.reset()
        # Store hyper parameters
        self.discount = discount
        self.alpha = alpha
        self.epsilon = epsilon
        self.kings_moves = kings_moves
        self.greedy = False

        # Initialize the action value estimates
        self.Q = np.zeros((n_y, n_x, self.n_actions))

    def reset(self, greedy=None):
        """
        Sets the agent back at the starting point
        Option to make the policy fully greedy.
        """
        self.y = int(self.n_y/2.)
        self.x = 0
        if greedy is not None:
            self.greedy = greedy

    def select_action(self, y=None, x=None):
        """
        Select an action according to an e-greedy policy based on the
        current state.

        Action definition: up is 0, right is 2, down is 4, left is 6
        """
        if (not self.greedy) and (random.random() < self.epsilon):
            action = random.randint(0, self.n_actions-1)
        else:
            sx = self.x if x is None else x
            sy = self.y if y is None else y
            action = np.argmax(self.Q[sy, sx, :].flatten()).flatten()

            equal = np.argwhere(self.Q[sy, sx, :] == self.Q[sy, sx, action])
            equal = equal.flatten()
            if len(equal) > 1:
                action = random.choice(equal.tolist())
            action = int(action)

        return action

    def update(self, prev_action, new_y, new_x, reward):
        """
        Moves agent to new state, and updates the action value estimates
        with the reward via Sarsa.
        """
        # Get the previous estimated value of previous action
        prev_est = self.Q[self.y, self.x, prev_action]

        # Select a possible next action according to current policy
        next_action = self.select_action(y=new_y, x=new_x)
        next_act_value = self.Q[new_y, new_x, next_action]

        # Update the action value estimate
        self.Q[self.y, self.x, prev_action] += (
            self.alpha*(reward + self.discount*next_act_value - prev_est)
        )

        # Update the agent's state
        self.y = new_y
        self.x = new_x

        return next_action


class WindyGridWorld:
    """
    Class to implement the Environment
    """
    def __init__(self, agent, goal, n_y=7, n_x=10, mean_wind=None, sigma=1):
        """
        agent - agent class to interact with the world
        goal - y, x coordinate to reach
        n_y, n_x - size of the world
        mean_wind - mean wind for each column in x, if None, randomly done
        sigma - stocastic wind equally distributed +- this, e.g. 1 is {-1, 0, 1}
        """
        self.agent = agent

        if mean_wind is None:
            self.mean_wind = np.random.randint(-1, 2, (n_y,))
        else:
            self.mean_wind = np.zeros(n_x, dtype=np.int)
            self.mean_wind[:len(mean_wind)] = mean_wind

        self.goal_x = goal[1]
        self.goal_y = goal[0]
        self.n_x = n_x
        self.n_y = n_y
        self.sigma = sigma

        self.state_history = [(agent.y, agent.x)]
        self.action_history = []

    def get_new_state_and_reward(self, action, y, x):
        """
        Given an action from the agent, and the current position,
        output the next position and the reward
        """

        if y == self.goal_y and x == self.goal_x:
            return y, x, 0

        if self.agent.kings_moves:
            move_y, move_x = action_to_delta_yx[action]
        else:
            move_y, move_x = action_to_delta_yx[action*2]

        wind_y = (
            self.mean_wind[int(x)] +
            random.randint(-self.sigma, self.sigma)
        )

        new_y = min(max(y + move_y + wind_y, 0), self.n_y-1)
        new_x = min(max(x + move_x, 0), self.n_x-1)

        at_goal = new_x == self.goal_x and new_y == self.goal_y

        reward = 0 if at_goal else -1

        return new_y, new_x, reward

    def play(self, max_steps=5000, skip_update=False):
        """
        Play the game until agent reaches goal or max steps
        """
        goal_not_reached = True
        step = 0
        agent = self.agent
        action = agent.select_action()
        while goal_not_reached and step < max_steps:

            self.action_history.append(action)
            new_y, new_x, reward = self.get_new_state_and_reward(
                action, agent.y, agent.x
            )
            next_action = agent.update(action, new_y, new_x, reward)

            self.state_history.append((agent.y, agent.x))

            goal_not_reached = (
                new_x != self.goal_x or new_y != self.goal_y
            )
            step += 1
            action = next_action

        if goal_not_reached:
            self.action_history.append(-1)
        else:
            self.action_history.append(8)

        return step

    def show_path(self):
        """
        Forensic method to show what happened
        """
        path = np.vstack(self.state_history)
        plt.figure(1)
        plt.subplot(2, 1, 1)
        plt.plot(self.action_history, 'r.')
        plt.subplot(2, 1, 2)
        plt.plot(path[:, 1], path[:, 0], '-bx', self.goal_x, self.goal_y, 'go')
        plt.figure(2)
        n_s, _ = path.shape
        plt.plot(range(n_s), path[:, 0], '-rx', range(n_s), path[:, 1], '-bx')
        plt.show()


def main():

    n_steps = []
    n_y = 7
    n_x = 10
    goal = (3, 7)
    mean_wind = [0, 0, 0, 1, 1, 1, 2, 2, 1, 0]

    agent = Agent(n_y, n_x, epsilon=0.1, alpha=0.1, kings_moves=True)

    n_train = 5000

    for episode in range(n_train):
        # Make the last attempt follow a greedy deterministic policy
        if episode == (n_train - 1):
            print("Following Greedy Policy")
            agent.reset(greedy=True)
        world = WindyGridWorld(
            agent, goal, n_y, n_x,
            mean_wind=mean_wind, sigma=1
        )
        n_actions = world.play()
        n_steps.append(n_actions)

        print("Finished episode", episode, "in", n_actions, "actions")
        agent.reset()  # put back to the starting point
        if False:
            world.show_path()
            # path = np.vstack(world.state_history)
            #plt.plot(range(10), path[:10, 0], '-rx', range(10), path[:10, 1], '-bx'); plt.show()
            # plt.imshow(agent.Q[:,0,:]); plt.show()
            import ipdb; ipdb.set_trace()

    path = np.vstack(world.state_history)

    # Plot the raw and smoothed # of steps as a function of episode
    filt = np.ones(25)/25
    avg_steps = signal.convolve(n_steps, filt, mode='same')
    plt.subplot(2, 1, 1)
    plt.plot(n_steps, 'r.', avg_steps, 'b')
    # Plot the final optimal policy
    plt.subplot(2, 1, 2)
    plt.plot(path[:, 1], path[:, 0], '-b.', goal[1], goal[0], 'go')

    # Plot the # of episodes as a function of time. (to match book)
    plt.figure(2)
    time_steps = np.cumsum([0] + n_steps)
    episode = range(len(time_steps))
    plt.plot(time_steps, episode)

    plt.show()


if __name__ == "__main__":
    main()
