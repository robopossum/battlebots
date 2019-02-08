#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 23:52:30 2019

@author: tom
"""
from collections import deque
from keras import Sequential
from keras.layers import Dense
from tqdm import tqdm
from keras.optimizers import Adam
from customAIGYM import firstAttempt
import numpy as np
import random
bestScore = 0




# Deep Q-learning Agent
class DQNAgent:
    def __init__(self, state_size=4, action_size=None):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=200000)
        self.gamma = 0.95    # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()
    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        model = Sequential()
        model.add(Dense(48, input_dim=self.state_size, activation='relu'))
        model.add(Dense(96, activation='relu'))
        model.add(Dense(192, activation='tanh'))
        # model.add(Dense(192, activation='sigmoid'))
        # model.add(Dense(384, activation='relu'))
        # model.add(Dense(1284, activation='tanh'))
        # model.add(Dense(1384, activation='tanh'))
        # model.add(Dense(4384, activation='tanh'))
        # model.add(Dense(1384, activation='tanh'))
        # model.add(Dense(384, activation='tanh'))
        model.add(Dense(192, activation='sigmoid'))
        model.add(Dense(48, activation='sigmoid'))
        model.add(Dense(self.action_size, activation='softmax'))
        model.compile(loss='mse',
                      optimizer=Adam(lr=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.currentScore += reward
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])  # returns action


    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + self.gamma * \
                         np.amax(self.model.predict(next_state)[0])
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=100, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay


def trainMethod(agent, env):
    episodes = 1
    bestScore = 25
    for e in range(episodes):
        # reset state in the beginning of each game
        state = env.reset()
        state = np.reshape(state, [1, 47])
        agent.currentScore = 0
        # time_t represents each frame of the game
        # Our goal is to keep the pole upright as long as possible until score of 500
        # the more time_t the more score
        for time_t in tqdm(range(1000)):
            # turn this on if you want to render
            # env.render()
            # Decide action
            action = agent.act(state)
            # Advance the game to the next frame based on the action.
            # Reward is 1 for every frame the pole survived
            next_state, reward, done, _ = env.step(action)
            next_state = np.reshape(next_state, [1, 47])
            # Remember the previous state, action, reward, and done
            agent.remember(state, action, reward, next_state, done)
            # make next_state the new current state for the next frame.
            state = next_state
            # done becomes True when the game ends
            # ex) The agent drops the pole
            if reward == 1:
                # print the score and break out of the loop
                print("episode: {}/{}, steps: {}/1000, score: {}"
                      .format(e, episodes, time_t, agent.currentScore))
        # train the agent with the experience of the episode
        from datetime import datetime as dt
        startTime = dt.now()

        agent.replay(64)
        agent.model.save_weights("currentDeepKerasModel_weights.h5f")
        timeTaken = (dt.now() - startTime).total_seconds()
        print("Took {} to train the model".format(timeTaken))
        if agent.currentScore > bestScore:
            print("Better Agent Found, Saving!")
            agent.model.save_weights("bestModel_weights.h5f")
            bestScore = agent.currentScore

def playGame(agent, env):
        agent.model.load_weights("currentDeepKerasModel_weights.h5f")
        state = env.reset()
        state = np.reshape(state, [1, 47])
        agent.currentScore = 0
        for time_t in tqdm(range(1000)):
            # turn this on if you want to render
            # env.render()
            # Decide action
            action = agent.act(state)
            next_state, reward, done, _ = env.step(action)
            next_state = np.reshape(next_state, [1, 47])
            state = next_state


if __name__ == "__main__":
    # initialize gym environment and the agent
    env = firstAttempt.FooEnv()
    agent = DQNAgent(47, 7)
    # Iterate the game
    train = True
    playGame(agent, env)
    if train is True:
        trainMethod(agent, env)
    else:
        playGame(agent, env)
