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
import numpy as np
import random
import keras
from keras.optimizers import Adam
from webSockerInteractor import wsEnv


#import cntk as tf
#Tensorflow = 1
#Microsoft CNTK = 0
config = tf.ConfigProto( device_count = {'GPU': 1 , 'CPU': 8} )
sess = tf.Session(config=config)
keras.backend.set_session(sess)


class DQN:
    def __init__(self, env):
        self.env     = env
        self.memory  = deque(maxlen=2000)
        self.gamma = 0.85
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.005
        self.tau = .125

        self.model        = self.create_model()
        self.target_model = self.create_model()

    def create_model(self):
        model   = Sequential()
        state_shape  = (47,)
        model.add(Dense(128, input_dim=state_shape[0], activation="relu"))
        model.add(Dense(480, activation="relu"))
        model.add(Dense(124, activation="relu"))
        model.add(Dense(8))
        model.compile(loss="mean_squared_error",
            optimizer=Adam(lr=self.learning_rate))
        return model


    def act(self, state):
        self.epsilon *= self.epsilon_decay
        self.epsilon = max(self.epsilon_min, self.epsilon)
        if np.random.random() < self.epsilon:
            return np.random.randint(0, 8)
        return np.argmax(self.model.predict(state)[0])

    def remember(self, state, action, reward, new_state, done):
        self.memory.append([state, action, reward, new_state, done])

    def replay(self):
        batch_size = 32
        if len(self.memory) < batch_size:
            return

        samples = random.sample(self.memory, batch_size)
        for sample in samples:
            state, action, reward, new_state, done = sample
            target = self.target_model.predict(state)
            if done:
                target[0][action] = reward
            else:
                Q_future = max(self.target_model.predict(new_state)[0])
                target[0][action] = reward + Q_future * self.gamma
            self.model.fit(state, target, epochs=1, verbose=0)

    def target_train(self):
        weights = self.model.get_weights()
        target_weights = self.target_model.get_weights()
        for i in range(len(target_weights)):
            target_weights[i] = weights[i] * self.tau + target_weights[i] * (1 - self.tau)
        self.target_model.set_weights(target_weights)

    def save_model(self, fn):
        self.model.save(fn)

def main():
    env     = wsEnv()
    gamma   = 0.9
    epsilon = .95
    trials  = 1000
    trial_len = 500

    # updateTargetNetwork = 1000
    bestScore = 0
    dqn_agent = DQN(env=env)
    rewards = []
    for trial in tqdm(range(trials)):
        cur_state = env.reset().reshape(1,47)
        score = 0
        for step in (range(trial_len)):
            action = dqn_agent.act(cur_state)
            new_state, reward, done, _ = env.step(action)
            new_state = new_state.reshape(1,47)
            dqn_agent.remember(cur_state, action, reward, new_state, done)
            if reward ==1:
                score += 1
            dqn_agent.replay()       # internally iterates default (prediction) model
            dqn_agent.target_train() # iterates target model
            cur_state = new_state
        rewards.append(score)
        print("Agent Scored: {}\nAverage Score: {}".format(score,
            sum(rewards)/len(rewards)))
        rewards.append(score)
        if bestScore < score:
            print("New best model : scored {} trials".format(score))
            dqn_agent.save_model("bestDQNModel.model")
            bestScore = score

    return dqn_agent


if __name__ == "__main__":
    probablyGoodAgent = main()