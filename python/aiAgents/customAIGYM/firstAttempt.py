#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 19:58:32 2019

@author: tom
"""
from datetime import datetime as dt
import pandas as pd
import splinter
import random
import json
import time
from threading import Thread

class browserEnvironment():
    currentAction = str()
    def resetEnvironment(self):
        if self.browser is not None:
            self.browser.quit()
        browser = splinter.Browser()
        time.sleep(5)
        browser.visit("http://localhost:3000")
        time.sleep(5)
        self.browser = browser

    def __init__(self):
        self.browser = None
        self.resetEnvironment()

    def getState(self):
        return self.browser.evaluate_script("clientState")

    def takeAction(self, actions):
        jsCommand = str()
        for k,v in actions.items():
            if k in ['agentId', 'messageType']:
                continue
            jsCommand = "clientControl.{} = {};".format(k,v)
            self.browser.evaluate_script(jsCommand)
        #time.sleep(0.2)

import gym
from gym import error, spaces, utils
from gym.utils import seeding


class FooEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, noEpisodes=1000, headless=True):
        self.browser = None
        self.reset(headless)
        self.noEpisodes = noEpisodes
        time.sleep(5)
        pass

    def step(self, action):
        #print("action is {}, step {}!".format(action, self.iterations))
        self.takeAction(self.mapAction(action))
        newState = self.browser.evaluate_script("clientState")
        step_reward = newState['xp'] - self.rawState['xp']
        self.rawState = newState
        done = False
        if self.iterations == self.noEpisodes:
            done = True
        self.iterations += 1
        #self.LSTMStateUpdate(ProcessState(self.rawState))
        return ProcessState(self.rawState), step_reward, done, {}

    def reset(self, headless=True):
        self.memState = np.zeros((50, 47))
        self.iterations = 0
        if self.browser is None:
            kwargs= {'executable_path':'C:/Users/mainuser/Documents/GitHub/battlebots/webDriver/geckodriver.exe',
                     'headless': headless}
            browser = splinter.Browser('firefox', **kwargs)
            time.sleep(5)
            browser.visit("http://localhost:3000")
            self.browser = browser
        else:
            self.browser.reload()
        time.sleep(5)
        self.rawState = self.browser.evaluate_script("clientState")
        return ProcessState(self.browser.evaluate_script("clientState"))

    def render(self, mode='human', close=False):
        pass

    def takeAction(self, actions):
        controlObject = {
                    "up": 0,
                    "down": 0,
                    "left": 0,
                    "right": 0,
                    "turnLeft": 0,
                    "turnRight": 0,
                    "shoot": 0,
                    }
        for k, v in actions.items():
            controlObject[k] = v
        jsCommand = str()
        for k,v in controlObject.items():
            if k in ['agentId', 'messageType']:
                continue
            jsCommand = "clientControl.{} = {};".format(k,v)
            self.browser.evaluate_script(jsCommand)

    def LSTMStateUpdate(self, state):
        self.memState = np.delete(self.memState, -1, 0)
        self.memState = np.insert(self.memState, 0,
                                  values=state, axis=0)




    def mapAction(self, actionNo):

        if actionNo == 1:
            return {'up':1}
        elif actionNo == 2:
            return {'down':1}
        elif actionNo == 3:
            return {'left':1}
        elif actionNo == 4:
            return {'right':1}
        elif actionNo == 5:
            return {'turnLeft':1}
        elif actionNo == 6:
            return {'turnRight':1}
        elif actionNo == 0:
            return {'shoot':1}

# test scripts
if __name__ == "__main__":
    print("hEllo")
    # we first start the browser
    brow = FooEnv()

    # then we confirm we can access a state;
    state = brow.step(0)

    # state should be dict as;
state = {
         'agentId': 1,
         'canShoot': True,
         'dX': 0,
         'dY': 0,
         'x': 400,
         'xp': 0,
         'y': 300,
         'messageType': 'frame',
         'sensors': [
                      {'angle': -50, 'hitting': 0, 'length': 125},
                      {'angle': -45, 'hitting': 0, 'length': 125},
                      {'angle': -40, 'hitting': 0, 'length': 125},
                      {'angle': -35, 'hitting': 0, 'length': 125},
                      {'angle': -30, 'hitting': 0, 'length': 125},
                      {'angle': -25, 'hitting': 0, 'length': 125},
                      {'angle': -20, 'hitting': 0, 'length': 125},
                      {'angle': -15, 'hitting': 0, 'length': 125},
                      {'angle': -10, 'hitting': 0, 'length': 125},
                      {'angle': -5, 'hitting': 0, 'length': 125},
                      {'angle': 0, 'hitting': 0, 'length': 125},
                      {'angle': 5, 'hitting': 0, 'length': 125},
                      {'angle': 10, 'hitting': 0, 'length': 125},
                      {'angle': 15, 'hitting': 0, 'length': 125},
                      {'angle': 20, 'hitting': 0, 'length': 125},
                      {'angle': 25, 'hitting': 0, 'length': 125},
                      {'angle': 30, 'hitting': 0, 'length': 125},
                      {'angle': 35, 'hitting': 0, 'length': 125},
                      {'angle': 40, 'hitting': 0, 'length': 125},
                      {'angle': 45, 'hitting': 0, 'length': 125},
                      {'angle': 50, 'hitting': 0, 'length': 125}],}

# we need to make a method to translate this to numpy...
import numpy as np

def ProcessState(state):
    ret = state.copy()
    try:
        del ret['agentId']
        #del ret ['y']
        #del ret ['x']
        del ret['messageType']
        del ret['canShoot']
    except KeyError:
        pass
    hittingAr = [x['hitting'] for x in ret['sensors']]
    distAr = [x['length'] for x in ret['sensors']]
    del ret['sensors']
    return np.array(list(ret.values()) + hittingAr + distAr)
