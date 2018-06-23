#! /usr/env/bin python

import random

import numpy as np
import matplotlib.pyplot as plt


class RightWrong:

    def __init__(self, n_states, agent, verbose=0):
        self.agent = agent
        self.n_states = n_states
        self.action_history = []
        self.verbose = verbose

    def take_action(self, action):

        self.action_history.append(action)

        new_state = self.agent.current_state + action

        reward = int(new_state == self.n_states) 

        return reward, new_state

    def run_episode(self, max_steps=5000, episode_num=1):

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

        n_steps = []

        for episode_num in range(1, n_episodes+1):
            episode_steps = self.run_episode(episode_num=episode_num)

            n_steps.append(episode_steps)

            # if self.agent.replace_trace:
            #     import ipdb; ipdb.set_trace()

            self.agent.reset()
            self.action_history.append(-1)

        return np.array(n_steps)


class Agent:

    def __init__(self, n_states, learn_rate=0.1, replace_trace=False, discount=0.99, 
                 eligibility_decay=0.9, epsilon=0.1, clear_revist=False):
        """
        :param learn_rate float: learning rate (aka alpha)
        :param bool replace_trace: If false, eligibility accumulates
        :param discount float: discount factor for future rewards (aka gamma)
        :param eligibility_decay float: decay on eligibility traces (aka lambda)
        :param epsilon float: probability of exploring under e-greedy
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
        self.Q = np.zeros((self.n_states+1, 2))
        self.E = np.zeros((self.n_states+1, 2))

        self._greedy = False

        self.reset()

    def reset(self):
        self.current_state = 0
        self.last_action = None
        self.E = np.zeros(self.E.shape)

    @property
    def greedy(self):
        return self._greedy

    @greedy.setter
    def greedy(self, val):
        self._greedy = bool(val)

    def select_action(self, state=None):

        if state is None:
            state = self.current_state

        if self.greedy or random.random() > self.epsilon:
            if self.Q[state, 0] == self.Q[state, 1]:
                action = int(random.random() > 0.5)
            else:
                action = int(np.argmax(self.Q[state, :]).flatten())

        else:
            action = int(random.random() > 0.5)

        return action

    def update_state_and_select_action(self, reward, new_state):

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

    n_alpha = 25
    n_exp = 100

    results = np.zeros((n_alpha, 2, n_exp))
    n_states = 10

    alphas = np.linspace(0.05, 0.95, n_alpha).tolist()

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
