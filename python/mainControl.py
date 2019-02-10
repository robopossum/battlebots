#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  3 00:46:26 2019

@author: tom
"""
from aiAgents import environmentInteractor
from aiAgents import expertSystemAgent
from tqdm import tqdm

# %load_ext autoreload
# %autoreload 2
import time


def playGame():
    time.sleep(5)
    noSteps = 1000
    for x in tqdm(range(noSteps)):
        state = environment.getState()
        # now we set the agent with a state
        agent.setState(state)
        # we get an action
        action = agent.getAction()
        # we now take the action in the environment;
        environment.takeAction(action)
    # now we see how we have done in 100 steps;
    environment.takeAction(expertSystemAgent.templateControlObject)
    stateScore = environment.getState()['xp']
    print("In {} steps, we were able to score {} xp".format(noSteps,
          stateScore))
#    environment.browser.quit()
    environment.browser.reload()
    return stateScore


if __name__ == "__main__":
    environment = environmentInteractor.browserEnvironment()
    # now we create our expert system based agent;
    agent = expertSystemAgent.expertSystemBasedAgent()

    culmScore = 0
    for x in range(100):
        culmScore += playGame()
    print("Stategy gained on average {} exp.".format(culmScore/10))
