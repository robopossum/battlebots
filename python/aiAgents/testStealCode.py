#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 23:52:30 2019

@author: tom
"""
#import cntk as C
import tensorflow as tf
from collections import deque
from keras import Sequential
from keras.layers import Dense
from tqdm import tqdm
from keras.optimizers import Adam, Nadam
from keras.utils.training_utils import multi_gpu_model
from customAIGYM import firstAttempt
import numpy as np
import random
import keras
from datetime import datetime as dt


#import cntk as tf

#Tensorflow = 1
#Microsoft CNTK = 0
config = tf.ConfigProto( device_count = {'GPU': 1 , 'CPU': 8} )
sess = tf.Session(config=config)
keras.backend.set_session(sess)

#iBackend = 1

#backendSelector(iBackend)

#def backendSelector(iBackend):
#    if self.iBackend == 0:
#        config = C.device.try_set_default_device(C.device.gpu(0))
#        sess = C.Session(config=config)
#        keras.backend.set_session(sess)
#    elif self.iBackend == 1:
#        config = tf.ConfigProto( device_count = {'GPU': 1 , 'CPU': 8} )
#        sess = tf.Session(config=config)
#        keras.backend.set_session(sess)
#

bestScore = 10


# Deep Q-learning Agent
class DQNAgent:
    def __init__(self, state_size=4, action_size=None):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=20000)
        self.gamma = 0.95    # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()
    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        model = Sequential()
        model.add(Dense(48, input_dim=self.state_size, activation='selu'))
        model.add(Dense(96, activation='relu'))
        model.add(Dense(192, activation='selu'))
#        model.add(Dense(192, activation='elu'))
#        model.add(Dense(684, activation='tanh'))
#        model.add(Dense(1284, activation='tanh'))
#        model.add(Dense(1384, activation='hard_sigmoid'))
#        model.add(Dense(2384, activation='exponential'))
#        model.add(Dense(1384, activation='elu'))
#        model.add(Dense(684, activation='tanh'))
        #model.add(Dense(392, activation='relu'))
        model.add(Dense(128, activation='relu'))
        model.add(Dense(self.action_size, activation='softmax'))
        model.compile(loss='mse',
                      optimizer=Nadam())
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
    episodes = 50000
    bestScore = 10

    scores = list()

    for e in range(episodes):
        # reset state in the beginning of each game
        state = env.reset()
        state = np.reshape(state, [1, 47])
        agent.currentScore = 0
        # time_t represents each frame of the game
        # Our goal is to keep the pole upright as long as possible until score of 500
        # the more time_t the more score
        for time_t in  tqdm(range(500)):
            # turn this on if you want to render
            # env.render()
            # Decide action
            action = agent.act(state)
            # Advance the game to the next frame based on the action.
            # Reward is 1 for every frame the pole survived
            next_state, reward, done, _ = env.step(action)
            next_state = np.reshape(next_state, [1, 47])
            # Remember the previous state, action, reward, and done
            # make next_state the new current state for the next frame.
            state = next_state
            # done becomes True when the game ends
            # ex) The agent drops the pole
            if reward == 1:
                agent.remember(state, action, reward, next_state, done)
                # print the score and break out of the loop
        print("episode: {}/{}, score: {}"
                      .format(e, episodes, agent.currentScore))
        # train the agent with the experience of the episode
        if agent.currentScore > bestScore:
            print("Better Agent Found, Saving!")
            agent.model.save_weights("bestModel_weights5.h5f") # so when we get a good model during training we save it
            bestScore = agent.currentScore
            agent.model.save_weights("currentDeepKerasModel_weights.h5f")
        if len(agent.memory) > 64:
            startTime = dt.now()
            agent.replay(64)
            timeTaken = (dt.now() - startTime).total_seconds()
            print("Took {} to train the model".format(timeTaken))

def playGame(agent, env):
    agent.model.load_weights("bestModel_weights4.h5f") # here we load what ever model we have to the agent
    state = env.reset(headless=False)
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

from webSockerInteractor import wsEnv

if __name__ == "__main__":
    # initialize gym environment and the agent
    agent = DQNAgent(47, 7)
    # Iterate the game
    train = True
    #env = firstAttempt.FooEnv()
    env = wsEnv()
    #playGame(agent, env)   #< if loading an old model to train, play the game before entering the conditional
    if train is True:
        #env = firstAttempt.FooEnv()
        trainMethod(agent, env)
    else:
        #env = firstAttempt.FooEnv(headless=False)
        agent.epsilon = 0.05
        playGame(agent, env)
    env.browser.quit()