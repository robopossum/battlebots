# -*- coding: utf-8 -*-
"""
Created on Sat Feb  9 18:25:37 2019

@author: mainuser
"""
import json
from websocket import create_connection

import gym
from gym import error, spaces, utils
from gym.utils import seeding



class webSocketInteractor:
    def __init__(self):
        self.ws = create_connection("ws://localhost:3001")
        #self.ws.send("Yo Server! Sort me out with a new game ;)")
        self.result =  json.loads(self.ws.recv())
        self.gameId = self.result['data']

    def closeCon(self):
        self.ws.close()

    def sendMessage(self, msg):
        self.ws.send(json.dumps({'gameID': self.gameId, 'data': msg}))

    def getMsg(self):
        result = self.ws.recv()
        while result == '[object Object]':
            result = self.ws.recv()
        return json.loads(result)



def mapAction(actionNo):
    if actionNo == 1:
        return {'up': 1}
    elif actionNo == 2:
        return {'down': 1}
    elif actionNo == 3:
        return {'left': 1}
    elif actionNo == 4:
        return {'right': 1}
    elif actionNo == 5:
        return {'turnLeft': 1}
    elif actionNo == 6:
        return {'turnRight': 1}
    elif actionNo == 0:
        return {'shoot': 1}
    else:
        return {}


if __name__ == "__main__":
    from tqdm import tqdm
    import random

    test = webSocketInteractor()
    test.sendMessage("Yo")

    for x in tqdm(range(1, 1000)):
        action = mapAction(random.randint(0, 7))
        test.sendMessage(action)
        state = test.getMsg()
    print(state)
    test.closeCon()








class wsEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, noEpisodes=1000, headless=True):


        #self.browser = None
        self.reset(headless)
        self.noEpisodes = noEpisodes
        #time.sleep(5)
        # pass

    def step(self, action):
        #print("action is {}, step {}!".format(action, self.iterations))
        self.takeAction(self.mapAction(action))
        newState = self.con.getMsg()
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
        self.con = webSocketInteractor()
        self.con.sendMessage(7)
        #time.sleep(5)
        self.rawState = self.con.getMsg()
        return ProcessState(self.rawState)

    def render(self, mode='human', close=False):
        pass


# this method can be updated once we know update type.
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
        self.con.sendMessage(controlObject)

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
        elif actionNo == 7:
            return {'shoot':1}

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





































if __name__ == '__main__':
    test = gameAgent()



