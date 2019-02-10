# -*- coding: utf-8 -*-
"""
Created on Fri Feb  8 22:05:41 2019

@author: mainuser
"""


from customAIGYM import firstAttempt
import keras



class bitchBot9000:
    def __init__(self):
        print("Human anihiliation initalized.")











if __name__ == "__main__":
    # initialize gym environment and the agent
    env = firstAttempt.FooEnv()
    agent = DQNAgent(47, 7)
    # Iterate the game
    train = True
    #playGame(agent, env)
    if train is True:
        trainMethod(agent, env)
    else:
        agent.epsilon = 0
        playGame(agent, env)
