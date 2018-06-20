#!/usr/env/bin python
"""
A Dynamic Programming solution to the Gambler's problem:
Given an unfair coin with even odds, and trying to get to a goal value,
what is the optimal amount to wager depending on how much money you have.
From Sutton and Barto Reinforcement Learning, Exercise 4.8
"""

import numpy as np
import matplotlib.pyplot as plt


class GamblerDP:
    """
    Dynamic Programming solution, using value iteration.
    """
    # state : how much money you have

    def __init__(self, win_prob=0.35, goal=128+8, gamma=1.):

        self.goal = goal
        self.win_prob = win_prob
        self.gamma = gamma
        self.policy = np.ones((goal+1,))
        self.policy[0] = 0
        self.value_estimates = np.zeros((goal+1,))

    def reward(self, state, new_state, action):
        return float(new_state >= self.goal)

    def iterate_values(self, state_idx, debug=0):

        old_val = self.value_estimates[state_idx]

        value_by_policy = np.zeros(state_idx+1)
        value_by_policy[0] = 0

        for stake in range(1, state_idx+1):
            end_states = (state_idx - stake, state_idx+stake)
            probs = (1. - self.win_prob, self.win_prob)
            for prob, new_state in zip(probs, end_states):
                reward = self.reward(state_idx, new_state, stake)
                if new_state >= self.goal:
                    val_est = 0.
                else:
                    val_est = self.value_estimates[new_state]
                value_by_policy[stake] += prob*(reward + self.gamma*val_est)

        best_policy = np.argmax(np.round(value_by_policy, 8))

        self.value_estimates[state_idx] = value_by_policy[best_policy]
        delta = abs(old_val - self.value_estimates[state_idx])
        self.policy[state_idx] = best_policy

        return delta

    def run(self, eps=1e-10):

        idx = 0
        max_delta = eps*2 + 1e-9

        while max_delta > eps:
            max_delta = 0.
            for state_idx in reversed(range(1, self.goal)):
                delta = self.iterate_values(state_idx)
                max_delta = max(max_delta, delta)

            idx += 1
            if idx % 25 == 0:
                print("Max delta: %d", max_delta)
                self.show_estimates()

        print("Finished! Max delta:", max_delta)
        self.show_estimates()

    def show_estimates(self):
        print("Value Estimates:")
        print(self.value_estimates)
        print("Policy:")
        print(self.policy)
        plt.subplot(2, 1, 1)
        plt.plot(self.value_estimates)
        plt.subplot(2, 1, 2)
        plt.plot(self.policy, marker='_', linewidth=0, linestyle='None')
        plt.show()

if __name__ == '__main__':
    G = GamblerDP()
    G.run()
