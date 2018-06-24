#! /usr/env/bin python
"""
Exercise 7.7 from Sutton and Barto "Reinforcement Learning"

The goal is to empirically demonstrate the advantage of using replacing traces on
a problem where you always want to move "right" rather than stay in the same place. 

The issue is that accumulating traces can bias you towards staying in the same place. 

This code implements Sarsa(lambda) with lambda=0.9. 
"""

import random

import numpy as np
import matplotlib.pyplot as plt


class RightWrong:
    """
    Environment of a simple problem: you can either stay in the same place "wrong"
    or move to the right "Right". Terminal state is all the way to the right
    """

    def __init__(self, n_states, agent, verbose=0):
        """
        :param int n_states: # of states before termination
        :param Agent agent: Sarsa(lambda) agent which estimates action values
        :param int verbose: Print results to stdout
        """
        self.agent = agent
        self.n_states = n_states
        self.action_history = []
        self.verbose = verbose

    def take_action(self, action):
        """
        :param int action: 0 or 1 which is to stay or go right
        :returns: reward, new_state (ints)
        """
        self.action_history.append(action)

        new_state = self.agent.current_state + action

        reward = int(new_state == self.n_states) 

        return reward, new_state

    def run_episode(self, max_steps=5000, episode_num=1):
        """
        Runs one episode of the Right/Wrong game

        :param int max_steps: avoide infinite loop
        :param int episode_num: for printing / debugging
        :returns: total # of steps taken
        """
        not_terminated, step = True, 0
        agent = self.agent
        action = agent.select_action()
        agent.last_action = action

        while not_terminated and step < max_steps:

            reward, new_state = self.take_action(action)

            action = agent.update_state_and_select_action(
                reward, new_state
            )

            not_terminated = agent.current_state != self.n_states

            step += 1

        if self.verbose:
            print("Finished Episode", episode_num, "in", step, "steps")
        return step


    def run_experiment(self, n_episodes=100):
        """
        Runs a specific # of episodes and returns the # of steps until termination for each episode
        """
        n_steps = []

        for episode_num in range(1, n_episodes+1):
            episode_steps = self.run_episode(episode_num=episode_num)
            n_steps.append(episode_steps)

            # Reset agent back to the beginning
            self.agent.reset()
            self.action_history.append(-1)

        return np.array(n_steps)


class Agent:
    """
    Class which implements the Sarsa(lambda) algorithm for the Right/Wrong problem
    Utilizes an e-greedy policy based on action-value estimates
    """

    def __init__(self, n_states, learn_rate=0.1, replace_trace=False, discount=0.99, 
                 eligibility_decay=0.9, epsilon=0.1, clear_revist=False):
        """
        :param learn_rate float: learning rate (aka alpha)
        :param bool replace_trace: If false, eligibility accumulates
        :param discount float: discount factor for future rewards (aka gamma)
        :param eligibility_decay float: decay on eligibility traces (aka lambda)
        :param epsilon float: probability of exploring under e-greedy
        :param bool clear_revist: If True, all other actions will be set to 0 on revist
        """

        self.learn_rate = learn_rate
        self.replace_trace = replace_trace
        self.discount = discount
        self.eligibility_decay = eligibility_decay
        self.n_states = n_states
        self.epsilon = epsilon
        self.clear_revist = clear_revist

        self.clear()

    def clear(self):
        """
        Clears out traces and estimates and moves agent to start
        """
        self.Q = np.zeros((self.n_states+1, 2))
        self._greedy = False
        self.reset()

    def reset(self):
        """
        Clears out traces and moves agent to start
        """
        self.current_state = 0
        self.last_action = None
        self.E = np.zeros((self.n_states+1, 2))

    @property
    def greedy(self):
        """
        If True, agent will follow only the greedy strategy (e.g. e=0)
        """
        return self._greedy

    @greedy.setter
    def greedy(self, val):
        self._greedy = bool(val)

    def select_action(self, state=None):
        """
        Given a state, selects the next action based on an e-greedy policy

        :param int state: If None, will use agent's current state
        """
        if state is None:
            state = self.current_state

        if self.greedy or random.random() > self.epsilon:
            if self.Q[state, 0] == self.Q[state, 1]:
                # If states are equivalue, choose randomly
                action = int(random.random() > 0.5)
            else:
                action = int(np.argmax(self.Q[state, :]).flatten())

        else:  # randomly choose a state
            action = int(random.random() > 0.5)

        return action

    def update_state_and_select_action(self, reward, new_state):
        """
        Given a reward and a new state, update estimates and traces 
        based on the previous action, and select the next one
        :returns: next action [int] 
        """

        last_action = self.last_action
        if last_action is None:
            current_val = 0
            last_action = 0
        else:
            current_val = self.Q[self.current_state, last_action]

        new_action = self.select_action(new_state)

        delta = reward + self.discount*self.Q[new_state, new_action] - current_val
        
        if self.replace_trace:
            if self.clear_revist:
                self.E[self.current_state, :] = 0
            self.E[self.current_state, last_action] = 1
        else:
            self.E[self.current_state, last_action] += 1

        # Update the State-Action Values and Eligibility traces
        self.Q = self.Q + self.learn_rate*delta*self.E
        self.E = self.discount*self.eligibility_decay*self.E

        self.current_state = new_state
        self.last_action = new_action

        return new_action


def main():

    # Setup parameters
    n_alpha = 25
    alphas = np.linspace(0.05, 0.95, n_alpha).tolist()
    n_exp = 100  # number of times to run each experiment
    results = np.zeros((n_alpha, 2, n_exp))
    n_states = 10 

    for alp_idx, alpha in enumerate(alphas):
        for replace in (0, 1):
            for exp_idx in range(n_exp):
                agent = Agent(
                    n_states=n_states, 
                    learn_rate=alpha, 
                    replace_trace=bool(replace),
                    discount=0.99,  # important for numerical stability! 
                )
                world = RightWrong(n_states, agent)

                step_history = world.run_experiment(n_episodes=20)

                rms_err = np.mean(np.sqrt((step_history - n_states)**2))
                results[alp_idx, replace, exp_idx] = rms_err

    # Get the mean results for each experiment
    avg_results = np.mean(results, axis=2)
    # plot the results
    lines = plt.plot(alphas, avg_results[:, 0], '-rx', alphas, avg_results[:, 1], '-bx')
    plt.xlabel('Learn Rate (alpha)')
    plt.ylabel('RMS Error over # of steps')
    lines[0].set_label('Accumulated')
    lines[1].set_label('Replace')
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
